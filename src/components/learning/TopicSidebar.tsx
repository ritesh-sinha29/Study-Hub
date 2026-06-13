"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarFooter,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { ChevronLeft, ChevronDown, ChevronRight, FileText, Folder, HelpCircle } from "lucide-react";
import { type TopicItem, type TopicFile, type TopicGroup } from "@/config/learning";

function FileItem({
  file,
  topicSlug,
  isActive,
}: {
  file: TopicFile;
  topicSlug: string;
  isActive: boolean;
}) {
  const href = `/dashboard/learning/${topicSlug}/${file.slug}`;
  return (
    <SidebarMenuItem key={file.slug}>
      <SidebarMenuButton
        isActive={isActive}
        tooltip={file.title}
        render={<Link href={href} />}
        className={cn(
          "h-8 text-[13px] px-2 font-normal transition-all py-1.5 rounded-md cursor-pointer gap-2.5 group-data-[collapsible=icon]:gap-0 group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:px-0",
          isActive
            ? "bg-neutral-100 dark:bg-neutral-800 text-foreground font-semibold hover:bg-neutral-100 dark:hover:bg-neutral-800 hover:text-foreground"
            : "text-muted-foreground hover:bg-muted/50 hover:text-foreground"
        )}
      >
        {file.number ? (
          <span
            className={cn(
              "w-6 shrink-0 text-[11px] font-mono font-semibold transition-colors group-data-[collapsible=icon]:w-auto",
              isActive
                ? "text-primary"
                : "text-muted-foreground/60"
            )}
          >
            {file.number}
          </span>
        ) : (
          <FileText className="size-4 shrink-0" />
        )}
        <span className="truncate group-data-[collapsible=icon]:hidden">{file.title}</span>
      </SidebarMenuButton>
    </SidebarMenuItem>
  );
}

function GroupSection({
  group,
  topicSlug,
  pathname,
}: {
  group: TopicGroup;
  topicSlug: string;
  pathname: string;
}) {
  const isActive = group.files.some(
    (f) => pathname === `/dashboard/learning/${topicSlug}/${f.slug}`
  );
  const [open, setOpen] = useState(isActive);

  // Auto-open when any file in this group becomes the active route
  useEffect(() => {
    if (isActive) setOpen(true);
  }, [isActive]);

  return (
    <div className="mb-1 mt-3 first:mt-0">
      {/* Group header — visually distinct from file items */}
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center gap-1.5 px-2 py-1 rounded-md transition-colors group/header text-neutral-800 dark:text-neutral-200 group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:px-0"
      >
        <Folder className="size-3 shrink-0 opacity-60" />
        <span className="truncate flex-1 text-left text-[10.5px] font-semibold uppercase tracking-widest group-data-[collapsible=icon]:hidden">
          {group.title.replace(/^\d+\.\s*/, "")}
        </span>
        <span className="group-data-[collapsible=icon]:hidden">
          {open ? (
            <ChevronDown className="size-3 shrink-0 opacity-40" />
          ) : (
            <ChevronRight className="size-3 shrink-0 opacity-40" />
          )}
        </span>
      </button>

      {/* Group files */}
      {open && (
        <SidebarMenu className="ml-3 border-l border-border pl-2 mt-0.5 group-data-[collapsible=icon]:hidden">
          {group.files.map((file) => {
            const href = `/dashboard/learning/${topicSlug}/${file.slug}`;
            const active = pathname === href;
            return (
              <FileItem
                key={file.slug}
                file={file}
                topicSlug={topicSlug}
                isActive={active}
              />
            );
          })}
        </SidebarMenu>
      )}
    </div>
  );
}

export function TopicSidebar({ topic }: { topic: TopicItem }) {
  const pathname = usePathname();

  // Check if any file in a group is active (to auto-open that group)
  const isGroupActive = (group: TopicGroup) =>
    group.files.some(
      (f) => pathname === `/dashboard/learning/${topic.slug}/${f.slug}`
    );

  return (
    <Sidebar collapsible="icon" variant="sidebar">
      <SidebarHeader className="h-16 flex flex-row items-center justify-between p-2 border-b border-border">
        <div className="flex items-center gap-2 flex-1 min-w-0 group-data-[collapsible=icon]:hidden">
          <SidebarMenu className="flex-1 min-w-0">
            <SidebarMenuItem>
              <SidebarMenuButton
                size="lg"
                render={<Link href="/dashboard/learning" />}
              >
                <div className="flex flex-col justify-center gap-0.5 leading-none">
                  <span className="font-semibold text-sm">{topic.title}</span>
                  <span className="text-xs text-muted-foreground">
                    {topic.files.length + topic.groups.reduce((acc, g) => acc + g.files.length, 0)} files
                  </span>
                </div>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </div>
        <SidebarTrigger className="h-8 w-8 shrink-0 hover:bg-muted group-data-[collapsible=icon]:mx-auto" />
      </SidebarHeader>

      <SidebarContent className="px-2">
        {topic.files.length === 0 && topic.groups.length === 0 ? (
          <div className="px-3 py-8 text-center">
            <FileText className="size-8 mx-auto text-muted-foreground/40" />
            <p className="mt-2 text-sm text-muted-foreground">No notes yet</p>
          </div>
        ) : (
          <>
            {/* Root-level files (no subfolder) */}
            {topic.files.length > 0 && (
              <SidebarMenu>
                {topic.files.map((file) => {
                  const href = `/dashboard/learning/${topic.slug}/${file.slug}`;
                  const isActive = pathname === href;
                  return (
                    <FileItem
                      key={file.slug}
                      file={file}
                      topicSlug={topic.slug}
                      isActive={isActive}
                    />
                  );
                })}
              </SidebarMenu>
            )}

            {/* Subfolder groups */}
            {topic.groups.map((group) => (
              <GroupSection
                key={group.slug}
                group={group}
                topicSlug={topic.slug}
                pathname={pathname}
              />
            ))}
          </>
        )}
      </SidebarContent>

      <SidebarFooter className="p-3 group-data-[collapsible=icon]:p-2 border-t border-border">
        <SidebarMenu className="gap-2">
          <SidebarMenuItem>
            <SidebarMenuButton
              size="default"
              render={<Link href="/dashboard/help" />}
              className="flex items-center justify-center gap-2 w-full h-9 rounded-md border border-border hover:bg-muted/50 hover:text-foreground text-[13px] font-medium transition-all group-data-[collapsible=icon]:size-8 group-data-[collapsible=icon]:p-0 group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:mx-auto"
            >
              <HelpCircle className="size-4 shrink-0" />
              <span className="group-data-[collapsible=icon]:hidden">Help & Support</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="default"
              render={<Link href="/dashboard/learning" />}
              className="flex items-center justify-center gap-2 w-full h-9 rounded-md border border-border hover:bg-muted/50 hover:text-foreground text-[13px] font-medium transition-all group-data-[collapsible=icon]:size-8 group-data-[collapsible=icon]:p-0 group-data-[collapsible=icon]:justify-center group-data-[collapsible=icon]:mx-auto"
            >
              <ChevronLeft className="size-4 shrink-0" />
              <span className="group-data-[collapsible=icon]:hidden">Back to Courses</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
