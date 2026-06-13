"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { usePathname } from "next/navigation";
import { SidebarProvider, SidebarTrigger, SidebarInset } from "@/components/ui/sidebar";
import { Separator } from "@/components/ui/separator";
import { AppSidebar } from "@/components/dashboard/AppSidebar";
import { TopicSidebar } from "@/components/learning/TopicSidebar";
import { getTopicBySlug } from "@/config/learning";
import { Search, Moon, Sun } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useTheme } from "next-themes";

const MIN_WIDTH = 200;
const MAX_WIDTH = 480;
const DEFAULT_WIDTH = 280;
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

  // Detect if we're on a learning topic page like /dashboard/learning/python-learning/...
  const match = pathname.match(/^\/dashboard\/learning\/([^/]+)/);
  const topicSlug = match?.[1];
  const topic = topicSlug ? getTopicBySlug(topicSlug) : undefined;

  return (
    <div
      ref={providerRef}
      style={{ "--sidebar-width": `${sidebarWidth}px` } as React.CSSProperties}
      className="flex h-svh w-full overflow-hidden"
    >
    <SidebarProvider style={{ "--sidebar-width": "inherit" } as React.CSSProperties}>
      {/* Swap sidebar based on route */}
      {topic ? <TopicSidebar topic={topic} /> : <AppSidebar />}

      {/* Drag handle */}
      <div
        onMouseDown={onMouseDown}
        className="relative z-50 w-1 cursor-col-resize shrink-0 group"
        title="Drag to resize"
      >
        <div className="absolute inset-y-0 -left-1 -right-1 group-hover:bg-primary/30 transition-colors duration-150" />
      </div>

      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b border-border/40 bg-background/80 backdrop-blur-md px-4 sticky top-0 z-50">
          <div className="flex items-center gap-2 flex-1">
            <SidebarTrigger className="-ml-1" />
            <Separator orientation="vertical" className="h-6 mr-2" />
            <div className="relative hidden sm:flex items-center flex-1 max-w-sm">
              <Search className="absolute left-2.5 size-4 text-muted-foreground" />
              <Input
                placeholder="Search..."
                className="h-9 w-full bg-muted/50 pl-8 border-none focus-visible:ring-1"
              />
            </div>
          </div>
          <div className="flex items-center gap-2">
            <ThemeToggle />
          </div>
        </header>
        <div className="flex flex-1 flex-col">
          {children}
        </div>
      </SidebarInset>
    </SidebarProvider>
    </div>
  );
}


