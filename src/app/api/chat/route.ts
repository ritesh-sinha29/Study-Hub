import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { streamText, tool } from 'ai';
import { NextResponse } from 'next/server';
import { z } from 'zod';
import { searchLocalCourses } from '@/lib/knowledge-base';

// Allow streaming responses up to 30 seconds
export const maxDuration = 30;

const google = createGoogleGenerativeAI({
  apiKey: process.env.GOOGLE_API_KEY || '',
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
  return messages.map(msg => {
    if (msg.role === 'user') {
      return { role: 'user', content: msg.content };
    }
    if (msg.role === 'assistant') {
      const formatted: any = { role: 'assistant', content: msg.content || "" };
      if (msg.toolCalls && msg.toolCalls.length > 0) {
        formatted.toolCalls = msg.toolCalls.map((tc: any) => ({
          type: 'tool-call',
          toolCallId: tc.id,
          toolName: tc.name,
          args: tc.args
        }));
      }
      return formatted;
    }
    if (msg.role === 'tool') {
      return {
        role: 'tool',
        content: Array.isArray(msg.content) ? msg.content.map((tr: any) => ({
          type: 'tool-result',
          toolCallId: tr.toolCallId,
          toolName: tr.toolName,
          result: tr.result
        })) : []
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
  if (!lastMessage || !lastMessage.content || typeof lastMessage.content !== 'string') {
    return new NextResponse(
      JSON.stringify({ error: 'Invalid message structure.' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  // Prevent sending massive strings
  if (lastMessage.content.length > 4000) {
    return new NextResponse(
      JSON.stringify({ error: 'Message content exceeds the maximum allowed length (4000 characters).' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  try {
    const formattedMessages = formatMessages(messages);

    const result = streamText({
      model: google('gemini-2.5-flash'),
      system: "You are the Study-Hub AI assistant. You help users learn programming, software engineering, and computer science concepts across all available courses (such as Python, C++, Data Structures & Algorithms, FastAPI, LangChain, LangGraph, and more), and help them navigate the Study-Hub platform. Be encouraging, concise, and informative. Use markdown formatting for code snippets. If you need details about course content, use the 'searchLocalCourses' tool. If the user asks general questions outside of local courses, use the 'searchWeb' tool.",
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
          execute: async ({ query }) => {
            return `Simulated search results for: "${query}"`;
          },
        }),
      },
      maxSteps: 5,
    } as any);

    // Custom JSONL stream implementation
    const responseStream = new TransformStream();
    const writer = responseStream.writable.getWriter();
    const encoder = new TextEncoder();

    (async () => {
      try {
        for await (const part of result.fullStream) {
          const p = part as any;
          if (p.type === 'text-delta') {
            writer.write(encoder.encode(JSON.stringify({ type: 'text', delta: p.textDelta }) + '\n'));
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
              result: p.result 
            }) + '\n'));
          }
        }
      } catch (err) {
        console.error("Stream writing failed:", err);
      } finally {
        writer.close();
      }
    })();

    return new NextResponse(responseStream.readable, {
      headers: { 'Content-Type': 'application/x-ndjson' }
    });
  } catch (error) {
    console.error('Error generating chat response:', error);
    return new NextResponse(
      JSON.stringify({ error: 'An unexpected error occurred. Please try again later.' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}

