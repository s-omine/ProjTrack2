import type { Metadata } from "next";

import { CopilotKit } from "@copilotkit/react-core";
import { StackProvider, StackTheme } from "@stackframe/stack/react";
import { stackServerApp } from "@/stack";
import "./globals.css";
import "@copilotkit/react-ui/styles.css";

export const metadata: Metadata = {
  title: "ProjTrack2 - AI Agent Platform",
  description: "AI-powered project tracking with CopilotKit and PydanticAI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={"antialiased"}>
        <StackProvider app={stackServerApp}>
          <StackTheme>
            <CopilotKit runtimeUrl="/api/copilotkit" agent="my_agent">
              {children}
            </CopilotKit>
          </StackTheme>
        </StackProvider>
      </body>
    </html>
  );
}
