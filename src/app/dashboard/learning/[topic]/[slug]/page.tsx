import { notFound } from "next/navigation";
import Link from "next/link";
import fs from "fs";
import path from "path";
import {
  ChevronRight,
  ChevronLeft,
} from "lucide-react";
import { getTopicBySlug, type TopicFile } from "@/config/learning";
import { MarkdownRenderer } from "@/components/learning/MarkdownRenderer";
import { TableOfContents } from "@/components/learning/TableOfContents";
import { extractHeadings } from "@/lib/extract-headings";

interface PageProps {
  params: Promise<{ topic: string; slug: string }>;
}

function getPrevNext(
  files: TopicFile[],
  currentSlug: string
): { prev: TopicFile | null; next: TopicFile | null } {
  const idx = files.findIndex((f) => f.slug === currentSlug);
  return {
    prev: idx > 0 ? files[idx - 1] : null,
    next: idx < files.length - 1 ? files[idx + 1] : null,
  };
}

export default async function TopicFilePage({ params }: PageProps) {
  const { topic: topicSlug, slug: fileSlug } = await params;
  const topic = getTopicBySlug(topicSlug);

  if (!topic) {
    notFound();
  }

  const file = topic.files.find((f) => f.slug === fileSlug);
  if (!file) {
    notFound();
  }

  // Read the markdown content from the file system
  const contentPath = path.join(
    process.cwd(),
    "src",
    "content",
    "learning",
    topicSlug,
    `${fileSlug}.md`
  );

  let content = "";
  try {
    content = fs.readFileSync(contentPath, "utf-8");
  } catch {
    content = `# ${file.title}\n\n*Content coming soon. Add your notes in \`src/content/learning/${topicSlug}/${fileSlug}.md\`.*`;
  }

  const headings = extractHeadings(content);
  const { prev, next } = getPrevNext(topic.files, fileSlug);

  return (
    <div className="flex flex-1">
      {/* Main content area */}
      <div className="flex-1 min-w-0">
        <div className="mx-auto max-w-3xl px-6 py-8 lg:px-10">
          {/* Breadcrumbs */}
          <nav className="mb-8 flex items-center gap-1.5 text-sm text-muted-foreground">
            <Link
              href="/dashboard/learning"
              className="hover:text-foreground transition-colors"
            >
              Courses
            </Link>
            <ChevronRight className="size-3.5" />
            <Link
              href={`/dashboard/learning/${topic.slug}`}
              className="hover:text-foreground transition-colors"
            >
              {topic.title}
            </Link>
            <ChevronRight className="size-3.5" />
            <span className="text-foreground font-medium truncate max-w-[200px]">
              {file.title}
            </span>
          </nav>

          {/* Content */}
          <MarkdownRenderer content={content} />

          {/* Navigation footer */}
          <div className="mt-12 flex items-center justify-between border-t border-border/20 pt-6">
            {prev ? (
              <Link
                href={`/dashboard/learning/${topic.slug}/${prev.slug}`}
                className="group flex flex-col gap-1"
              >
                <span className="text-xs text-muted-foreground">Previous</span>
                <span className="flex items-center gap-1 text-sm font-medium text-foreground transition-colors group-hover:text-primary">
                  <ChevronLeft className="size-4" />
                  {prev.title}
                </span>
              </Link>
            ) : (
              <div />
            )}
            {next ? (
              <Link
                href={`/dashboard/learning/${topic.slug}/${next.slug}`}
                className="group flex flex-col gap-1 text-right"
              >
                <span className="text-xs text-muted-foreground">Next</span>
                <span className="flex items-center gap-1 text-sm font-medium text-foreground transition-colors group-hover:text-primary">
                  {next.title}
                  <ChevronRight className="size-4" />
                </span>
              </Link>
            ) : (
              <div />
            )}
          </div>
        </div>
      </div>

      {/* Table of Contents sidebar */}
      <aside className="hidden xl:block w-64 shrink-0 border-l border-border/20 px-6 py-8">
        <TableOfContents headings={headings} />
      </aside>


    </div>
  );
}
