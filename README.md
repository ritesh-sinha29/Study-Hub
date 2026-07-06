# 🎓 Learning Portal

A premium, interactive developer learning portal and documentation dashboard. This platform dynamically indexes and serves revision notes, cheat sheets, and study guides for core developer topics.

## 🚀 Features

- **Dynamic Content Indexing**: Auto-generates routing configs by scanning markdown and Python files inside the `src/content/learning` folder.
- **Tech Stack Coverage**: Comprehensive study guides for:
  - **Python Learning**: Core fundamentals, object-oriented programming, decorators, async-await, and advanced features.
  - **FastAPI**: Path/query parameters, dependency injection, CRUD operations with SQLite, JWT authentication, and background tasks.
  - **LangChain & LangGraph**: Agentic workflows, state graphs, and LLM orchestration.
  - **RAG (Retrieval-Augmented Generation)**: Vector search, document processing, and semantic search guides.
  - **DSA (Data Structures & Algorithms)**: Fundamental algorithms and data structures.
- **Interactive UI**: Clean, modern dark-themed dashboard built with React 19, Next.js 16/Next.js App Router, Tailwind CSS v4, and Lucide Icons.
- **Syntax Highlighting**: Beautiful code blocks powered by PrismJS.

---

## 🛠️ Technology Stack

- **Framework**: [Next.js](https://nextjs.org/) (App Router)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **Components**: [Shadcn UI](https://ui.shadcn.com/) & [Base UI](https://base-ui.com/)
- **Markdown Rendering**: [react-markdown](https://github.com/remarkjs/react-markdown) & [remark-gfm](https://github.com/remarkjs/remark-gfm)
- **Code Highlighting**: [PrismJS](https://prismjs.com/)

---

## 📂 Repository Structure

- `src/app/` - Next.js routing and page layouts
- `src/components/` - UI components (layout, dashboard, visual guides)
- `src/content/learning/` - Raw markdown (`.md`) and python (`.py`) study guides sorted by topic
- `src/config/` - Auto-generated configuration file (`learning.ts`)
- `scripts/` - Utilities and automation tools

---

## 💻 Getting Started

### 1. Install Dependencies

Using `pnpm`:
```bash
pnpm install
```

### 2. Run the Development Server

Start the application locally:
```bash
pnpm dev
```
> **Note**: This will automatically run `scripts/generate_config.js` to index your latest guides and then start the Next.js development server at [http://localhost:3000](http://localhost:3000).

### 3. Add New Content
Simply place a `.md` or `.py` file into any folder under `src/content/learning/`. The dev script will parse the title from the first `#` header, format it, and append it to the sidebar navigation automatically!
