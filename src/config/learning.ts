export interface TopicItem {
  title: string;
  slug: string;
  description: string;
  icon?: string;
  files: TopicFile[];
}

export interface TopicFile {
  title: string;
  slug: string;
  description?: string;
}

export const learningTopics: TopicItem[] = [
  {
    title: "Python Learning",
    slug: "python-learning",
    description: "Python fundamentals, deep dives, and core concepts",
    icon: "Python",
    files: [
      { title: "Day 1 - First Program", slug: "day-1-first-program", description: "Getting started with Python" },
      { title: "Strings & Methods", slug: "strings-and-methods" },
      { title: "Multiline Strings", slug: "multiline-strings" },
      { title: "Lists & List Methods", slug: "lists-and-list-methods" },
      { title: "Tuples", slug: "tuples" },
      { title: "Sets", slug: "sets" },
      { title: "Dictionaries", slug: "dictionaries" },
      { title: "User Input", slug: "user-input" },
      { title: "If-Else Conditions", slug: "if-else-conditions" },
      { title: "Match Case", slug: "match-case" },
      { title: "Loops", slug: "loops" },
      { title: "Functions & Arguments", slug: "functions-and-arguments" },
      { title: "Type Hints & Type Checking", slug: "type-hints" },
      { title: "OOP - Classes & Objects", slug: "oop-classes-and-objects" },
      { title: "Decorators", slug: "decorators" },
      { title: "Async/Await", slug: "async-await" },
      { title: "Exception Handling", slug: "exception-handling" },
      { title: "Modules & Imports", slug: "modules-and-imports" },
      { title: "JSON Handling", slug: "json-handling" },
      { title: "List Comprehensions", slug: "list-comprehensions" },
      { title: "Lambda, Map & Filter", slug: "lambda-map-filter" },
      { title: "Generators & Iterators", slug: "generators-and-iterators" },
      { title: "TypedDict & Dataclasses", slug: "typeddict-and-dataclasses" },
      { title: "Environment Variables", slug: "environment-variables" },
      { title: "File I/O", slug: "file-io" },
      { title: "Dunder Methods", slug: "dunder-methods" },
      { title: "Context Managers", slug: "context-managers" },
      { title: "Decorators Deep Dive", slug: "decorators-deep-dive" },
    ],
  },
  {
    title: "FastAPI",
    slug: "fastapi",
    description: "FastAPI fundamentals and project structure",
    icon: "FastAPI",
    files: [
      { title: "Introduction & Setup", slug: "introduction-and-setup" },
      { title: "Path Parameters", slug: "path-parameters" },
      { title: "Query Parameters", slug: "query-parameters" },
      { title: "Request Body & Pydantic", slug: "request-body-pydantic" },
      { title: "Response Models & Status Codes", slug: "response-models-and-status" },
      { title: "Error Handling", slug: "error-handling" },
      { title: "Dependency Injection", slug: "dependency-injection" },
      { title: "Database CRUD with SQLite", slug: "database-crud-sqlite" },
      { title: "Middleware & CORS", slug: "middleware-cors" },
      { title: "Security & JWT", slug: "security-jwt" },
      { title: "Background Tasks & File Uploads", slug: "background-tasks-and-files" },
    ],
  },
  {
    title: "LangGraph",
    slug: "langgraph",
    description: "LangGraph agent workflows and graphs",
    icon: "LangGraph",
    files: [],
  },
  {
    title: "DSA in C++",
    slug: "dsa-in-cpp",
    description: "Data structures and algorithms in C++",
    icon: "DSA",
    files: [],
  },
];

export function flattenTopicFiles(topics: TopicItem[]): (TopicFile & { topic: string })[] {
  const files: (TopicFile & { topic: string })[] = [];
  for (const topic of topics) {
    for (const file of topic.files) {
      files.push({ ...file, topic: topic.slug });
    }
  }
  return files;
}

export function getTopicBySlug(slug: string): TopicItem | undefined {
  return learningTopics.find((t) => t.slug === slug);
}

export const allTopicSlugs = learningTopics.map((t) => t.slug);
