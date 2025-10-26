# Technical Context: ProjTrack2

## Technologies Used

### Frontend Stack
- **Next.js 15.3.2**: React framework with App Router
- **React 19**: UI library
- **TypeScript 5**: Type-safe JavaScript
- **Tailwind CSS 4**: Utility-first styling
- **CopilotKit 1.10.6**: AI integration framework
  - `@copilotkit/react-core`: Core CopilotKit functionality
  - `@copilotkit/react-ui`: UI components
  - `@copilotkit/runtime`: Runtime integration
  - `@ag-ui/client`: Agent communication protocol

### Backend Stack
- **Python 3.12+**: Programming language
- **PydanticAI**: AI agent framework
  - `pydantic-ai-slim[ag-ui]`: Core framework with AG-UI integration
  - `pydantic-ai-slim[openai]`: OpenAI model support
- **uvicorn**: ASGI server
- **python-dotenv**: Environment variable management
- **logfire**: Logging and observability

### Development Tools
- **npm/pnpm**: Node.js package manager
- **uv**: Python package manager
- **concurrently**: Run multiple processes simultaneously
- **ESLint**: Code linting
- **PostCSS**: CSS processing

## Development Setup

### Prerequisites
```bash
# System requirements
- Node.js 20+
- Python 3.12+
- uv (Python package manager)
- OpenAI API key
```

### Installation Process
1. Clone the repository
2. Run `npm install` (or pnpm/yarn/bun install)
   - This automatically runs `install:agent` via postinstall hook
3. Create `.env` file in `agent/` folder:
   ```
   OPENAI_API_KEY=sk-...your-key...
   ```
4. Start development servers:
   ```bash
   npm run dev
   ```

### Automated Setup Scripts
- `scripts/setup-agent.sh` (Unix) / `setup-agent.bat` (Windows)
- `scripts/run-agent.sh` (Unix) / `run-agent.bat` (Windows)

### Development Workflow

#### Running Development Servers
```bash
# Both servers simultaneously
npm run dev

# Frontend only
npm run dev:ui

# Agent only  
npm run dev:agent

# With debug logging
npm run dev:debug
```

#### Build & Production
```bash
# Build Next.js app
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## Technical Constraints

### Environment Variables
- **Required**: `OPENAI_API_KEY` in `agent/.env`
- Frontend runs on port 3000 (default)
- Agent runs on port 8000

### Dependencies
- Node.js 20+ required for Next.js 15
- Python 3.12+ for modern PydanticAI features
- OpenAI API access (paid account)

### Browser Support
- Modern browsers with React 19 support
- No IE11 or old browser support

## Configuration Files

### Frontend Configuration
- `package.json`: Dependencies and scripts
- `tsconfig.json`: TypeScript configuration
- `next.config.ts`: Next.js configuration
- `eslint.config.mjs`: Linting rules
- `postcss.config.mjs`: CSS processing
- `.gitignore`: Git ignore patterns

### Backend Configuration
- `agent/pyproject.toml`: Python dependencies and project metadata
- `agent/uv.lock`: Dependency lock file
- `agent/.env`: Environment variables (not committed)

## File Structure

```
projtrack/
├── agent/                    # Python backend
│   ├── src/
│   │   ├── agent.py         # Agent logic
│   │   └── main.py          # Server entry
│   ├── pyproject.toml       # Python config
│   └── .env                 # API keys (local only)
│
├── src/                      # Next.js frontend
│   ├── app/                 # App Router
│   │   ├── api/copilotkit/ # API route
│   │   ├── page.tsx        # Main page
│   │   └── layout.tsx      # Layout wrapper
│   ├── components/          # React components
│   └── lib/                 # Utilities
│
├── scripts/                  # Setup scripts
├── public/                  # Static assets
└── package.json            # Frontend config
```

## Dependencies

### Critical Frontend Dependencies
```json
{
  "@copilotkit/react-core": "1.10.6",
  "@copilotkit/react-ui": "1.10.6",
  "@copilotkit/runtime": "1.10.6",
  "next": "15.3.2",
  "react": "^19.0.0"
}
```

### Critical Backend Dependencies
```toml
dependencies = [
    "pydantic-ai-slim[ag-ui]",
    "pydantic-ai-slim[openai]",
    "uvicorn",
    "python-dotenv",
    "logfire>=4.10.0"
]
```

## API Endpoints

### Frontend API Route
- `/api/copilotkit` - POST endpoint for CopilotKit communication

### Agent Endpoints
- `http://localhost:8000/` - Main agent endpoint (AG-UI protocol)

## Environment Setup

### Local Development
- Hot reload enabled for both frontend and backend
- Concurrent execution with auto-restart
- Debug mode available for detailed logging

### Production Considerations
- Environment variables must be properly configured
- Build optimization enabled
- SSR/SSG optimization
- API security considerations

