import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { streamText } from 'ai';
import { NextResponse } from 'next/server';

// Allow streaming responses up to 30 seconds
export const maxDuration = 30;

const google = createGoogleGenerativeAI({
  apiKey: process.env.GOOGLE_API_KEY || process.env.GOOGLE_GENERATIVE_AI_API_KEY,
});

// Simple in-memory rate limiter map
const rateLimitMap = new Map<string, { count: number; resetTime: number }>();
const RATE_LIMIT_WINDOW = 60 * 1000; // 1 minute
const MAX_REQUESTS_PER_MINUTE = 15;   // Limit to 5 requests per minute

function checkRateLimit(ip: string): boolean {
  const now = Date.now();

  // Prune map size if it grows too large (prevent memory leak)
  if (rateLimitMap.size > 2000) {
    for (const [key, data] of rateLimitMap.entries()) {
      if (now > data.resetTime) {
        rateLimitMap.delete(key);
      }
    }
  }

  const limitData = rateLimitMap.get(ip);

  if (!limitData) {
    rateLimitMap.set(ip, { count: 1, resetTime: now + RATE_LIMIT_WINDOW });
    return false;
  }

  if (now > limitData.resetTime) {
    rateLimitMap.set(ip, { count: 1, resetTime: now + RATE_LIMIT_WINDOW });
    return false;
  }

  limitData.count++;
  if (limitData.count > MAX_REQUESTS_PER_MINUTE) {
    return true;
  }

  return false;
}

export async function POST(req: Request) {
  // Get IP address from headers
  const ip = req.headers.get('x-forwarded-for') || req.headers.get('x-real-ip') || '127.0.0.1';

  // Apply rate limiting
  if (checkRateLimit(ip)) {
    return new NextResponse(
      JSON.stringify({ error: 'Too many requests. Please try again in a minute.' }),
      { status: 429, headers: { 'Content-Type': 'application/json' } }
    );
  }

  let body;
  try {
    body = await req.json();
  } catch {
    return new NextResponse(JSON.stringify({ error: 'Invalid JSON body.' }), { status: 400 });
  }

  const { messages } = body;

  // Validate message payload structure
  if (!Array.isArray(messages) || messages.length === 0) {
    return new NextResponse(
      JSON.stringify({ error: 'Invalid request: Messages are required.' }),
      { status: 400 }
    );
  }

  // Prevent sending massive chat history histories to inflate token usage
  if (messages.length > 50) {
    return new NextResponse(
      JSON.stringify({ error: 'Chat history limit exceeded.' }),
      { status: 400 }
    );
  }

  // Validate the content of the last message
  const lastMessage = messages[messages.length - 1];
  if (!lastMessage || typeof lastMessage.content !== 'string') {
    return new NextResponse(
      JSON.stringify({ error: 'Invalid message structure.' }),
      { status: 400 }
    );
  }

  // Prevent sending massive strings (e.g. prompt injection, file dumps)
  if (lastMessage.content.length > 4000) {
    return new NextResponse(
      JSON.stringify({ error: 'Message content exceeds the maximum allowed length (4000 characters).' }),
      { status: 400 }
    );
  }

  try {
    const result = streamText({
      model: google('gemini-2.5-pro'),
      system: "You are the Study-Hub AI assistant. You help users learn programming, software engineering, and computer science concepts across all available courses (such as Python, C++, Data Structures & Algorithms, FastAPI, LangChain, LangGraph, and more), and help them navigate the Study-Hub platform. Be encouraging, concise, and informative. Use markdown formatting for code snippets.",
      messages,
    });

    return result.toTextStreamResponse();
  } catch (error) {
    console.error('Error generating chat response:', error);
    return new NextResponse(
      JSON.stringify({ error: 'An unexpected error occurred. Please try again later.' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}

