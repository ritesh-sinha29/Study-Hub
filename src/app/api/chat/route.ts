import { createOpenAI } from '@ai-sdk/openai';
import { streamText, tool, isStepCount } from 'ai';
import { NextResponse } from 'next/server';
import { z } from 'zod';
import { searchLocalCourses } from '@/lib/knowledge-base';
import { isAuthenticated } from '@/lib/auth-server';

// Allow streaming responses up to 30 seconds
export const maxDuration = 30;

// OpenAI configuration (commented out for future switch back)
// const openai = createOpenAI({
//   apiKey: process.env.OPENAI_API_KEY || '',
// });

// Alibaba Cloud Qwen Configuration (OpenAI Compatible)
const qwen = createOpenAI({
  baseURL: process.env.QWEN_BASE_URL || 'https://dashscope.aliyuncs.com/compatible-mode/v1',
  apiKey: process.env.QWEN_API_KEY || '',
});

// sliding window: 15 requests / minute
interface RateLimitWindow {
  timestamp: number;
  count: number;
}
const rateLimitMap = new Map<string, RateLimitWindow>();

function isRateLimited(ip: string): boolean {
  const now = Date.now();
  const windowMs = 60 * 1000;
  const limit = 15;

  const currentWindow = rateLimitMap.get(ip);
  if (!currentWindow) {
    rateLimitMap.set(ip, { timestamp: now, count: 1 });
    return false;
  }

  if (now - currentWindow.timestamp > windowMs) {
    rateLimitMap.set(ip, { timestamp: now, count: 1 });
    return false;
  }

  if (currentWindow.count >= limit) {
    return true;
  }

  currentWindow.count++;
  return false;
}

// Convert client-side message structure to Vercel AI SDK CoreMessage structure
function formatMessages(messages: any[]): any[] {
  // Find all tool call IDs that actually have a matching tool result in the history
  const respondedToolCallIds = new Set<string>();
  messages.forEach(msg => {
    if (msg.role === 'tool' && Array.isArray(msg.content)) {
      msg.content.forEach((tr: any) => {
        const id = tr.toolCallId || tr.id;
        if (id) respondedToolCallIds.add(id);
      });
    }
  });

  return messages.map(msg => {
    if (msg.role === 'user') {
      return { role: 'user', content: msg.content };
    }
    if (msg.role === 'assistant') {
      // Filter out tool calls that were never responded to by the client
      const validToolCalls = (msg.toolCalls || []).filter((tc: any) => {
        const id = tc.id || tc.toolCallId;
        return respondedToolCallIds.has(id);
      });

      if (validToolCalls.length > 0) {
        const content: any[] = [];
        if (msg.content) {
          content.push({ type: 'text', text: msg.content });
        }
        validToolCalls.forEach((tc: any) => {
          content.push({
            type: 'tool-call',
            toolCallId: tc.id || tc.toolCallId,
            toolName: tc.name || tc.toolName,
            input: tc.args || tc.input
          });
        });
        return { role: 'assistant', content };
      }
      return { role: 'assistant', content: msg.content || "" };
    }
    if (msg.role === 'tool') {
      return {
        role: 'tool',
        content: Array.isArray(msg.content) ? msg.content.map((tr: any) => {
          const rawResult = tr.result !== undefined ? tr.result : tr.output;
          
          let outputObj: any;
          if (rawResult && typeof rawResult === 'object' && 'type' in rawResult && ('value' in rawResult || 'reason' in rawResult)) {
            outputObj = rawResult;
          } else if (typeof rawResult === 'string') {
            outputObj = { type: 'text', value: rawResult };
          } else if (rawResult !== undefined && rawResult !== null) {
            outputObj = { type: 'json', value: rawResult };
          } else {
            outputObj = { type: 'text', value: "No result returned" };
          }

          return {
            type: 'tool-result',
            toolCallId: tr.toolCallId,
            toolName: tr.toolName,
            output: outputObj
          };
        }) : []
      };
    }
    return msg;
  });
}

