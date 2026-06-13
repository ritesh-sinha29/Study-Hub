"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useMemo } from "react";
import { CopyButton } from "./CopyButton";
import {
  Lightbulb,
  Info,
  TriangleAlert,
  CircleAlert,
} from "lucide-react";
import { slugify } from "@/lib/extract-headings";

interface MarkdownRendererProps {
  content: string;
}

type CalloutType = "NOTE" | "TIP" | "IMPORTANT" | "WARNING" | "CAUTION";

function getCalloutInfo(type: CalloutType) {
  switch (type) {
    case "NOTE":
      return {
        icon: Info,
        className: "border-blue-500/30 bg-blue-500/5",
        iconClassName: "text-blue-500",
      };
    case "TIP":
      return {
        icon: Lightbulb,
        className: "border-emerald-500/30 bg-emerald-500/5",
        iconClassName: "text-emerald-500",
      };
    case "IMPORTANT":
      return {
        icon: Info,
        className: "border-purple-500/30 bg-purple-500/5",
        iconClassName: "text-purple-500",
      };
    case "WARNING":
      return {
        icon: TriangleAlert,
        className: "border-amber-500/30 bg-amber-500/5",
        iconClassName: "text-amber-500",
      };
    case "CAUTION":
      return {
        icon: CircleAlert,
        className: "border-red-500/30 bg-red-500/5",
        iconClassName: "text-red-500",
      };
  }
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {
  const components = useMemo(
    () => ({
      h1: ({ children, ...props }: React.ComponentPropsWithoutRef<"h1">) => {
        const id = slugify(String(children));
        return (
          <h1
            id={id}
            className="scroll-m-20 text-3xl font-bold tracking-tight mb-2 mt-2"
            {...props}
          >
            {children}
          </h1>
        );
      },
      h2: ({ children, ...props }: React.ComponentPropsWithoutRef<"h2">) => {
        const id = slugify(String(children));
        return (
          <h2
            id={id}
            className="scroll-m-20 text-xl font-semibold tracking-tight mb-3 mt-10 first:mt-0 border-b border-border/20 pb-2"
            {...props}
          >
            <a
              href={`#${id}`}
              className="group inline-flex items-center gap-2 no-underline hover:text-foreground"
            >
              {children}
              <span className="text-muted-foreground/30 opacity-0 transition-opacity group-hover:opacity-100 text-base font-normal">
                #
              </span>
            </a>
          </h2>
        );
      },
      h3: ({ children, ...props }: React.ComponentPropsWithoutRef<"h3">) => {
        const id = slugify(String(children));
        return (
          <h3
            id={id}
            className="scroll-m-20 text-lg font-semibold tracking-tight mb-2 mt-8"
            {...props}
          >
            <a
              href={`#${id}`}
              className="group inline-flex items-center gap-2 no-underline hover:text-foreground"
            >
              {children}
              <span className="text-muted-foreground/30 opacity-0 transition-opacity group-hover:opacity-100 text-sm font-normal">
                #
              </span>
            </a>
          </h3>
        );
      },
      p: ({ children, ...props }: React.ComponentPropsWithoutRef<"p">) => (
        <p
          className="leading-7 text-muted-foreground [&:not(:first-child)]:mt-5"
          {...props}
        >
          {children}
        </p>
      ),
      ul: ({ children, ...props }: React.ComponentPropsWithoutRef<"ul">) => (
        <ul className="my-5 ml-6 list-disc [&>li]:mt-2" {...props}>
          {children}
        </ul>
      ),
      ol: ({ children, ...props }: React.ComponentPropsWithoutRef<"ol">) => (
        <ol className="my-5 ml-6 list-decimal [&>li]:mt-2" {...props}>
          {children}
        </ol>
      ),
      li: ({ children, ...props }: React.ComponentPropsWithoutRef<"li">) => (
        <li className="text-muted-foreground" {...props}>
          {children}
        </li>
      ),
      code: ({
        children,
        className,
        ...props
      }: React.ComponentPropsWithoutRef<"code">) => {
        const isInline = !className;
        if (isInline) {
          return (
            <code
              className="relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm font-medium"
              {...props}
            >
              {children}
            </code>
          );
        }
        return (
          <code className={className} {...props}>
            {children}
          </code>
        );
      },
      pre: ({
        children,
        ...props
      }: React.ComponentPropsWithoutRef<"pre">) => {
        // Extract code text for copy button
        let codeText = "";
        if (children && typeof children === "object" && "props" in (children as object)) {
          const childProps = (children as { props?: { children?: unknown } }).props;
          codeText = String(childProps?.children ?? "");
        }

        // Extract language for filename label
        let language = "";
        if (children && typeof children === "object" && "props" in (children as object)) {
          const childProps = (children as { props?: { className?: string } }).props;
          const match = childProps?.className?.match(/language-(\w+)/);
          language = match ? match[1] : "";
        }

        return (
          <div className="relative group my-6">
            {language && (
              <div className="flex items-center justify-between rounded-t-lg border border-b-0 border-border/40 bg-muted/30 px-4 py-1.5">
                <span className="text-xs font-medium text-muted-foreground/70">
                  {language}
                </span>
              </div>
            )}
            <pre
              className={`overflow-x-auto rounded-lg border bg-[#0a0a0f] dark:bg-[#0a0a0f] text-[#e4e4e7] p-4 text-sm font-mono leading-relaxed [&>code]:bg-transparent [&>code]:p-0 [&>code]:text-inherit ${language ? "rounded-t-none" : ""}`}
              {...props}
            >
              {children}
            </pre>
            <CopyButton text={codeText} />
          </div>
        );
      },
      blockquote: ({
        children,
        ...props
      }: React.ComponentPropsWithoutRef<"blockquote">) => {
        // Check for GitHub-style callouts: > [!NOTE] / > [!TIP] / > [!WARNING] / > [!CAUTION]
        const firstChild = Array.isArray(children) ? children[0] : children;
        const text = firstChild && typeof firstChild === "object" && "props" in firstChild
          ? String((firstChild as { props?: { children?: unknown } }).props?.children ?? "")
          : String(firstChild ?? "");
        const calloutMatch = text.match(/^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*([\s\S]*)/);
        if (calloutMatch) {
          const type = calloutMatch[1] as CalloutType;
          const rest = calloutMatch[2].trim();
          const info = getCalloutInfo(type);
          const Icon = info.icon;
          // Remove the first child (callout header) and keep the rest
          const restChildren = Array.isArray(children) ? children.slice(1) : [];
          return (
            <div
              className={`my-6 flex gap-3 rounded-lg border px-4 py-3 ${info.className}`}
            >
              <Icon className={`mt-0.5 size-5 shrink-0 ${info.iconClassName}`} />
              <div className="text-sm leading-7 text-muted-foreground [&>p]:mt-0">
                {rest && <p className="mt-0">{rest}</p>}
                {restChildren}
              </div>
            </div>
          );
        }
        return (
          <blockquote
            className="mt-6 border-l-4 border-primary/30 pl-4 italic text-muted-foreground"
            {...props}
          >
            {children}
          </blockquote>
        );
      },
      table: ({
        children,
        ...props
      }: React.ComponentPropsWithoutRef<"table">) => (
        <div className="my-6 overflow-x-auto rounded-lg border">
          <table className="w-full text-sm" {...props}>
            {children}
          </table>
        </div>
      ),
      th: ({
        children,
        ...props
      }: React.ComponentPropsWithoutRef<"th">) => (
        <th
          className="border-b border-border bg-muted/50 px-4 py-2.5 text-left font-medium"
          {...props}
        >
          {children}
        </th>
      ),
      td: ({
        children,
        ...props
      }: React.ComponentPropsWithoutRef<"td">) => (
        <td
          className="border-b border-border px-4 py-2.5 text-muted-foreground"
          {...props}
        >
          {children}
        </td>
      ),
      hr: (props: React.ComponentPropsWithoutRef<"hr">) => (
        <hr className="my-8 border-border/20" {...props} />
      ),
      a: ({
        children,
        ...props
      }: React.ComponentPropsWithoutRef<"a">) => (
        <a
          className="text-primary underline underline-offset-4 hover:text-primary/80 transition-colors"
          target="_blank"
          rel="noopener noreferrer"
          {...props}
        >
          {children}
        </a>
      ),
    }),
    []
  );

  return (
    <article className="min-w-0">
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {content}
      </ReactMarkdown>
    </article>
  );
}
