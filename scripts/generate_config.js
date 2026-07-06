const fs = require('fs');
const path = require('path');

const CONTENT_DIR = path.join(__dirname, '../src/content/learning');
const CONFIG_FILE = path.join(__dirname, '../src/config/learning.ts');

const STATIC_TOPICS = [
  {
    title: "Python Learning",
    slug: "python-learning",
    description: "Python fundamentals, deep dives, and core concepts",
    icon: "Python",
  },
  {
    title: "FastAPI",
    slug: "fastapi",
    description: "FastAPI fundamentals and project structure",
    icon: "FastAPI",
  },
  {
    title: "LangGraph",
    slug: "langgraph",
    description: "LangGraph agent workflows and graphs",
    icon: "LangGraph",
  },
  {
    title: "DSA with C++",
    slug: "dsa-with-cpp",
    description: "Data structures and algorithms in C++",
    icon: "DSA",
  },
  {
    title: "C++",
    slug: "cpp",
    description: "C++ basics, programming syntax, and foundations",
    icon: "BookOpen",
  },
  {
    title: "LangChain",
    slug: "langchain",
    description: "LangChain frameworks, components, and LLM integrations",
    icon: "LangChain",
  },
  {
    title: "RAG",
    slug: "rag",
    description: "Retrieval-Augmented Generation architectures, embeddings, and vector databases",
    icon: "RAG",
  }
];

const PREFERRED_ORDER = {
  "python-learning": [
    "day-1-first-program",
    "strings-and-methods",
    "multiline-strings",
    "lists-and-list-methods",
    "tuples",
    "sets",
    "dictionaries",
    "user-input",
    "if-else-conditions",
    "match-case",
    "loops",
    "functions-and-arguments",
    "type-hints",
    "oop-classes-and-objects",
    "decorators",
    "async-await",
    "exception-handling",
    "modules-and-imports",
    "json-handling",
    "list-comprehensions",
    "lambda-map-filter",
    "generators-and-iterators",
    "typeddict-and-dataclasses",
    "environment-variables",
    "file-io",
    "dunder-methods",
    "context-managers",
    "decorators-deep-dive"
  ],
  "fastapi": [
    "introduction-and-setup",
    "path-parameters",
    "query-parameters",
    "request-body-pydantic",
    "response-models-and-status",
    "error-handling",
    "dependency-injection",
    "database-crud-sqlite",
    "middleware-cors",
    "security-jwt",
    "background-tasks-and-files"
  ]
};

function extractTitle(filePath, slug) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.replace(/\r\n/g, '\n').split('\n');
    
    for (let line of lines) {
      line = line.trim();
      if (line === '') continue;
      
      if (line.startsWith('#') || line.startsWith('//')) {
        const clean = line.replace(/^(?:#|\/\/)\s*/, '').replace(/[\-=\*#_\/]+/g, '').trim();
        
        if (clean.length > 2) {
          let title = clean;
          // Strip any course/series heading prefix like "FASTAPI STUDY GUIDE: 01." or "FASTAPI YT SERIES: 02."
          title = title.replace(/^(?:[\w]+\s+)+(?:guide|study|series|course|tutorial)[:\s]*(?:\d+[\w]*[\.\s\-]*)*/i, '');
          // Strip any remaining leading number like "01. " or "01 - "
          title = title.replace(/^\d+[a-zA-Z]*[\.\s\-]+/, '');
          
          let formattedTitle = title.split(/\s+/)
            .map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase())
            .join(' ');
            
          formattedTitle = formattedTitle
            .replace(/^Python\s+/i, '')
            .replace(/\s*\(for\s+beginners\)/i, '')
            .replace(/\s*\(learning\s+guide\)/i, '')
            .replace(/\s*\(file\s+i\/o\)/i, '')
            .trim();
            
          return formattedTitle;
        }
      } else if (line.startsWith('```')) {
        continue;
      } else {
        break;
      }
    }
  } catch (err) {
    console.error('Error extracting title from:', filePath, err);
  }
  
  return slug.split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

function getFileNumber(filename) {
  const match = filename.match(/^(\d+)([a-zA-Z]*)/);
  if (!match) return { num: Infinity, suffix: '' };
  return {
    num: parseInt(match[1], 10),
    suffix: match[2]
  };
}

