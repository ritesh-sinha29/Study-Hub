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
        className="flex items-center gap-1.5 rounded px-2 py-1 text-xs font-medium text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/60 transition-all cursor-pointer"
        aria-label="Copy code"
      >
        {copied ? (
          <>
            <Check className="size-3 text-emerald-400 animate-in fade-in duration-200" />
            <span className="text-emerald-400 text-[10px] uppercase tracking-wider font-semibold">Copied</span>
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
      className="absolute right-3 top-3 flex size-7 items-center justify-center rounded-md border border-zinc-800 bg-[#252526] text-zinc-400 opacity-0 transition-all hover:border-zinc-700 hover:text-zinc-100 group-hover:opacity-100 cursor-pointer shadow-md"
      aria-label="Copy code"
    >
      {copied ? (
        <Check className="size-3.5 text-emerald-400 animate-in fade-in duration-200" />
      ) : (
        <Copy className="size-3.5" />
      )}
    </button>
  );
}

