import { stackServerApp } from "@/stack";

// Stack Auth handler route
// This catches all /handler/* routes and processes them with Stack Auth
export async function POST(req: Request) {
  return stackServerApp.handleRequest(req);
}

export async function GET(req: Request) {
  return stackServerApp.handleRequest(req);
}

export const runtime = "nodejs";

