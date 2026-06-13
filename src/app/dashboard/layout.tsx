"use client";

import { useState, useEffect } from "react";
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

  // Detect if we're on a learning topic page like /dashboard/learning/python-learning/...
  const match = pathname.match(/^\/dashboard\/learning\/([^/]+)/);
  const topicSlug = match?.[1];
  const topic = topicSlug ? getTopicBySlug(topicSlug) : undefined;

  return (
    <SidebarProvider>
      {/* Swap sidebar based on route: AppSidebar for main dashboard, TopicSidebar for learning topics */}
      {topic ? <TopicSidebar topic={topic} /> : <AppSidebar />}

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
  );
}
