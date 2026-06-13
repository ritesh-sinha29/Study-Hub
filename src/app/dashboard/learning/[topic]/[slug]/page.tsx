import { notFound } from "next/navigation";
import fs from "fs";
import path from "path";
import { getTopicBySlug } from "@/config/learning";
import { TopicSidebar } from "@/components/learning/TopicSidebar";
import { MarkdownRenderer } from "@/components/learning/MarkdownRenderer";

interface PageProps {
  params: Promise<{ topic: string; slug: string }>;
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

  return (
    <div className="flex flex-1">
      <TopicSidebar topic={topic} />
      <main className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-3xl px-6 py-8">
          <MarkdownRenderer content={content} />
        </div>
      </main>
    </div>
  );
}
