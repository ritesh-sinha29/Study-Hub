"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { cn } from "@/lib/utils";
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarFooter,
} from "@/components/ui/sidebar";
import { ChevronLeft, ChevronDown, ChevronRight, FileText, HelpCircle } from "lucide-react";
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
          "h-8 text-[13px] px-2 font-normal transition-all py-1.5 rounded-md cursor-pointer gap-2.5",
          isActive
            ? "bg-neutral-100 dark:bg-neutral-800 text-foreground font-semibold hover:bg-neutral-100 dark:hover:bg-neutral-800 hover:text-foreground"
            : "text-muted-foreground hover:bg-muted/50 hover:text-foreground"
        )}
      >
        {file.number ? (
          <span
            className={cn(
              "flex size-5 shrink-0 items-center justify-center rounded text-[10px] font-bold font-mono transition-colors",
              isActive
                ? "bg-primary/15 text-primary"
                : "bg-muted text-muted-foreground"
            )}
          >
            {file.number}
          </span>
        ) : (
          <span className="size-5 shrink-0" />
        )}
        <span className="truncate">{file.title}</span>
      </SidebarMenuButton>
    </SidebarMenuItem>
  );
}

function GroupSection({
  group,
  topicSlug,
  pathname,
  defaultOpen,
}: {
  group: TopicGroup;
  topicSlug: string;
  pathname: string;
  defaultOpen: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div className="mb-1">
      {/* Group header */}
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-[12px] font-semibold text-muted-foreground hover:text-foreground transition-colors"
      >
        {group.number ? (
          <span className="flex size-5 shrink-0 items-center justify-center rounded bg-muted text-[10px] font-bold font-mono text-muted-foreground">
            {group.number}
          </span>
        ) : null}
        <span className="truncate flex-1 text-left">{group.title.replace(/^\d+\.\s*/, "")}</span>
        {open ? (
          <ChevronDown className="size-3.5 shrink-0 opacity-50" />
        ) : (
          <ChevronRight className="size-3.5 shrink-0 opacity-50" />
        )}
      </button>

      {/* Group files */}
      {open && (
        <SidebarMenu className="ml-3 border-l border-border/40 pl-2 mt-0.5">
          {group.files.map((file) => {
            const href = `/dashboard/learning/${topicSlug}/${file.slug}`;
            const isActive = pathname === href;
            return (
              <FileItem
                key={file.slug}
                file={file}
                topicSlug={topicSlug}
                isActive={isActive}
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
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="lg"
              render={<Link href="/dashboard/learning" />}
            >
              <div className="flex size-8 items-center justify-center rounded-lg bg-primary text-sm font-bold text-primary-foreground">
                S
              </div>
              <div className="flex flex-col justify-center gap-0.5 leading-none">
                <span className="font-semibold text-sm">{topic.title}</span>
                <span className="text-xs text-muted-foreground">
                  {topic.files.length + topic.groups.reduce((acc, g) => acc + g.files.length, 0)} files
                </span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      <div className="px-3 my-2">
        <div className="h-px bg-border/40" />
      </div>

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
                defaultOpen={isGroupActive(group)}
              />
            ))}
          </>
        )}
      </SidebarContent>

      <SidebarFooter className="p-3 border-t border-border/40">
        <SidebarMenu className="gap-2">
          <SidebarMenuItem>
            <SidebarMenuButton
              size="default"
              render={<Link href="/dashboard/help" />}
              className="flex items-center justify-center gap-2 w-full h-9 rounded-md border border-border/60 hover:bg-muted/50 hover:text-foreground text-[13px] font-medium transition-all"
            >
              <HelpCircle className="size-4 shrink-0" />
              <span>Help & Support</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="default"
              render={<Link href="/dashboard/learning" />}
              className="flex items-center justify-center gap-2 w-full h-9 rounded-md border border-border/60 hover:bg-muted/50 hover:text-foreground text-[13px] font-medium transition-all"
            >
              <ChevronLeft className="size-4 shrink-0" />
              <span>Back to Courses</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
