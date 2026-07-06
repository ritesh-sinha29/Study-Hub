import Link from "next/link";
import { learningTopics, getAllTopicFiles } from "@/config/learning";
import { BookOpen, Code2, Network, Dices, ArrowRight, FileText, Layers, Brain, Database } from "lucide-react";

const iconMap: Record<string, typeof BookOpen> = {
  Python: Code2,
  FastAPI: BookOpen,
  LangGraph: Network,
  DSA: Dices,
  LangChain: Brain,
  RAG: Database,
};

export default function StudyHubPage() {
  return (
    <div className="flex flex-1 flex-col gap-8 p-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
          Study Hub 📚
        </h1>
        <p className="mt-2 text-muted-foreground max-w-xl">
          Browse your revision notes organized by topic. Click a topic to dive into the content.
        </p>
      </div>

      {/* Topic Grid */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {learningTopics.map((topic) => {
          const Icon = iconMap[topic.icon ?? ""] || BookOpen;
          const totalFiles = getAllTopicFiles(topic).length;
          const hasGroups = topic.groups.length > 0;
          return (
            <Link
              key={topic.slug}
              href={`/dashboard/${topic.slug}`}
              className="group relative rounded-xl border bg-card p-5 transition-all hover:shadow-md hover:border-primary/30 active:scale-[0.98]"
            >
              <div className="flex items-start justify-between">
                <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10 text-primary">
                  <Icon className="size-5" />
                </div>
                <ArrowRight className="size-4 text-muted-foreground opacity-0 -translate-x-1 transition-all group-hover:opacity-100 group-hover:translate-x-0" />
              </div>
              <h3 className="mt-4 font-semibold">{topic.title}</h3>
              <p className="mt-1 text-sm text-muted-foreground line-clamp-2">
                {topic.description}
              </p>
              <div className="mt-4 flex items-center gap-4 text-xs text-muted-foreground">
                <span className="flex items-center gap-1">
                  <FileText className="size-3" />
                  {totalFiles} {totalFiles === 1 ? "file" : "files"}
                </span>
                {hasGroups && (
                  <span className="flex items-center gap-1">
                    <Layers className="size-3" />
                    {topic.groups.length} {topic.groups.length === 1 ? "section" : "sections"}
                  </span>
                )}
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
