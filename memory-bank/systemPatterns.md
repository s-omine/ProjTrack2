# System Patterns: ProjTrack2

## Architecture Pattern
**Full-Stack AI Application with Separation of Concerns**

### Component Relationships
```
┌─────────────────┐
│   Next.js UI    │
│   (Frontend)    │
│                 │
│  React +        │
│  CopilotKit     │
└────────┬────────┘
         │
         │ HTTP/AG-UI Protocol
         │
┌────────▼────────┐
│  CopilotKit     │
│  API Route      │
│  (Middleware)   │
└────────┬────────┘
         │
         │ Agent Connection
         │
┌────────▼────────┐
│ PydanticAI      │
│ Agent           │
│ (Backend)       │
└─────────────────┘
```

## Key Technical Decisions

### 1. Separation of Frontend and Backend
- **Frontend**: React + Next.js for modern web experience
- **Backend**: Python + PydanticAI for AI logic
- **Communication**: AG-UI protocol over HTTP

### 2. State Management Pattern
- **Centralized State**: Managed in Python agent
- **Reactive Updates**: Frontend listens to state changes
- **Bidirectional Sync**: Frontend can trigger state updates

**Implementation:**
- `ProverbsState` in Python defines the state schema
- `useCoAgent` hook in React subscribes to state
- State changes propagate automatically

### 3. Tool Registration Pattern
**Agent Side (Python):**
```python
@agent.tool
def tool_name(ctx: RunContext[StateDeps[StateType]], param: type) -> ReturnType:
    # Tool logic here
    pass
```

**Frontend Side (TypeScript):**
```typescript
useCopilotAction({
    name: "action_name",
    parameters: [...],
    handler: ({ params }) => { /* action logic */ }
})
```

### 4. Generative UI Pattern
Components are defined in frontend but rendered by AI decisions:
```typescript
useCopilotAction({
    name: "generate_ui",
    render: ({ args }) => <DynamicComponent {...args} />
})
```

### 5. Human-in-the-Loop Pattern
Critical actions require user interaction before completion:
```typescript
useCopilotAction({
    renderAndWaitForResponse: ({ respond, status }) => (
        <ConfirmationDialog onConfirm={() => respond("confirmed")} />
    )
})
```

## Design Patterns in Use

### Dependency Injection
- State passed via `StateDeps` to agent tools
- `RunContext` provides access to dependencies
- Clean separation of concerns

### Observer Pattern
- Frontend observes state changes
- Automatic re-rendering on state updates
- No manual state synchronization needed

### Facade Pattern
- CopilotKit abstracts communication complexity
- Simple API for complex multi-agent systems
- Single entry point for agent interactions

### Strategy Pattern
- Different tool types (sync, async, state-changing)
- Pluggable tool implementations
- Easy to extend with new capabilities

## Component Structure

### Agent Components (`agent/src/`)
- `agent.py`: Agent definition, state schema, tools
- `main.py`: FastAPI server setup and execution

### Frontend Components (`src/`)
- `app/page.tsx`: Main UI with CopilotKit integration
- `app/layout.tsx`: Root layout with CopilotKit provider
- `components/`: React components for UI elements
- `lib/types.ts`: Shared TypeScript types

## Communication Flow

### State Update Flow
1. User requests action → Frontend triggers tool
2. Frontend sends request → CopilotKit API route
3. API routes to agent → PydanticAI agent
4. Agent executes tool → Updates state
5. Agent returns StateSnapshotEvent
6. Frontend receives update → UI re-renders

### Tool Execution Flow
1. Agent decides to call tool
2. Tool executes and returns result
3. Result sent to frontend via AG-UI
4. Frontend displays result if needed

## Best Practices Implemented

### Error Handling
- Environment variable validation
- Type checking at compile time (TypeScript)
- Runtime validation (Pydantic models)

### Code Organization
- Clear separation: agent/ vs src/
- Consistent naming conventions
- Modular component structure

### Performance
- Lazy loading of components
- Efficient state updates
- Minimal re-renders

### Developer Experience
- Hot reload for both frontend and backend
- Type safety throughout
- Clear error messages
- Comprehensive logging

