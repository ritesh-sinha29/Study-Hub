import fs from "fs";
import path from "path";
import { parsePythonToMarkdown } from "./parse-python";
import { parseCppToMarkdown } from "./parse-cpp";

export interface IndexedDoc {
  topicSlug: string;
  filename: string;
  title: string;
  content: string;
  tokens: Set<string>;
}

let searchIndex: IndexedDoc[] | null = null;
let lastIndexTime = 0;
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes cache in development mode

// Stopwords to filter out from queries & content for better keyword matching
const STOPWORDS = new Set([
  "what", "is", "how", "to", "the", "a", "an", "of", "in", "and", "for", "with",
  "about", "on", "at", "by", "from", "this", "that", "these", "those", "why",
  "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do",
  "does", "did", "can", "could", "should", "would", "will", "i", "you", "he", "she",
  "it", "we", "they", "me", "him", "her", "us", "them", "my", "your", "his", "its"
]);

function tokenize(text: string): Set<string> {
  const words = text.toLowerCase().match(/\b[a-z0-9]{2,}\b/g) || [];
  return new Set(words.filter(word => !STOPWORDS.has(word)));
}

// Recursively scan a directory for files
function getFilesRecursively(dir: string): string[] {
  let results: string[] = [];
  if (!fs.existsSync(dir)) return [];

  const list = fs.readdirSync(dir);
  for (const file of list) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getFilesRecursively(filePath));
    } else {
      const ext = path.extname(file).toLowerCase();
      if (ext === ".md" || ext === ".py" || ext === ".cpp") {
        results.push(filePath);
      }
    }
  }
  return results;
}

// Build the search index by reading and parsing files from disk
async function buildIndex(): Promise<IndexedDoc[]> {
  const contentDir = path.join(process.cwd(), "src", "content", "learning");
  const index: IndexedDoc[] = [];

  if (!fs.existsSync(contentDir)) {
    console.warn("⚠️ Content directory not found:", contentDir);
    return [];
  }

  // Scan topic folders directly from disk
  const topics = fs.readdirSync(contentDir);
  for (const topicSlug of topics) {
    const topicPath = path.join(contentDir, topicSlug);
    if (!fs.statSync(topicPath).isDirectory()) continue;

    const filePaths = getFilesRecursively(topicPath);
    for (const filePath of filePaths) {
      try {
        const relativeFilename = path.relative(topicPath, filePath).replace(/\\/g, "/");
        let content = fs.readFileSync(filePath, "utf-8");
        const fileExt = path.extname(filePath).toLowerCase();
        
        // Clean Title from filename
        const baseName = path.basename(filePath, fileExt);
        const title = baseName
          .replace(/^\d+[-_]/, "")
          .replace(/[-_]/g, " ")
          .replace(/\b\w/g, c => c.toUpperCase());

        // Parse code comments if python or cpp
        if (fileExt === ".py") {
          content = parsePythonToMarkdown(content, title);
        } else if (fileExt === ".cpp") {
          content = parseCppToMarkdown(content, title);
        }

        const tokens = tokenize(`${topicSlug} ${title} ${content}`);
        index.push({
          topicSlug,
          filename: relativeFilename,
          title,
          content,
          tokens
        });
      } catch (err) {
        console.error(`❌ Failed to index file: ${filePath}`, err);
      }
    }
  }

  console.log(`✅ Indexed ${index.length} course documents successfully.`);
  return index;
}

// Retrieve the search index with cache logic
export async function getSearchIndex(): Promise<IndexedDoc[]> {
  const now = Date.now();
  const isDev = process.env.NODE_ENV === "development";

  if (!searchIndex || (isDev && now - lastIndexTime > CACHE_DURATION)) {
    searchIndex = await buildIndex();
    lastIndexTime = now;
  }
  return searchIndex;
}

// Search local course knowledge base
export async function searchLocalCourses(query: string): Promise<string> {
  const index = await getSearchIndex();
  const queryTokens = tokenize(query);

  if (queryTokens.size === 0) return "";

  const scoredDocs = index.map(doc => {
    let score = 0;
    
    // Check keyword intersection matches
    for (const token of queryTokens) {
      // Boost score if topic slug matches a query token
      if (doc.topicSlug.toLowerCase() === token) {
        score += 25;
      }

      if (doc.tokens.has(token)) {
        // High weight for title matches
        const titleLower = doc.title.toLowerCase();
        if (titleLower.includes(token)) {
          score += 15;
        } else {
          score += 2;
        }

        // Add small score based on term frequency in body content
        const regex = new RegExp(`\\b${token}\\b`, "gi");
        const matches = doc.content.match(regex);
        if (matches) {
          score += Math.min(matches.length * 0.5, 5); // cap frequency score to prevent spamming
        }
      }
    }

    return { doc, score };
  });

  // Filter out zero matches and sort by score descending
  const matches = scoredDocs
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 2); // Get top 2 matching documents

  if (matches.length === 0) {
    return "No matching local course material found for this query.";
  }

  // Format matches into a structured text context block
  return matches
    .map(({ doc, score }, idx) => {
      const maxCharLength = 800;
      const contentExcerpt = doc.content.length > maxCharLength 
        ? doc.content.slice(0, maxCharLength) + "\n\n...(content truncated due to length)..."
        : doc.content;

      return `[Document #${idx + 1}]
Course Topic Slug: ${doc.topicSlug}
Lesson File: ${doc.filename}
Lesson Title: ${doc.title}
Relevance Score: ${score}
Content:
"""
${contentExcerpt}
"""`;
    })
    .join("\n\n========================================\n\n");
}
