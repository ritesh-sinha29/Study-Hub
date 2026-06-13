"use client";

import { usePathname } from "next/navigation";
import { SidebarProvider, SidebarTrigger, SidebarInset } from "@/components/ui/sidebar";
import { Separator } from "@/components/ui/separator";
import { AppSidebar } from "@/components/dashboard/AppSidebar";
import { TopicSidebar } from "@/components/learning/TopicSidebar";
import { getTopicBySlug } from "@/config/learning";
import Link from "next/link";
import { Bell, Search } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

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
            <Button variant="ghost" size="icon-sm" className="relative">
              <Bell className="size-4" />
              <span className="absolute top-1.5 right-1.5 size-2 rounded-full bg-primary" />
            </Button>
            <Separator orientation="vertical" className="h-6" />
            <Link
              href="/"
              className="flex items-center gap-2 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
            >
              <div className="flex size-7 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">
                U
              </div>
              <span className="hidden sm:inline">User</span>
            </Link>
          </div>
        </header>
        <div className="flex flex-1 flex-col">
          {children}
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