export async function POST(req: Request) {
  // Extract client IP address for rate limiting
  const ip = req.headers.get('x-forwarded-for') || req.headers.get('x-real-ip') || '127.0.0.1';

  if (isRateLimited(ip)) {
    return new NextResponse(
      JSON.stringify({ error: 'Too many requests. Please try again in a minute.' }),
      { status: 429, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // Ensure user is signed in to use the AI chatbot
  if (!(await isAuthenticated())) {
    return new NextResponse(
      JSON.stringify({ error: 'Sign in required to chat with the AI assistant.' }),
      { status: 401, headers: { 'Content-Type': 'application/json' } }
    );
  }

  let body;
  try {
    body = await req.json();
  } catch {
    return new NextResponse(
      JSON.stringify({ error: 'Invalid JSON request body.' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const { messages } = body;
  if (!messages || !Array.isArray(messages) || messages.length === 0) {
    return new NextResponse(
      JSON.stringify({ error: 'Messages are required and must be an array.' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const lastMessage = messages[messages.length - 1];
  if (!lastMessage || !lastMessage.content) {
    return new NextResponse(
      JSON.stringify({ error: 'Invalid message structure.' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // Prevent sending massive strings for text/user inputs
  if (lastMessage.role === 'user' || typeof lastMessage.content === 'string') {
    if (typeof lastMessage.content !== 'string') {
      return new NextResponse(
        JSON.stringify({ error: 'Invalid message structure: user content must be a string.' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }
    if (lastMessage.content.length > 4000) {
      return new NextResponse(
        JSON.stringify({ error: 'Message content exceeds the maximum allowed length (4000 characters).' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }
  }

  try {
    const formattedMessages = formatMessages(messages.slice(-4));

    const result = streamText({
      // OpenAI model (commented out for future switch back)
      // model: openai('gpt-4o-mini'),
      // Alibaba Cloud Qwen model
      model: qwen.chat(process.env.QWEN_MODEL || 'qwen-turbo'),

      system: "You are the Study-Hub AI assistant. You help users learn programming, software engineering, and computer science concepts across courses like Python, C++, Data Structures & Algorithms, FastAPI, LangChain, LangGraph, and more. Be helpful, concise, and use markdown for code. Default to short answers; give detailed explanations only when asked. Use the 'searchLocalCourses' tool for course-related questions, and the 'searchWeb' tool for general topics.",
      messages: formattedMessages,
      tools: {
        searchLocalCourses: tool({
          description: "Search local Study-Hub course notes and code files for relevant lessons.",
          inputSchema: z.object({ query: z.string() }),
          execute: async ({ query }) => {
            return await searchLocalCourses(query);
          },
        }),
        searchWeb: tool({
          description: "Search the web using Google for general topics outside Study-Hub.",
          inputSchema: z.object({ query: z.string() }),
        }),
      },
      stopWhen: isStepCount(5),
    });

    // Custom JSONL stream implementation
    const responseStream = new TransformStream();
    const writer = responseStream.writable.getWriter();
    const encoder = new TextEncoder();

    (async () => {
      try {
        for await (const part of result.fullStream) {
          const p = part as any;
          if (p.type === 'text-delta') {
            writer.write(encoder.encode(JSON.stringify({ type: 'text', delta: p.text }) + '\n'));
          } else if (p.type === 'tool-call') {
            writer.write(encoder.encode(JSON.stringify({ 
              type: 'tool-call', 
              id: p.toolCallId, 
              name: p.toolName, 
              args: p.args || p.input 
            }) + '\n'));
          } else if (p.type === 'tool-result') {
            writer.write(encoder.encode(JSON.stringify({ 
              type: 'tool-result', 
              id: p.toolCallId, 
              name: p.toolName, 
              result: p.result !== undefined ? p.result : p.output 
            }) + '\n'));
          }
        }
      } catch (err: any) {
        console.error("Stream writing failed:", err);
        const errMsg = err?.message || "An error occurred during response generation.";
        try {
          writer.write(encoder.encode(JSON.stringify({ type: 'error', error: errMsg }) + '\n'));
        } catch (writeErr) {
          console.error("Failed to write error to stream:", writeErr);
        }
      } finally {
        writer.close();
      }
    })();

    return new NextResponse(responseStream.readable, {
      headers: { 
        'Content-Type': 'application/x-ndjson; charset=utf-8',
        'Cache-Control': 'no-cache, no-transform',
        'Connection': 'keep-alive',
        'X-Accel-Buffering': 'no',
      }
    });
  } catch (error) {
    console.error('Error generating chat response:', error);
    return new NextResponse(
      JSON.stringify({ error: 'An unexpected error occurred. Please try again later.' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}

