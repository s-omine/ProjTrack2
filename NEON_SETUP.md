# Neon Database Setup Guide

This guide will help you set up Neon DB for persistent storage in your ProjTrack application.

## Prerequisites

1. A Neon account - [Sign up at neon.tech](https://neon.tech)
2. Neon MCP server configured in Cursor

## Setup Steps

### 1. Configure Neon MCP in Cursor

1. Open Cursor Settings → Features → MCP Servers
2. Add the Neon MCP server with your API key from [Neon Console](https://console.neon.tech)

### 2. Create a Neon Project

Once the MCP is configured, you can create a project. The code is ready to use with Neon once configured.

### 3. Get Your Connection String

From the Neon console:
1. Go to your project dashboard
2. Click on "Connection Details"
3. Copy the PostgreSQL connection string (format: `postgresql://user:password@hostname.neon.tech/dbname`)

### 4. Configure Environment Variables

Add your Neon connection string to the `.env` file in the `agent/` directory:

```bash
cd projtrack/agent
```

Create or edit `.env`:

```env
# OpenAI API Key (required)
OPENAI_API_KEY=sk-your-key-here

# Neon Database Connection (optional)
NEON_DATABASE_URL=postgresql://user:password@hostname.neon.tech/dbname
```

### 5. Install Dependencies

The database dependencies (`asyncpg` and `psycopg2-binary`) have been added to `pyproject.toml`. Install them:

```bash
cd agent
uv sync
```

**Note**: If you see `ModuleNotFoundError: No module named 'asyncpg'`, run the command above to install the dependencies.

### 6. Start the Application

```bash
cd ..
npm run dev
```

## How It Works

### Database Schema

The application automatically creates a `proverbs` table with the following structure:

```sql
CREATE TABLE proverbs (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
)
```

### State Persistence

- The agent maintains its state both in-memory (for CopilotKit synchronization) and in the database (for persistence)
- When you add or modify proverbs, they are automatically saved to the database
- On startup, the application loads existing proverbs from the database

### Fallback Behavior

If the database is not configured or unavailable:
- The application will continue to work with in-memory state only
- A warning message will be displayed at startup
- No data will persist between restarts

## Testing the Setup

1. Start the application
2. Add some proverbs through the chat interface
3. Restart the application
4. The proverbs should still be there (loaded from database)

## Troubleshooting

### "Database not configured" Warning

- Check that `NEON_DATABASE_URL` is set in `agent/.env`
- Verify the connection string format
- Ensure you copied the complete connection string

### Connection Errors

- Verify your Neon project is active
- Check that the connection string includes the correct credentials
- Ensure your IP address is not blocked by Neon

### Authentication Errors

- Regenerate your Neon API key if needed
- Ensure the MCP server credentials are up to date in Cursor settings

## Next Steps

Once Neon is connected, you can:
- Verify the MCP tools are available
- Create or manage database branches
- Monitor database usage in the Neon console
- Scale your database as needed

