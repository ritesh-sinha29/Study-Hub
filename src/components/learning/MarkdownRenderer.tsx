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
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@/components/ui/accordion";
import { slugify } from "@/lib/extract-headings";
import { cn } from "@/lib/utils";
import Prism from "prismjs";
import "prismjs/components/prism-python";
import "prismjs/components/prism-javascript";
import "prismjs/components/prism-typescript";
import "prismjs/components/prism-json";
import "prismjs/components/prism-bash";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-c";
import "prismjs/components/prism-cpp";

interface MarkdownRendererProps {
  content: string;
}

type CalloutType = "NOTE" | "TIP" | "IMPORTANT" | "WARNING" | "CAUTION";

function getCalloutInfo(type: CalloutType) {
  switch (type) {
    case "NOTE":
      return {
        icon: Info,
        className: "border-blue-500/20 bg-blue-500/[0.03] text-blue-900/80 dark:text-blue-200/80",
        iconClassName: "text-blue-500 dark:text-blue-400",
      };
    case "TIP":
      return {
        icon: Lightbulb,
        className: "border-emerald-500/20 bg-emerald-500/[0.03] text-emerald-900/80 dark:text-emerald-200/80",
        iconClassName: "text-emerald-500 dark:text-emerald-400",
      };
    case "IMPORTANT":
      return {
        icon: Info,
        className: "border-purple-500/20 bg-purple-500/[0.03] text-purple-900/80 dark:text-purple-200/80",
        iconClassName: "text-purple-500 dark:text-purple-400",
      };
    case "WARNING":
      return {
        icon: TriangleAlert,
        className: "border-amber-500/20 bg-amber-500/[0.03] text-amber-900/80 dark:text-amber-200/80",
        iconClassName: "text-amber-500 dark:text-amber-400",
      };
    case "CAUTION":
      return {
        icon: CircleAlert,
        className: "border-red-500/20 bg-red-500/[0.03] text-red-900/80 dark:text-red-200/80",
        iconClassName: "text-red-500 dark:text-red-400",
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
            className="scroll-m-20 text-3xl font-extrabold tracking-tight mb-4 mt-6 text-foreground"
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
            className="scroll-m-20 text-2xl font-bold tracking-tight mb-4 mt-10 first:mt-0 border-b border-border/30 pb-2 text-foreground"
            {...props}
          >
            <a
              href={`#${id}`}
              className="group inline-flex items-center gap-2 no-underline hover:text-foreground transition-colors"
            >
              {children}
              <span className="text-muted-foreground/30 opacity-0 transition-opacity group-hover:opacity-100 text-lg font-normal">
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
            className="scroll-m-20 text-lg font-semibold tracking-tight mb-3 mt-8 text-foreground"
            {...props}
          >
            <a
              href={`#${id}`}
              className="group inline-flex items-center gap-2 no-underline hover:text-foreground transition-colors"
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
          className="leading-7 text-[15px] text-muted-foreground my-4"
          {...props}
        >
          {children}
        </p>
      ),
      ul: ({ children, ...props }: React.ComponentPropsWithoutRef<"ul">) => (
        <ul className="my-4 ml-6 list-disc [&>li]:mt-1.5" {...props}>
          {children}
        </ul>
      ),
      ol: ({ children, ...props }: React.ComponentPropsWithoutRef<"ol">) => (
        <ol className="my-4 ml-6 list-decimal [&>li]:mt-1.5" {...props}>
          {children}
        </ol>
      ),
      li: ({ children, ...props }: React.ComponentPropsWithoutRef<"li">) => (
        <li className="text-muted-foreground text-[15px]" {...props}>
          {children}
        </li>
      ),
      code: ({
        children,
        className,
        node,
        ...props
      }: React.ComponentPropsWithoutRef<"code"> & { node?: any }) => {
        const isInline = !className;
        if (isInline) {
          return (
            <code
              className="relative rounded bg-muted/50 px-[0.4rem] py-[0.2rem] font-mono text-[0.85em] font-semibold text-foreground border border-border/10"
              {...props}
            >
              {children}
            </code>
          );
        }

        const match = /language-(\w+)/.exec(className || "");
        const lang = match ? match[1] : "";
        const codeText = String(children).replace(/\n$/, "");
        
        let highlightedHtml = "";
        try {
          if (lang && Prism.languages[lang]) {
            highlightedHtml = Prism.highlight(codeText, Prism.languages[lang], lang);
          } else {
            highlightedHtml = Prism.highlight(codeText, Prism.languages.markup, "markup");
          }
        } catch (e) {
          highlightedHtml = codeText;
        }

        return (
          <code
            className={cn(className, "block font-mono text-[13px] leading-relaxed")}
            dangerouslySetInnerHTML={{ __html: highlightedHtml }}
            {...props}
          />
        );
      },
      pre: ({
        children,
        ...props
      }: React.ComponentPropsWithoutRef<"pre">) => {
        let codeText = "";
        if (children && typeof children === "object" && "props" in (children as object)) {
          const childProps = (children as { props?: { children?: unknown } }).props;
          codeText = String(childProps?.children ?? "");
        }

        let language = "";
        if (children && typeof children === "object" && "props" in (children as object)) {
          const childProps = (children as { props?: { className?: string } }).props;
          const match = childProps?.className?.match(/language-(\w+)/);
          language = match ? match[1] : "";
        }

        return (
          <div className="relative group my-6 rounded-lg border border-border/60 dark:border-border/40 bg-neutral-50 dark:bg-[#09090b] overflow-hidden">
            {language ? (
              <div className="flex items-center justify-between border-b border-border/60 dark:border-border/40 bg-muted/30 dark:bg-muted/10 px-4 py-2">
                <span className="text-[10px] uppercase tracking-wider font-mono font-bold text-muted-foreground/60">
                  {language}
                </span>
                <CopyButton text={codeText} inline />
              </div>
            ) : (
              <CopyButton text={codeText} />
            )}
            <pre
              className="overflow-x-auto p-4 text-[13px] font-mono leading-relaxed bg-transparent text-foreground/90 dark:text-[#e4e4e7] [&>code]:bg-transparent [&>code]:p-0 [&>code]:text-inherit"
              {...props}
            >
              {children}
            </pre>
          </div>
        );
      },
      blockquote: ({
        children,
        ...props
      }: React.ComponentPropsWithoutRef<"blockquote">) => {
        const firstChild = Array.isArray(children) ? children[0] : children;
        const text = firstChild && typeof firstChild === "object" && "props" in firstChild
          ? String((firstChild as { props?: { children?: unknown } }).props?.children ?? "")
          : String(firstChild ?? "");
        const calloutMatch = text.match(/^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*([\s\S]*)/);
        if (calloutMatch) {
          const type = calloutMatch[1] as CalloutType;
          const rest = calloutMatch[2] ? calloutMatch[2].trim() : "";
          const info = getCalloutInfo(type);
          const Icon = info.icon;
          const restChildren = Array.isArray(children) ? children.slice(1) : [];
          return (
            <div
              className={cn("my-5 flex gap-3.5 rounded-lg border px-4 py-3 text-sm leading-6", info.className)}
            >
              <Icon className={cn("mt-0.5 size-4.5 shrink-0", info.iconClassName)} />
              <div className="flex-1 [&>p]:mt-0 text-[14px]">
                {rest && <p className="mt-0 font-medium">{rest}</p>}
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
        <div className="my-6 overflow-x-auto rounded-lg border border-border/40">
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
          className="border-b border-border/40 bg-muted/40 px-4 py-2.5 text-left font-semibold text-foreground"
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
          className="border-b border-border/20 px-4 py-2.5 text-muted-foreground"
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
          className="text-primary font-medium underline underline-offset-4 hover:text-primary/80 transition-colors"
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

  const { mainContent, questions } = useMemo(() => {
    const qaRegex = /<Questions>([\s\S]*?)<\/Questions>/;
    const match = content.match(qaRegex);
    let mainContent = content;
    let questions: Array<{ id: string; title: string; content: string }> = [];

    if (match) {
      mainContent = content.replace(qaRegex, "");
      const qaSection = match[1];
      const questionRegex = /<Question\s+id="([^"]+)"\s+title="([^"]+)">([\s\S]*?)<\/Question>/g;
      let qMatch;
      while ((qMatch = questionRegex.exec(qaSection)) !== null) {
        questions.push({
          id: qMatch[1],
          title: qMatch[2],
          content: qMatch[3].trim(),
        });
      }
    }

    return { mainContent, questions };
  }, [content]);

  return (
    <article className="min-w-0">
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {mainContent}
      </ReactMarkdown>

      {questions.length > 0 && (
        <div className="mt-16 border-t border-border/40 pt-10">
          <h2 className="text-2xl font-bold tracking-tight mb-6 text-foreground">
            Interview Q&As
          </h2>
          <Accordion className="w-full space-y-3">
            {questions.map((q) => (
              <AccordionItem
                key={q.id}
                value={q.id}
                className="border border-border/60 dark:border-border/40 rounded-lg overflow-hidden bg-card/30 dark:bg-[#09090b]/30 hover:bg-neutral-50/50 dark:hover:bg-[#09090b]/50 transition-colors duration-200"
              >
                <AccordionTrigger className="px-5 py-4 text-[15px] font-semibold text-foreground/90 hover:text-foreground no-underline">
                  <span className="flex items-center gap-3">
                    <span className="text-xs font-mono px-2 py-0.5 bg-muted text-muted-foreground rounded border border-border/20">
                      {q.id}
                    </span>
                    {q.title}
                  </span>
                </AccordionTrigger>
                <AccordionContent className="px-5 pb-4 pt-1 text-[14.5px] leading-relaxed text-muted-foreground border-t border-border/20 dark:border-border/10 bg-neutral-50/[0.15] dark:bg-[#09090b]/10">
                  <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
                    {q.content}
                  </ReactMarkdown>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      )}
    </article>
  );
}

