# Authentication Setup Guide for ProjTrack2

## Overview

Neon Auth has been provisioned for your project. This guide will help you set up Stack Auth for user authentication in your Next.js application.

## Current Status

✅ **Neon Auth**: Provisioned in database  
✅ **Database Schema**: `neon_auth.users_sync` table created  
⚠️ **Stack Auth**: Not yet configured in the application

## Getting Your Neon Auth Credentials

Since Neon Auth is already provisioned, you need to retrieve your credentials from the Neon Console:

1. Visit [Neon Console](https://console.neon.tech)
2. Select your project: **ProjTrack2** (ID: `dark-mode-26041820`)
3. Navigate to **Settings** → **Neon Auth**
4. Copy the following credentials:
   - `NEXT_PUBLIC_STACK_PROJECT_ID`
   - `NEXT_PUBLIC_STACK_PUBLISHABLE_CLIENT_KEY`
   - `STACK_SECRET_SERVER_KEY`

## Setting Up Stack Auth

### Step 1: Install Stack Auth SDK

```bash
cd projtrack
npm install @stackframe/stack
```

### Step 2: Configure Environment Variables

Create a `.env` file in the `projtrack` directory:

```env
# Add these variables to projtrack/.env
NEXT_PUBLIC_STACK_PROJECT_ID=your-project-id-here
NEXT_PUBLIC_STACK_PUBLISHABLE_CLIENT_KEY=your-publishable-key-here
STACK_SECRET_SERVER_KEY=your-secret-key-here
```

**Note:** Both `.env` and `.env.local` work for Next.js. In this project, use `.env` since the gitignore already excludes it. `.env.local` and `.env` are treated the same by Next.js for this setup.

### Step 3: Initialize Stack Auth

Run the Stack Auth initialization command:

```bash
npx @stackframe/init-stack . --no-browser
```

This will:
- Add `@stackframe/stack` to your dependencies
- Create a `stack.ts` file for StackServerApp setup
- Wrap the root layout with `StackProvider` and `StackTheme`
- Create a Suspense boundary in `app/loading.tsx`
- Create auth routes in `app/handler/[...stack]/page.tsx`

### Step 4: Configure Authentication Routes

The initialization creates auth handlers, but you may need to update them based on your needs:

**Auth Routes Created:**
- `/handler/sign-in`
- `/handler/sign-up`
- `/handler/forgot-password`

### Step 5: Add Authentication to Your Layout

After initialization, your `layout.tsx` should look like this:

```tsx
import { CopilotKit } from "@copilotkit/react-core";
import { StackProvider, StackTheme } from "@stackframe/stack/react";
import { StackServerApp } from "@stackframe/stack";
import "./globals.css";
import "@copilotkit/react-ui/styles.css";

// Initialize Stack Server App
const projectId = process.env.NEXT_PUBLIC_STACK_PROJECT_ID!;
const stackServerApp = new StackServerApp({ projectId });

export default async function RootLayout({
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
```

### Step 6: Add Authentication Components

Create user authentication UI using Stack Auth components:

**Option A: Use Pre-built Components**

```tsx
import { SignIn, SignUp, UserButton } from "@stackframe/stack/react";

// In your page
export default function Page() {
  return (
    <div>
      <SignIn />
      <SignUp />
      <UserButton />
    </div>
  );
}
```

**Option B: Custom Components**

```tsx
import { OAuthButtonGroup, MagicLinkSignIn, CredentialSignIn } from "@stackframe/stack/react";

export default function LoginPage() {
  return (
    <div>
      <OAuthButtonGroup />
      <MagicLinkSignIn />
      <CredentialSignIn />
    </div>
  );
}
```

### Step 7: Protect Pages

**Client Component:**
```tsx
"use client";
import { useUser } from "@stackframe/stack/react";

export default function ProtectedPage() {
  const user = useUser({ or: "redirect" });
  
  return <div>Welcome, {user.displayName}!</div>;
}
```

**Server Component:**
```tsx
import { stackServerApp } from "@/stack";

export default async function ServerProtectedPage() {
  const user = await stackServerApp.getUser({ or: "redirect" });
  
  return <div>Welcome, {user.displayName}!</div>;
}
```

### Step 8: Create Middleware for Route Protection

Create `middleware.ts` in the `projtrack` root:

```tsx
import { NextRequest, NextResponse } from "next/server";
import { stackServerApp } from "./stack";

export async function middleware(request: NextRequest) {
  const user = await stackServerApp.getUser();
  
  if (!user) {
    return NextResponse.redirect(new URL('/handler/sign-in', request.url));
  }
  
  return NextResponse.next();
}

export const config = { 
  matcher: '/protected/:path*' 
};
```

## Database Integration

Neon Auth is already integrated with your database:

- **Schema**: `neon_auth`
- **Table**: `users_sync`
- **Sync**: User data is automatically synced from Stack Auth to Neon

## Testing Authentication

1. **Start your development server:**
   ```bash
   npm run dev
   ```

2. **Visit these URLs:**
   - http://localhost:3000/handler/sign-up
   - http://localhost:3000/handler/sign-in

3. **Test sign-up/sign-in flows**

## Configuration Files

After setup, you'll have these new files:

```
projtrack/
├── .env                                # Auth credentials (not committed)
├── stack.ts                            # Stack Server App configuration
├── middleware.ts                       # Route protection
├── app/
│   ├── loading.tsx                    # Suspense boundary
│   ├── handler/
│   │   └── [...stack]/
│   │       └── page.tsx               # Auth route handlers
│   └── layout.tsx                      # Updated with StackProvider
```

## Security Notes

- Never commit `.env` to version control (already in .gitignore)
- Keep `STACK_SECRET_SERVER_KEY` secure (server-side only)
- Use environment-specific credentials for production

## Troubleshooting

### "NEXT_PUBLIC_STACK_PROJECT_ID is not defined"
- Check that `.env` exists in `projtrack/` directory
- Verify environment variables are correct
- Restart development server

### "Cannot connect to Stack Auth"
- Verify API keys in Neon Console
- Check that Neon Auth is enabled for your project
- Ensure database connection is working

### Authentication not working
- Check browser console for errors
- Verify Stack Auth credentials are correct
- Ensure `@stackframe/stack` is properly installed

## Next Steps

After authentication is set up, you can:

1. **Add protected routes** for agent functionality
2. **Create user-specific state** in the agent
3. **Implement role-based access control**
4. **Add user profiles and settings**
5. **Integrate with agent proverbs storage per user**

## Resources

- [Stack Auth Documentation](https://stack-auth.com/docs)
- [Stack Auth GitHub](https://github.com/stackframejs/stack)
- [Neon Auth Guide](https://neon.tech/docs/auth)
- [CopilotKit Docs](https://docs.copilotkit.ai)

## Important Notes

⚠️ **Do NOT use NextAuth.js or better-auth** - Use Stack Auth only as recommended by Neon Auth integration.

⚠️ **Do NOT create SignIn/SignUp components manually** - Use the ones from `@stackframe/stack/react` or generated by `init-stack`.

⚠️ **Server-side initialization** - Always use `StackServerApp` for server components, not `StackClientApp`.

