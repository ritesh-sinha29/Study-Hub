import { notFound } from "next/navigation";
import Link from "next/link";
import { allTopicSlugs, getTopicBySlug, getAllTopicFiles } from "@/config/learning";
import { ArrowRight, BookOpen, Layers, FileText } from "lucide-react";

export function generateStaticParams() {
  return allTopicSlugs.map((slug: string) => ({ topic: slug }));
}

export default async function TopicPage({
  params,
}: {
  params: Promise<{ topic: string }>;
}) {
  const { topic: topicSlug } = await params;
  const topic = getTopicBySlug(topicSlug);

  if (!topic) {
    notFound();
  }

  const allFiles = getAllTopicFiles(topic);
  const firstFile = allFiles[0];

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center max-w-lg mx-auto">
      {/* Icon */}
      <div className="flex size-20 items-center justify-center rounded-2xl bg-primary/10 ring-1 ring-primary/20">
        <BookOpen className="size-9 text-primary" />
      </div>

      {/* Heading */}
      <h1 className="mt-6 text-3xl font-bold tracking-tight">
        Welcome to {topic.title}
      </h1>
      <p className="mt-3 text-muted-foreground leading-relaxed">
        {topic.description}
      </p>

      {/* Stats */}
      <div className="mt-6 flex items-center justify-center gap-6 text-sm text-muted-foreground">
        <div className="flex items-center gap-1.5">
          <FileText className="size-4" />
          <span>{allFiles.length} notes</span>
        </div>
        {topic.groups.length > 0 && (
          <div className="flex items-center gap-1.5">
            <Layers className="size-4" />
            <span>{topic.groups.length} sections</span>
          </div>
        )}
      </div>

      {/* CTA */}
      {firstFile ? (
        <Link
          href={`/dashboard/learning/${topic.slug}/${firstFile.slug}`}
          className="mt-8 inline-flex items-center gap-2 rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-primary-foreground hover:bg-primary/90 transition-colors"
        >
          Start Learning
          <ArrowRight className="size-4" />
        </Link>
      ) : (
        <p className="mt-8 text-sm text-muted-foreground">
          No notes yet — add your first file to get started.
        </p>
      )}

      <Link
        href="/dashboard/learning"
        className="mt-4 text-xs text-muted-foreground hover:text-foreground transition-colors"
      >
        ← Back to all topics
      </Link>
    </div>
  );
}
