import { notFound } from "next/navigation";
import Link from "next/link";
import fs from "fs";
import path from "path";
import {
  ChevronRight,
  ChevronLeft,
} from "lucide-react";
import { getTopicBySlug, getAllTopicFiles, learningTopics, type TopicFile } from "@/config/learning";
import { MarkdownRenderer } from "@/components/learning/MarkdownRenderer";
import { TableOfContents } from "@/components/learning/TableOfContents";
import { extractHeadings } from "@/lib/extract-headings";
import { parsePythonToMarkdown } from "@/lib/parse-python";

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

  const allFiles = getAllTopicFiles(topic);
  const file = allFiles.find((f) => f.slug === fileSlug);
  if (!file) {
    notFound();
  }

  const displayTitle = file.number ? `${file.number}. ${file.title}` : file.title;
  const getFileDisplayTitle = (f: TopicFile) => f.number ? `${f.number}. ${f.title}` : f.title;

  // Read the content from the file system using the filename in config
  const contentPath = path.join(
    process.cwd(),
    "src",
    "content",
    "learning",
    topicSlug,
    file.filename
  );
  const isPython = file.filename.endsWith(".py");

  let content = "";
  try {
    content = fs.readFileSync(contentPath, "utf-8");
    if (isPython) {
      content = parsePythonToMarkdown(content, displayTitle);
    }
  } catch {
    content = `# ${displayTitle}\n\n*Content coming soon. Add your notes in \`src/content/learning/${topicSlug}/${file.filename}\`.*`;
  }

  const headings = extractHeadings(content);
  const { prev, next } = getPrevNext(allFiles, fileSlug);

  return (
    <div className="flex flex-1">
      {/* Main content area */}
      <div className="flex-1 min-w-0">
        <div className="mx-auto max-w-3xl px-6 py-8 lg:px-10">
          {/* Breadcrumbs */}
          <nav className="mb-8 flex items-center gap-1.5 text-sm text-muted-foreground">
            <Link
              href="/dashboard"
              className="hover:text-foreground transition-colors"
            >
              Courses
            </Link>
            <ChevronRight className="size-3.5" />
            <Link
              href={`/dashboard/${topic.slug}`}
              className="hover:text-foreground transition-colors"
            >
              {topic.title}
            </Link>
            <ChevronRight className="size-3.5" />
            <span className="text-foreground font-medium truncate max-w-[200px]">
              {displayTitle}
            </span>
          </nav>

          {/* Content */}
          <MarkdownRenderer content={content} />

          {/* Navigation footer */}
          <div className="mt-12 flex items-center justify-between border-t border-border/20 pt-6">
            {prev ? (
              <Link
                href={`/dashboard/${topic.slug}/${prev.slug}`}
                className="group flex flex-col gap-1"
              >
                <span className="text-xs text-muted-foreground">Previous</span>
                <span className="flex items-center gap-1 text-sm font-medium text-foreground transition-colors group-hover:text-primary">
                  <ChevronLeft className="size-4" />
                  {getFileDisplayTitle(prev)}
                </span>
              </Link>
            ) : (
              <div />
            )}
            {next ? (
              <Link
                href={`/dashboard/${topic.slug}/${next.slug}`}
                className="group flex flex-col gap-1 text-right"
              >
                <span className="text-xs text-muted-foreground">Next</span>
                <span className="flex items-center gap-1 text-sm font-medium text-foreground transition-colors group-hover:text-primary">
                  {getFileDisplayTitle(next)}
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
      <aside className="hidden xl:block w-64 shrink-0 border-l border-border px-6 py-8">
        <TableOfContents headings={headings} />
      </aside>


    </div>
  );
}

export async function generateStaticParams() {
  const params: Array<{ topic: string; slug: string }> = [];
  for (const topic of learningTopics) {
    const allFiles = getAllTopicFiles(topic);
    for (const file of allFiles) {
      params.push({
        topic: topic.slug,
        slug: file.slug,
      });
    }
  }
  return params;
}
