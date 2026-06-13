"use client";

import Link from "next/link";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
} from "@/components/ui/sidebar";
import {
  BookOpen,
  HelpCircle,
} from "lucide-react";

const navItems = [
  {
    title: "Courses",
    icon: BookOpen,
    href: "/dashboard/learning",
  },
];

const footerItems = [
  {
    title: "Help & Support",
    icon: HelpCircle,
    href: "/dashboard/help",
  },
];

export function AppSidebar() {
  return (
    <Sidebar collapsible="icon" variant="sidebar">
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" render={<Link href="/dashboard" />}>
              <div className="flex size-8 items-center justify-center rounded-lg bg-primary text-sm font-bold text-primary-foreground">
                S
              </div>
              <div className="flex flex-col justify-center gap-0.5 leading-none">
                <span className="font-semibold text-sm">Study Hub</span>
                <span className="text-xs text-muted-foreground">
                  Study Platform
                </span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      <div className="px-3 my-2">
        <div className="h-px bg-border/40" />
      </div>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton tooltip={item.title} render={<Link href={item.href} />}>
                    <item.icon className="size-4" />
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="p-3 border-t border-border/40">
        <SidebarMenu>
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
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
