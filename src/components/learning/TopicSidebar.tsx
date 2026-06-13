"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
} from "@/components/ui/sidebar";
import { ChevronLeft, FileText } from "lucide-react";
import { type TopicItem } from "@/config/learning";

export function TopicSidebar({ topic }: { topic: TopicItem }) {
  const pathname = usePathname();

  return (
    <Sidebar collapsible="icon" variant="sidebar">
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="lg"
              render={<Link href="/dashboard/learning" />}
            >
              <div className="flex size-8 items-center justify-center rounded-lg bg-primary text-sm font-bold text-primary-foreground">
                L
              </div>
              <div className="flex flex-col gap-0.5 leading-none">
                <span className="font-semibold text-sm">{topic.title}</span>
                <span className="text-xs text-muted-foreground">
                  {topic.files.length} files
                </span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="sm"
              render={<Link href="/dashboard/learning" />}
            >
              <ChevronLeft className="size-4" />
              <span>All topics</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      <SidebarContent>
        <SidebarMenu>
          {topic.files.length === 0 ? (
            <div className="px-3 py-8 text-center">
              <FileText className="size-8 mx-auto text-muted-foreground/40" />
              <p className="mt-2 text-sm text-muted-foreground">
                No notes yet
              </p>
            </div>
          ) : (
            topic.files.map((file) => {
              const href = `/dashboard/learning/${topic.slug}/${file.slug}`;
              const isActive = pathname === href;
              return (
                <SidebarMenuItem key={file.slug}>
                  <SidebarMenuButton
                    isActive={isActive}
                    tooltip={file.title}
                    render={<Link href={href} />}
                    className={cn(
                      "h-8 text-[13px] px-3 font-normal transition-all py-1.5 rounded-md cursor-pointer",
                      isActive
                        ? "bg-primary/10 text-primary font-medium hover:bg-primary/10 hover:text-primary"
                        : "text-muted-foreground hover:bg-muted/50 hover:text-foreground"
                    )}
                  >
                    <span>{file.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              );
            })

          )}
        </SidebarMenu>
      </SidebarContent>
    </Sidebar>
  );
}
