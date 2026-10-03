import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { homedir } from "node:os";
import { join } from "node:path";

const exec = promisify(execFile);
const SEMBLE_BIN = join(homedir(), ".cargo", "bin", "semble_rs");

async function run(args, timeout = 60000) {
  const { stdout, stderr } = await exec(SEMBLE_BIN, args, {
    timeout,
    maxBuffer: 1024 * 1024 * 10,
  });
  return stderr ? `${stdout}\n${stderr}` : stdout;
}

const server = new McpServer({
  name: "semble",
  version: "1.0.0",
});

server.tool(
  "search",
  "Hybrid BM25+semantic code search. Returns ranked snippets with line numbers. Use compact=true for token-efficient output.",
  {
    query: z.string().describe("Search query (symbol name or natural language)"),
    path: z.string().describe("Project directory path to search"),
    compact: z.boolean().default(true).describe("Compact output for token savings (recommended)"),
    top_k: z.number().default(10).describe("Max results to return"),
  },
  async ({ query, path, compact, top_k }) => {
    const args = ["search", query, path, "-k", String(top_k)];
    if (compact) args.push("--compact");
    const result = await run(args);
    return { content: [{ type: "text", text: result }] };
  }
);

server.tool(
  "find_related",
  "Find code similar to a specific file location. Useful for discovering related logic.",
  {
    location: z.string().describe("File path and optional line (e.g. src/auth.ts:42)"),
    path: z.string().describe("Project directory path"),
    top_k: z.number().default(5).describe("Max results"),
  },
  async ({ location, path, top_k }) => {
    const args = ["find-related", location, path, "-k", String(top_k)];
    const result = await run(args);
    return { content: [{ type: "text", text: result }] };
  }
);

server.tool(
  "deps",
  "Show what a file depends on (imports) and what symbols it defines.",
  {
    file: z.string().describe("File path to analyze"),
  },
  async ({ file }) => {
    const result = await run(["deps", file]);
    return { content: [{ type: "text", text: result }] };
  }
);

server.tool(
  "impact",
  "Show all files transitively affected if a file changes. Use before refactoring.",
  {
    file: z.string().describe("File path to analyze impact for"),
    path: z.string().describe("Project directory path"),
  },
  async ({ file, path }) => {
    const result = await run(["impact", file, path]);
    return { content: [{ type: "text", text: result }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
