"use client";

import { useState } from "react";
import { Check, Copy } from "lucide-react";

export function CopyButton({ text, inline }: { text: string; inline?: boolean }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (inline) {
    return (
      <button
        onClick={handleCopy}
        className="flex items-center gap-1.5 rounded px-2 py-1 text-xs font-medium text-muted-foreground/70 hover:text-foreground hover:bg-muted/50 transition-all cursor-pointer"
        aria-label="Copy code"
      >
        {copied ? (
          <>
            <Check className="size-3 text-green-500 animate-in fade-in duration-200" />
            <span className="text-green-500 text-[10px] uppercase tracking-wider font-semibold">Copied</span>
          </>
        ) : (
          <>
            <Copy className="size-3" />
            <span className="text-[10px] uppercase tracking-wider font-semibold">Copy</span>
          </>
        )}
      </button>
    );
  }

  return (
    <button
      onClick={handleCopy}
      className="absolute right-3 top-3 flex size-7 items-center justify-center rounded-md border border-border/20 bg-[#0d0d15] text-muted-foreground/50 opacity-0 transition-all hover:border-border/40 hover:text-muted-foreground group-hover:opacity-100 cursor-pointer shadow-md"
      aria-label="Copy code"
    >
      {copied ? (
        <Check className="size-3.5 text-green-500 animate-in fade-in duration-200" />
      ) : (
        <Copy className="size-3.5" />
      )}
    </button>
  );
}

