"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useMemo } from "react";

interface MarkdownRendererProps {
  content: string;
}

export function MarkdownRenderer({ content }: MarkdownRendererProps) {

  const components = useMemo(
    () => ({
      h1: ({ children, ...props }: React.ComponentPropsWithoutRef<"h1">) => (
        <h1
          className="scroll-m-20 text-3xl font-bold tracking-tight mb-4 mt-2"
          {...props}
        >
          {children}
        </h1>
      ),
      h2: ({ children, ...props }: React.ComponentPropsWithoutRef<"h2">) => (
        <h2
          className="scroll-m-20 text-xl font-semibold tracking-tight mb-3 mt-8 first:mt-0"
          {...props}
        >
          {children}
        </h2>
      ),
      h3: ({ children, ...props }: React.ComponentPropsWithoutRef<"h3">) => (
        <h3
          className="scroll-m-20 text-lg font-semibold tracking-tight mb-2 mt-6"
          {...props}
        >
          {children}
        </h3>
      ),
      p: ({ children, ...props }: React.ComponentPropsWithoutRef<"p">) => (
        <p
          className="leading-7 text-muted-foreground [&:not(:first-child)]:mt-4"
          {...props}
        >
          {children}
        </p>
      ),
      ul: ({ children, ...props }: React.ComponentPropsWithoutRef<"ul">) => (
        <ul className="my-4 ml-6 list-disc [&>li]:mt-2" {...props}>
          {children}
        </ul>
      ),
      ol: ({ children, ...props }: React.ComponentPropsWithoutRef<"ol">) => (
        <ol className="my-4 ml-6 list-decimal [&>li]:mt-2" {...props}>
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
      }: React.ComponentPropsWithoutRef<"pre">) => (
        <div className="relative group my-4">
          <pre
            className="overflow-x-auto rounded-lg border bg-muted/50 p-4 text-sm font-mono [&>code]:bg-transparent [&>code]:p-0"
            {...props}
          >
            {children}
          </pre>
        </div>
      ),
      blockquote: ({
        children,
        ...props
      }: React.ComponentPropsWithoutRef<"blockquote">) => (
        <blockquote
          className="mt-4 border-l-4 border-primary/30 pl-4 italic text-muted-foreground"
          {...props}
        >
          {children}
        </blockquote>
      ),
      table: ({
        children,
        ...props
      }: React.ComponentPropsWithoutRef<"table">) => (
        <div className="my-4 overflow-x-auto rounded-lg border">
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
          className="border-b border-border bg-muted/50 px-4 py-2 text-left font-medium"
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
          className="border-b border-border px-4 py-2 text-muted-foreground"
          {...props}
        >
          {children}
        </td>
      ),
      hr: (props: React.ComponentPropsWithoutRef<"hr">) => (
        <hr className="my-6 border-border/40" {...props} />
      ),
      a: ({
        children,
        ...props
      }: React.ComponentPropsWithoutRef<"a">) => (
        <a
          className="text-primary underline underline-offset-4 hover:text-primary/80"
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
    <article className="prose-custom">
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {content}
      </ReactMarkdown>
    </article>
  );
}
