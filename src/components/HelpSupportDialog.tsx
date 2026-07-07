"use client";

import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  HelpCircleIcon,
  Send,
  User,
  Trash2,
  Square,
  ChevronRight,
  Loader2,
  Check
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

export const AIAssistantIcon = ({ className }: { className?: string }) => (
  <svg
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <defs>
      <linearGradient id="aiIconGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#3b82f6" />
        <stop offset="100%" stopColor="#8b5cf6" />
      </linearGradient>
    </defs>
    <path
      d="M12 3L14.5 8.5L20 11L14.5 13.5L12 19L9.5 13.5L4 11L9.5 8.5L12 3Z"
      fill="url(#aiIconGrad)"
    />
    <path
      d="M19 3L20 5.5L22.5 6.5L20 7.5L19 10L18 7.5L15.5 6.5L18 5.5L19 3Z"
      fill="url(#aiIconGrad)"
      opacity="0.7"
    />
    <path
      d="M5 15L6 17.5L8.5 18.5L6 19.5L5 22L4 17.5L1.5 18.5L4 17.5L5 15Z"
      fill="url(#aiIconGrad)"
      opacity="0.7"
    />
  </svg>
);

interface HelpSupportDialogProps {
  trigger?: React.ReactNode;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
}

export function HelpSupportDialog({ trigger, open, onOpenChange }: HelpSupportDialogProps) {
  const [internalOpen, setInternalOpen] = useState(false);
  const isOpen = open !== undefined ? open : internalOpen;
  const setIsOpen = onOpenChange !== undefined ? onOpenChange : setInternalOpen;

  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [toolDecisions, setToolDecisions] = useState<Record<string, "approved" | "denied">>({});

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const sendChatRequest = async (currentMessages: any[]) => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: currentMessages }),
      });

      if (!res.ok) {
        let errMsg = "Failed to fetch response";
        try {
          const errData = await res.json();
          errMsg = errData.error || errMsg;
        } catch {}
        throw new Error(errMsg);
      }
      if (!res.body) throw new Error("No response body");

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let assistantMsg = { role: "assistant", content: "", toolCalls: [] as any[], toolResults: [] as any[] };
      
      setMessages([...currentMessages, assistantMsg]);

      let buffer = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const data = JSON.parse(line);
            if (data.type === "text") {
              assistantMsg.content += data.delta;
              setMessages([...currentMessages, { ...assistantMsg }]);
            } else if (data.type === "tool-call") {
              assistantMsg.toolCalls = assistantMsg.toolCalls || [];
              if (!assistantMsg.toolCalls.some((tc: any) => tc.id === data.id)) {
                assistantMsg.toolCalls.push(data);
              }
              setMessages([...currentMessages, { ...assistantMsg }]);
            } else if (data.type === "tool-result") {
              assistantMsg.toolResults = assistantMsg.toolResults || [];
              if (!assistantMsg.toolResults.some((tr: any) => tr.id === data.id)) {
                assistantMsg.toolResults.push(data);
              }
              setMessages([...currentMessages, { ...assistantMsg }]);
            } else if (data.type === "error") {
              assistantMsg.content += `⚠️ **Error:** ${data.error}`;
              setMessages([...currentMessages, { ...assistantMsg }]);
            }
          } catch {
            // Fallback for raw text lines
            assistantMsg.content += line;
            setMessages([...currentMessages, { ...assistantMsg }]);
          }
        }
      }
    } catch (error: any) {
      console.error("Chat error:", error);
      const msg = error?.message || "Something went wrong. Please try again.";
      setMessages([...currentMessages, { role: "assistant", content: `⚠️ ${msg}` }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    await sendChatRequest(newMessages);
  };

  const handleToolApproval = async (msgIdx: number, toolCall: any, approved: boolean) => {
    if (isLoading) return;
    
    // Set decision state
    setToolDecisions(prev => ({ ...prev, [toolCall.id]: approved ? "approved" : "denied" }));
    setIsLoading(true);

    let searchResult = "User denied web search access. Please answer based on your internal knowledge.";
    
    if (approved) {
      try {
        const searchRes = await fetch(`/api/search?query=${encodeURIComponent(toolCall.args.query)}`);
        if (searchRes.ok) {
          const searchData = await searchRes.json();
          searchResult = searchData.result || "No search results returned.";
        } else {
          searchResult = "Web search failed to execute.";
        }
      } catch (err) {
        console.error("Search API error:", err);
        searchResult = "Error performing web search.";
      }
    }

    // Build history up to and including the assistant message that made this tool call.
    // We must NOT include the empty streaming assistant bubble appended by sendChatRequest.
    const historyUpToToolCall = messages.slice(0, msgIdx + 1);

    // Add tool response message
    const updatedMessages = [
      ...historyUpToToolCall,
      {
        role: "tool",
        content: [
          {
            type: "tool-result",
            toolCallId: toolCall.id,
            toolName: toolCall.name,
            result: searchResult
          }
        ]
      }
    ];

    setMessages(updatedMessages);
    await sendChatRequest(updatedMessages);
  };

  const clear = () => {
    setMessages([]);
    setToolDecisions({});
  };

  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTo({
        top: scrollContainerRef.current.scrollHeight,
        behavior: isLoading ? "auto" : "smooth",
      });
    }
  }, [messages, isLoading]);

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      {trigger && <div className="w-full cursor-pointer" onClick={() => setIsOpen(true)}>{trigger}</div>}
      <DialogContent className="sm:max-w-[580px] p-4 rounded-xl h-[560px] flex flex-col overflow-hidden bg-background border border-border shadow-2xl animate-in fade-in-50 zoom-in-95 duration-200">
        <style dangerouslySetInnerHTML={{
          __html: `
          @keyframes chatbot-shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
          }
          .text-shimmer {
            background: linear-gradient(90deg, #71717a 25%, #f4f4f5 50%, #71717a 75%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: chatbot-shimmer 2.2s infinite linear;
            display: inline-flex;
            align-items: center;
          }
        `}} />
        <DialogHeader className="mb-4">
          <DialogTitle className="text-base font-semibold text-foreground flex items-center gap-2">
            <AIAssistantIcon className="h-5 w-5 shrink-0" />
            AI Help & Support
          </DialogTitle>
          <div className="flex items-center text-xs text-muted-foreground justify-between">
            <p>Consult the Study-Hub AI assistant for instant answers.</p>
          </div>
        </DialogHeader>

        <div className="w-full -mt-1.5 flex-1 flex flex-col min-h-0 focus:outline-none justify-between">
          <div
            ref={scrollContainerRef}
            className="flex-1 overflow-y-auto pr-1 mb-3 space-y-3 min-h-0 select-none scrollbar-thin scrollbar-thumb-muted-foreground/20 scrollbar-track-transparent"
          >
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center p-4 space-y-4 select-none">
                <AIAssistantIcon className="h-9 w-9" />
                <div className="space-y-1">
                  <h4 className="text-base font-medium text-foreground">Study-Hub AI Assistant</h4>
                </div>
                <div className="flex flex-col gap-2 w-full max-w-[400px] pt-1">
                  {[
                    { label: "Ask anything about Study-Hub", query: "Help me get started and explain what I can do here." },
                    { label: "Find course materials", query: "Where can I find the Python fundamentals course?" },
                    { label: "Ask technical questions", query: "Can you explain what immutable means in Python?" },
                    { label: "Know more features", query: "Tell me more about the platform's features." }
                  ].map((item, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => setInput(item.query)}
                      className="flex items-center justify-between px-4 py-2.5 bg-muted/30 hover:bg-muted/60 border border-border/80 rounded-xl text-xs text-muted-foreground transition-all duration-200 cursor-pointer group hover:border-border"
                    >
                      <span className="font-medium text-foreground/80 group-hover:text-foreground transition-colors">{item.label}</span>
                      <ChevronRight className="w-3.5 h-3.5 text-muted-foreground group-hover:text-foreground/80 transition-colors" />
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="space-y-3 text-left animate-in fade-in-50 duration-200">
                {messages.map((msg, idx) => {
                  if (msg.role === "tool") {
                    const isApproved = msg.content?.[0]?.result && !msg.content[0].result.includes("denied");
                    return (
                      <div key={idx} className="flex justify-start pl-7 text-[10px] text-muted-foreground items-center gap-1.5 py-1">
                        <AIAssistantIcon className="size-3.5 opacity-70 animate-pulse text-indigo-500" />
                        <span>
                          {isApproved 
                            ? `Searched the web for: "${msg.content[0].toolName}"` 
                            : "Web search cancelled"}
                        </span>
                      </div>
                    );
                  }

                  const isUser = msg.role === "user";
                  return (
                    <div
                      key={idx}
                      className={cn(
                        "flex w-full gap-2",
                        isUser ? "justify-end" : "justify-start"
                      )}
                    >
                      {!isUser && (
                        <AIAssistantIcon className="h-5 w-5 shrink-0 mt-0.5 text-primary" />
                      )}
                      <div
                        className={cn(
                          "max-w-[75%] rounded-2xl p-2 text-[11px] leading-relaxed break-words",
                          isUser
                            ? "bg-primary text-primary-foreground rounded-tr-none shadow-md"
                            : "bg-muted/40 border border-border/80 text-foreground rounded-tl-none"
                        )}
                      >
                        {msg.content ? (
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            components={{
                              p: ({ children }) => <p className="mb-1.5 last:mb-0 leading-relaxed">{children}</p>,
                              ul: ({ children }) => <ul className="list-disc pl-4 mb-2 space-y-1">{children}</ul>,
                              ol: ({ children }) => <ol className="list-decimal pl-4 mb-2 space-y-1">{children}</ol>,
                              li: ({ children }) => <li className="leading-relaxed">{children}</li>,
                              strong: ({ children }) => <strong className="font-semibold text-foreground">{children}</strong>,
                              a: ({ href, children }) => (
                                <a href={href} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                                  {children}
                                </a>
                              ),
                              code: ({ className, children, ...props }: any) => {
                                const isInline = !className;
                                return isInline ? (
                                  <code className="bg-muted px-1 py-0.5 rounded text-[10px] font-mono text-foreground">{children}</code>
                                ) : (
                                  <pre className="bg-muted p-2 rounded-lg my-1.5 overflow-x-auto text-[10px] font-mono border border-border text-muted-foreground">
                                    <code {...props}>{children}</code>
                                  </pre>
                                );
                              }
                            }}
                          >
                            {msg.content}
                          </ReactMarkdown>
                        ) : isLoading && msg.role !== "user" && !msg.content ? (
                          <span className="flex items-center gap-1.5 font-medium text-shimmer">
                            Assistant is thinking...
                          </span>
                        ) : null}

                        {/* Interactive Tool Approval Request Panel & Status Indicators */}
                        {msg.toolCalls?.map((tc: any) => {
                          const queryText = tc.args?.query || tc.input?.query || "";
                          
                          if (tc.name === "searchLocalCourses") {
                            const isCompleted = msg.toolResults?.some((tr: any) => tr.id === tc.id);
                            return (
                              <div key={tc.id} className="mt-2 p-2 rounded-xl border border-border bg-muted/20 text-[10px] flex items-center gap-2">
                                {isCompleted ? (
                                  <>
                                    <Check className="size-3.5 text-green-500 shrink-0" />
                                    <span className="text-muted-foreground">Searched local course materials: "{queryText}"</span>
                                  </>
                                ) : (
                                  <>
                                    <Loader2 className="size-3.5 animate-spin text-primary shrink-0" />
                                    <span className="text-foreground font-medium">Searching local course materials: "{queryText}"...</span>
                                  </>
                                )}
                              </div>
                            );
                          }

                          if (tc.name === "searchWeb") {
                            const decision = toolDecisions[tc.id];
                            if (!decision) {
                              return (
                                <div key={tc.id} className="mt-2 p-2 rounded-xl border border-indigo-150 dark:border-indigo-900/60 bg-indigo-50/40 dark:bg-indigo-950/20 text-[10px] space-y-2">
                                  <div className="flex items-center gap-1.5 text-indigo-700 dark:text-indigo-400 font-semibold">
                                    <AIAssistantIcon className="size-3.5" />
                                    <span>Web Search: "{queryText}"</span>
                                  </div>
                                  <p className="text-muted-foreground leading-normal">
                                    I need to search the web to retrieve this information.
                                  </p>
                                  <div className="flex gap-1.5 pt-0.5">
                                    <Button
                                      size="sm"
                                      type="button"
                                      onClick={() => handleToolApproval(idx, tc, true)}
                                      className="h-6 px-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md text-[9.5px] cursor-pointer"
                                    >
                                      Approve Search
                                    </Button>
                                    <Button
                                      size="sm"
                                      type="button"
                                      variant="outline"
                                      onClick={() => handleToolApproval(idx, tc, false)}
                                      className="h-6 px-2.5 text-[9.5px] rounded-md border-indigo-200 hover:bg-indigo-50/50 dark:border-indigo-900 cursor-pointer text-foreground"
                                    >
                                      Deny
                                    </Button>
                                  </div>
                                </div>
                              );
                            } else {
                              return (
                                <div key={tc.id} className="mt-2 text-[9.5px] text-muted-foreground italic flex items-center gap-1">
                                  <span>
                                    {decision === "approved" 
                                      ? `✓ Web search approved ("${queryText}")`
                                      : `✗ Web search denied`
                                    }
                                  </span>
                                </div>
                              );
                            }
                          }
                          return null;
                        })}
                      </div>
                      {isUser && (
                        <Avatar className="h-6 w-6 border border-border shrink-0 mt-0.5">
                          <AvatarFallback className="text-[9px] font-semibold bg-muted text-muted-foreground flex items-center justify-center">
                            <User className="h-3 w-3 text-muted-foreground" />
                          </AvatarFallback>
                        </Avatar>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          <form
            onSubmit={handleSubmit}
            className="relative flex items-center gap-1.5 bg-background border border-border rounded-md p-1 focus-within:border-primary/50"
          >
            {messages.length > 0 && (
              <Button
                type="button"
                onClick={clear}
                variant="ghost"
                size="icon"
                className="h-7 w-7 text-muted-foreground hover:text-foreground hover:bg-muted/40 rounded-md shrink-0 flex items-center justify-center cursor-pointer transition-colors"
                title="Clear chat history"
              >
                <Trash2 className="h-3.5 w-3.5" />
              </Button>
            )}
            <Input
              type="text"
              placeholder="Ask assistant anything..."
              value={input}
              onChange={handleInputChange}
              disabled={isLoading}
              className="bg-transparent! border-none! text-foreground placeholder:text-muted-foreground h-8 text-xs focus-visible:ring-0! flex-1 outline-none pr-2"
            />
            {isLoading ? (
              <Button
                type="button"
                onClick={() => {}}
                size="icon"
                className="h-7 w-7 bg-destructive/10 hover:bg-destructive/20 text-destructive border border-destructive/20 rounded-md shrink-0 flex items-center justify-center cursor-pointer transition-colors"
                title="Stop generating"
              >
                <Square className="h-3 w-3 fill-destructive" />
              </Button>
            ) : (
              <Button
                type="submit"
                size="icon"
                disabled={!input.trim()}
                className="h-7 w-7 bg-primary hover:bg-primary/90 text-primary-foreground rounded-md shrink-0 flex items-center justify-center cursor-pointer disabled:bg-muted disabled:text-muted-foreground disabled:cursor-not-allowed transition-colors"
                title="Send message"
              >
                <Send className="h-3.5 w-3.5" />
              </Button>
            )}
          </form>
        </div>
      </DialogContent>
    </Dialog>
  );
}
