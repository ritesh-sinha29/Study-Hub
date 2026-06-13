import { notFound, redirect } from "next/navigation";
import Link from "next/link";
import { allTopicSlugs, getTopicBySlug } from "@/config/learning";
import { TopicSidebar } from "@/components/learning/TopicSidebar";
import { ChevronRight, BookOpen } from "lucide-react";

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

  // If topic has files, redirect to the first file
  if (topic.files.length > 0) {
    const firstFile = topic.files[0];
    redirect(`/dashboard/learning/${topic.slug}/${firstFile.slug}`);
  }

  return (
    <div className="flex flex-1">
      <TopicSidebar topic={topic} />
      <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
        <div className="flex size-16 items-center justify-center rounded-full bg-muted">
          <BookOpen className="size-8 text-muted-foreground" />
        </div>
        <h2 className="mt-6 text-xl font-semibold">{topic.title}</h2>
        <p className="mt-2 text-muted-foreground max-w-md">
          {topic.description}
        </p>
        <p className="mt-1 text-sm text-muted-foreground">
          No content files yet. Start by adding your first note.
        </p>
        <Link
          href="/dashboard/learning"
          className="mt-6 inline-flex items-center gap-1 text-sm text-primary hover:underline"
        >
          Back to topics
          <ChevronRight className="size-4" />
        </Link>
      </div>
    </div>
  );
}
