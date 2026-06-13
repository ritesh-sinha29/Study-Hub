"use client";

import Link from "next/link";
import { useState } from "react";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Menu, X } from "lucide-react";


export function Header() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <div className="flex size-8 items-center justify-center rounded-lg bg-primary text-sm font-bold text-primary-foreground">
            S
          </div>
          <span className="text-lg font-semibold tracking-tight">Study Hub</span>
        </Link>

        {/* Desktop CTA */}
        <div className="hidden items-center gap-3 md:flex">
          <Link
            href="/dashboard"
            className={cn(buttonVariants({ size: "sm" }))}
          >
            Start Learning
          </Link>
        </div>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex size-9 items-center justify-center rounded-lg md:hidden hover:bg-muted"
          aria-label={isOpen ? "Close menu" : "Open menu"}
        >
          {isOpen ? <X className="size-5" /> : <Menu className="size-5" />}
        </button>
      </div>

      {/* Mobile Nav */}
      <div
        className={cn(
          "overflow-hidden border-t border-border/40 transition-all duration-200 md:hidden",
          isOpen ? "max-h-80" : "max-h-0"
        )}
      >
        <nav className="flex flex-col gap-1 px-4 py-4">
          <hr className="my-2 border-border/40" />
          <Link
            href="/dashboard"
            onClick={() => setIsOpen(false)}
            className={cn(buttonVariants({ size: "default" }), "mt-1 w-full")}
          >
            Start Learning
          </Link>
        </nav>
      </div>
    </header>
  );
}
