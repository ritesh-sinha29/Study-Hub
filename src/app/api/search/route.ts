import { NextResponse } from "next/server";

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const query = searchParams.get("query");

  if (!query) {
    return new NextResponse(
      JSON.stringify({ error: "Missing query parameter." }),
      { status: 400, headers: { "Content-Type": "application/json" } }
    );
  }

  // 1. Try Tavily Search API if configured
  if (process.env.TAVILY_API_KEY) {
    try {
      const res = await fetch("https://api.tavily.com/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          api_key: process.env.TAVILY_API_KEY,
          query: query,
          max_results: 3,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        const results = data.results?.map((r: any) => `[${r.title}](${r.url}): ${r.content}`).join("\n\n") || "";
        return new NextResponse(JSON.stringify({ result: results }), {
          headers: { "Content-Type": "application/json" },
        });
      }
    } catch (err) {
      console.error("Tavily search failed, falling back...", err);
    }
  }

  // 2. Try Serper (Google Search) API if configured
  if (process.env.SERPER_API_KEY) {
    try {
      const res = await fetch("https://google.serper.dev/search", {
        method: "POST",
        headers: {
          "X-API-KEY": process.env.SERPER_API_KEY,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ q: query, num: 3 }),
      });
      if (res.ok) {
        const data = await res.json();
        const results = data.organic?.map((r: any) => `[${r.title}](${r.link}): ${r.snippet}`).join("\n\n") || "";
        return new NextResponse(JSON.stringify({ result: results }), {
          headers: { "Content-Type": "application/json" },
        });
      }
    } catch (err) {
      console.error("Serper search failed, falling back...", err);
    }
  }

  // 3. Fallback: Return a simulated search result if no keys are set
  const mockResults = `[Python official docs] (https://docs.python.org/3/): Official documentation covering general Python guides and specifications.
[StackOverflow discussion] (https://stackoverflow.com/): Community discussions and solutions about computer science and software development issues related to: "${query}".
[W3Schools reference] (https://www.w3schools.com/): Interactive coding references and syntax guides explaining standard software concepts.

*(Note: No TAVILY_API_KEY or SERPER_API_KEY was found in .env.local; showing simulated web search results)*`;

  return new NextResponse(JSON.stringify({ result: mockResults }), {
    headers: { "Content-Type": "application/json" },
  });
}
