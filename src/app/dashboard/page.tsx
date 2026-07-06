import Link from "next/link";
import { learningTopics, getAllTopicFiles } from "@/config/learning";
import { ArrowRight, FileText, Layers } from "lucide-react";
import * as LucideIcons from "lucide-react";

function getIconForTopic(slug: string, iconName?: string) {
  const normalized = slug.toLowerCase().replace(/[^a-z0-9]/g, "");

  // 1. If an explicit icon name is matched in Lucide, return it
  if (iconName && (LucideIcons as any)[iconName]) {
    return (LucideIcons as any)[iconName];
  }

  // 2. Check for exact match in Lucide keys (case-insensitive)
  const keys = Object.keys(LucideIcons);
  for (const key of keys) {
    if (key.toLowerCase() === normalized) {
      return (LucideIcons as any)[key];
    }
  }

  // 3. Fallback standard developer keyword mappings
  if (normalized.includes("python") || normalized.includes("cpp") || normalized.includes("cplusplus") || normalized.includes("programming")) {
    return LucideIcons.Code2;
  }
  if (normalized.includes("fastapi") || normalized.includes("api") || normalized.includes("server")) {
    return LucideIcons.Terminal;
  }
  if (normalized.includes("langgraph") || normalized.includes("graph")) {
    return LucideIcons.Network;
  }
  if (normalized.includes("dsa") || normalized.includes("algo") || normalized.includes("structure")) {
    return LucideIcons.Dices;
  }
  if (normalized.includes("langchain") || normalized.includes("chain")) {
    return LucideIcons.Brain;
  }
  if (normalized.includes("rag") || normalized.includes("database") || normalized.includes("db") || normalized.includes("sql")) {
    return LucideIcons.Database;
  }
  if (normalized.includes("git") || normalized.includes("github")) {
    return LucideIcons.GitBranch;
  }
  if (normalized.includes("docker") || normalized.includes("container") || normalized.includes("kubernetes")) {
    return LucideIcons.Box;
  }
  if (normalized.includes("javascript") || normalized.includes("js") || normalized.includes("react") || normalized.includes("web") || normalized.includes("node") || normalized.includes("html") || normalized.includes("css")) {
    return LucideIcons.Layout;
  }
  if (normalized.includes("java") || normalized.includes("spring")) {
    return LucideIcons.Coffee;
  }

  // 4. Check for partial prefix/containment match in Lucide
  for (const key of keys) {
    const keyLower = key.toLowerCase();
    if (keyLower.startsWith(normalized) || keyLower.includes(normalized)) {
      return (LucideIcons as any)[key];
    }
  }

  // Default fallback
  return LucideIcons.BookOpen;
}

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
          const Icon = getIconForTopic(topic.slug, topic.icon);
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
