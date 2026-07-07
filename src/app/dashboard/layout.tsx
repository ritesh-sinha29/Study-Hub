"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { usePathname } from "next/navigation";
import { SidebarProvider, SidebarInset, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/dashboard/AppSidebar";
import { TopicSidebar } from "@/components/learning/TopicSidebar";
import { getTopicBySlug } from "@/config/learning";
import { Search, Moon, Sun } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useTheme } from "next-themes";

const MIN_WIDTH = 200;
const MAX_WIDTH = 480;
const DEFAULT_WIDTH = 230;
const STORAGE_KEY = "sidebar-width";

function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <Button variant="ghost" size="icon-sm" disabled>
        <Moon className="size-4" />
      </Button>
    );
  }

  return (
    <Button
      variant="ghost"
      size="icon-sm"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="relative"
      aria-label="Toggle theme"
    >
      {theme === "dark" ? (
        <Sun className="size-4" />
      ) : (
        <Moon className="size-4" />
      )}
    </Button>
  );
}

import { HelpSupportDialog } from "@/components/HelpSupportDialog";

function FloatingRoboButton() {
  return (
    <div className="fixed bottom-20 md:bottom-6 right-6 z-50 select-none hover:scale-110 active:scale-95 transition-all duration-300">
      <div
        className="relative flex items-center justify-center w-14 h-14 rounded-full bg-gradient-to-tr from-primary to-primary/80 text-primary-foreground shadow-2xl border border-primary/20 cursor-pointer"
        aria-label="Ask AI Assistant"
      >
        {/* Antenna */}
        <div className="absolute -top-1.5 left-1/2 -translate-x-1/2 w-1 h-3 flex flex-col items-center">
          <div className="w-0.5 h-2 bg-cyan-400" />
          <div className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping absolute -top-1" />
          <div className="w-2 h-2 rounded-full bg-cyan-400 absolute -top-0.5 shadow-[0_0_8px_#22d3ee]" />
        </div>
        
        {/* Robo Head */}
        <div className="w-10 h-8 rounded-xl bg-neutral-900 border border-neutral-700/80 flex flex-col justify-between items-center p-1.5 overflow-hidden relative shadow-[inset_0_1px_3px_rgba(255,255,255,0.1)]">
          {/* Eyes container */}
          <div className="flex gap-2.5 mt-0.5 justify-center items-center w-full">
            {/* Left Eye */}
            <div className="w-2.5 h-2.5 rounded-full bg-neutral-800 border border-neutral-700 flex items-center justify-center relative overflow-hidden">
              <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 absolute animate-eyemove shadow-[0_0_4px_#22d3ee]" />
            </div>
            {/* Right Eye */}
            <div className="w-2.5 h-2.5 rounded-full bg-neutral-800 border border-neutral-700 flex items-center justify-center relative overflow-hidden">
              <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 absolute animate-eyemove shadow-[0_0_4px_#22d3ee]" />
            </div>
          </div>
          {/* Mouth */}
          <div className="w-5 h-0.5 bg-cyan-400/80 rounded-full animate-pulse shadow-[0_0_4px_#22d3ee] mb-0.5" />
        </div>
      </div>

      <style dangerouslySetInnerHTML={{
        __html: `
          @keyframes eyemove {
            0%, 100% { transform: translate(0, 0); }
            15% { transform: translate(-1.5px, 0); }
            30% { transform: translate(1.5px, 0); }
            45% { transform: translate(0, -1px); }
            60% { transform: translate(0, 1px); }
            75% { transform: translate(1px, -0.5px); }
          }
          .animate-eyemove {
            animation: eyemove 4s infinite ease-in-out;
          }
        `
      }} />
    </div>
  );
}

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [sidebarWidth, setSidebarWidth] = useState(DEFAULT_WIDTH);
  const providerRef = useRef<HTMLDivElement>(null);
  const isDragging = useRef(false);
  const startX = useRef(0);
  const startWidth = useRef(DEFAULT_WIDTH);
  const currentWidth = useRef(DEFAULT_WIDTH);
  const rafId = useRef<number>(0);

  // Load persisted width
  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      const parsed = parseInt(saved, 10);
      if (!isNaN(parsed) && parsed >= MIN_WIDTH && parsed <= MAX_WIDTH) {
        setSidebarWidth(parsed);
        currentWidth.current = parsed;
        startWidth.current = parsed;
      }
    }
  }, []);

  const onMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    isDragging.current = true;
    startX.current = e.clientX;
    startWidth.current = currentWidth.current;
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";
  }, []);

  useEffect(() => {
    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging.current) return;
      cancelAnimationFrame(rafId.current);
      rafId.current = requestAnimationFrame(() => {
        const delta = e.clientX - startX.current;
        const newWidth = Math.min(MAX_WIDTH, Math.max(MIN_WIDTH, startWidth.current + delta));
        currentWidth.current = newWidth;
        // Directly mutate CSS var — no React re-render
        providerRef.current?.style.setProperty("--sidebar-width", `${newWidth}px`);
      });
    };

    const onMouseUp = () => {
      if (!isDragging.current) return;
      isDragging.current = false;
      cancelAnimationFrame(rafId.current);
      document.body.style.cursor = "";
      document.body.style.userSelect = "";
      // Sync React state only once on release
      setSidebarWidth(currentWidth.current);
      localStorage.setItem(STORAGE_KEY, String(currentWidth.current));
    };

    window.addEventListener("mousemove", onMouseMove, { passive: true });
    window.addEventListener("mouseup", onMouseUp);
    return () => {
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
    };
  }, []); // ← empty deps: registers once, never re-registers

  // Detect if we're on a learning topic page like /dashboard/python-learning/...
  const match = pathname.match(/^\/dashboard\/([^/]+)/);
  const topicSlug = match?.[1];
  const topic = topicSlug ? getTopicBySlug(topicSlug) : undefined;

  return (
    <div
      ref={providerRef}
      style={{ "--sidebar-width": `${sidebarWidth}px` } as React.CSSProperties}
      className="flex h-svh w-full overflow-hidden"
    >
    <SidebarProvider
      style={{ "--sidebar-width": "inherit" } as React.CSSProperties}
      className="h-full overflow-hidden"
    >
      {/* Swap sidebar based on route */}
      {topic ? <TopicSidebar topic={topic} /> : <AppSidebar />}

      {/* Drag handle */}
      <div
        onMouseDown={onMouseDown}
        className="relative z-50 w-1 cursor-col-resize shrink-0 group"
        title="Drag to resize"
      >
        <div className="absolute inset-y-0 -left-px w-px bg-transparent group-hover:bg-neutral-400 dark:group-hover:bg-neutral-500 transition-colors duration-150" />
        {/* Wider invisible grab area */}
        <div className="absolute inset-y-0 -left-2 -right-2" />
      </div>

      <SidebarInset className="h-full overflow-y-auto">
        <header className="flex h-16 shrink-0 items-center border-b border-border bg-background/80 backdrop-blur-md px-4 sticky top-0 z-50 gap-2">
          <SidebarTrigger className="-ml-1 md:hidden" />
          <div className="flex items-center gap-3 ml-auto">
            <div className="relative hidden sm:flex items-center">
              <Search className="absolute left-2.5 size-4 text-muted-foreground" />
              <Input
                placeholder="Search..."
                className="h-9 w-56 bg-muted/50 pl-8 border-none focus-visible:ring-1"
              />
            </div>
            <ThemeToggle />
          </div>
        </header>
        <div className="flex flex-1 flex-col">
          {children}
        </div>
        {/* Floating Chat Trigger */}
        <HelpSupportDialog trigger={<FloatingRoboButton />} />
      </SidebarInset>
    </SidebarProvider>
    </div>
  );
}


