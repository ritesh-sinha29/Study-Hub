"use client";

import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import type { Heading } from "@/lib/extract-headings";

interface TableOfContentsProps {
  headings: Heading[];
}

export function TableOfContents({ headings }: TableOfContentsProps) {
  const [activeId, setActiveId] = useState<string>("");

  useEffect(() => {
    if (headings.length === 0) return;

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        }
      },
      { rootMargin: "-80px 0px -80% 0px" }
    );

    for (const heading of headings) {
      const el = document.getElementById(heading.id);
      if (el) observer.observe(el);
    }

    return () => observer.disconnect();
  }, [headings]);

  if (headings.length === 0) return null;

  return (
    <nav className="sticky top-24 w-56 shrink-0 hidden xl:block">
      <div className="pl-4 border-l border-border/40">
        <p className="mb-3 text-[11px] font-bold uppercase tracking-wider text-muted-foreground/60">
          On this page
        </p>
        <ul className="space-y-1">
          {headings.map((heading) => (
            <li key={heading.id} className="relative">
              <a
                href={`#${heading.id}`}
                className={cn(
                  "block text-[13px] py-1 border-l-2 transition-all hover:text-foreground duration-200 -ml-[17px]",
                  activeId === heading.id
                    ? "border-primary text-foreground font-medium"
                    : "border-transparent text-muted-foreground/80",
                  heading.level === 3 ? "pl-8" : "pl-4"
                )}
              >
                {heading.text}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );

}