function generateConfig() {
  console.log('Scanning content directory...');
  const topics = [];

  // Dynamically discover all course folders in the learning content directory
  let folders = [];
  if (fs.existsSync(CONTENT_DIR)) {
    folders = fs.readdirSync(CONTENT_DIR).filter(item => {
      const fullPath = path.join(CONTENT_DIR, item);
      return fs.statSync(fullPath).isDirectory();
    });
  }

  // Combine predefined static topics and any newly created subdirectories
  const allTopicSlugs = Array.from(new Set([
    ...STATIC_TOPICS.map(t => t.slug),
    ...folders
  ]));

  for (const topicSlug of allTopicSlugs) {
    const staticTopic = STATIC_TOPICS.find(t => t.slug === topicSlug);
    const topicDir = path.join(CONTENT_DIR, topicSlug);
    
    const topicMeta = staticTopic || {
      title: topicSlug.split('-')
        .map(w => w.charAt(0).toUpperCase() + w.slice(1))
        .join(' '),
      slug: topicSlug,
      description: `Revision notes and guides for ${topicSlug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}`,
      icon: "BookOpen"
    };

    // Root-level files (no subfolder)
    const rootFiles = [];
    // Subfolder groups
    const groups = [];

    function parseFile(item, fullPath, relativeFilename) {
      if (item.endsWith('-test.md') || item.endsWith('-test.py')) return null;
      const baseName = item.replace(/\.[^/.]+$/, '');
      const slug = baseName.replace(/^\d+[_ \-]/, '').replace(/_/g, '-');
      const title = extractTitle(fullPath, slug);
      const numberMatch = baseName.match(/^(\d+[a-zA-Z]*)[_ \-]/);
      const number = numberMatch ? numberMatch[1] : undefined;
      return { title, slug, number, filename: relativeFilename.replace(/\\/g, '/'), sortKey: item.toLowerCase() };
    }

    function sortFiles(arr) {
      return arr.sort((a, b) => {
        const numA = getFileNumber(path.basename(a.filename));
        const numB = getFileNumber(path.basename(b.filename));
        if (numA.num !== numB.num) return numA.num - numB.num;
        if (numA.suffix !== numB.suffix) return numA.suffix.localeCompare(numB.suffix);
        return a.sortKey.localeCompare(b.sortKey);
      });
    }

    if (fs.existsSync(topicDir)) {
      const topLevelItems = fs.readdirSync(topicDir);

      for (const item of topLevelItems) {
        const fullPath = path.join(topicDir, item);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory()) {
          // This is a subfolder → becomes a group
          const groupBaseName = item;
          const groupSlug = groupBaseName.replace(/^\d+[_ \-]/, '').replace(/_/g, '-');
          const groupNumberMatch = groupBaseName.match(/^(\d+[a-zA-Z]*)[_ \-]/);
          const groupNumber = groupNumberMatch ? groupNumberMatch[1] : undefined;
          let groupTitle = groupSlug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
          if (groupNumber) groupTitle = `${groupNumber}. ${groupTitle}`;

          const groupFiles = [];
          const subItems = fs.readdirSync(fullPath);
          for (const subItem of subItems) {
            const subFullPath = path.join(fullPath, subItem);
            if (fs.statSync(subFullPath).isFile() && (subItem.endsWith('.md') || subItem.endsWith('.py') || subItem.endsWith('.cpp'))) {
              const parsed = parseFile(subItem, subFullPath, path.join(item, subItem));
              if (parsed) groupFiles.push(parsed);
            }
          }
          sortFiles(groupFiles);
          groups.push({
            title: groupTitle,
            slug: groupSlug,
            number: groupNumber,
            sortKey: item.toLowerCase(),
            files: groupFiles.map(({ title, slug, number, filename }) => ({ title, slug, number, filename }))
          });

        } else if (stat.isFile() && (item.endsWith('.md') || item.endsWith('.py') || item.endsWith('.cpp'))) {
          // Root-level file
          const parsed = parseFile(item, fullPath, item);
          if (parsed) rootFiles.push(parsed);
        }
      }
    }

    sortFiles(rootFiles);
    groups.sort((a, b) => {
      const numA = getFileNumber(a.sortKey);
      const numB = getFileNumber(b.sortKey);
      if (numA.num !== numB.num) return numA.num - numB.num;
      if (numA.suffix !== numB.suffix) return numA.suffix.localeCompare(numB.suffix);
      return a.sortKey.localeCompare(b.sortKey);
    });

    const cleanFiles = rootFiles.map(({ title, slug, number, filename }) => ({ title, slug, number, filename }));
    const cleanGroups = groups.map(({ title, slug, number, files }) => ({ title, slug, number, files }));

    topics.push({
      ...topicMeta,
      files: cleanFiles,
      groups: cleanGroups
    });
  }

  const code = `// This file is auto-generated by scripts/generate_config.js
// Do not edit this file manually.

export interface TopicFile {
  title: string;
  slug: string;
  filename: string;
  number?: string;
}

export interface TopicGroup {
  title: string;
  slug: string;
  number?: string;
  files: TopicFile[];
}

export interface TopicItem {
  title: string;
  slug: string;
  description: string;
  icon?: string;
  files: TopicFile[];
  groups: TopicGroup[];
}

export const learningTopics: TopicItem[] = ${JSON.stringify(topics, null, 2)};

export function flattenTopicFiles(topics: TopicItem[]): (TopicFile & { topic: string })[] {
  const files: (TopicFile & { topic: string })[] = [];
  for (const topic of topics) {
    for (const file of topic.files) {
      files.push({ ...file, topic: topic.slug });
    }
    for (const group of topic.groups) {
      for (const file of group.files) {
        files.push({ ...file, topic: topic.slug });
      }
    }
  }
  return files;
}

export function getAllTopicFiles(topic: TopicItem): TopicFile[] {
  return [
    ...topic.files,
    ...topic.groups.flatMap(g => g.files),
  ];
}

export function getTopicBySlug(slug: string): TopicItem | undefined {
  return learningTopics.find((t) => t.slug === slug);
}

export const allTopicSlugs = learningTopics.map((t) => t.slug);
`;

  fs.writeFileSync(CONFIG_FILE, code, 'utf-8');
  console.log(`Successfully generated config file at ${CONFIG_FILE}`);
}

generateConfig();
