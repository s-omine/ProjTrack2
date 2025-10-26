# CopilotKit Integration Guide

## Overview
This document provides guidance on continuing development with CopilotKit based on the indexed documentation and current project structure.

## Key CopilotKit Concepts

### 1. **Provider Setup** (`layout.tsx`)
```typescript
<CopilotKit runtimeUrl="/api/copilotkit" agent="my_agent">
  {children}
</CopilotKit>
```

### 2. **Shared State** (`useCoAgent)
- Connects UI to agent state
- Bidirectional sync
- Used in: `page.tsx` line 71-78

### 3. **Frontend Actions** (`useCopilotAction`)
- Allow agent to execute frontend operations
- Generative UI for dynamic components
- Used in: `page.tsx` line 15-25, 81-91, 94-100

### 4. **Human-in-the-Loop** (`renderAndWaitForResponse`)
- Requires user approval for sensitive operations
- Wait for user response before continuing
- Used in: `page.tsx` line 94-100

## Template Patterns from CopilotKit

### Pattern 1: Basic Chat Setup
```typescript
import { CopilotChat } from "@copilotkit/react-ui";

<CopilotChat
  instructions="You are a helpful assistant"
  labels={{
    title: "Assistant",
    initial: "How can I help?"
  }}
/>
```

### Pattern 2: Context Injection (`useCopilotReadable`)
```typescript
import { useCopilotReadable } from "@copilotkit/react-core";

useCopilotReadable({
  description: "Current user data",
  value: userData
});
```

### Pattern 3: Runtime Configuration
The API route pattern (`route.ts`):
```typescript
const runtime = new CopilotRuntime({
  agents: {
    "my_agent": new HttpAgent({url: "http://localhost:8000/"}),
  }   
});
```

## Recommended Next Steps

### 1. Add Context Management
Implement `useCopilotReadable` to share app context with agent:
```typescript
useCopilotReadable({
  description: "Current page",
  value: { route: "/dashboard", userId: "123" }
});
```

### 2. Expand Agent Tools
Add more Python tools in `agent.py`:
```python
@agent.tool
def process_data(ctx: RunContext[StateDeps[YourState]], data: str) -> str:
    """Process user data"""
    return processed_data
```

### 3. Create New UI Components
Build custom generative UI:
```typescript
useCopilotAction({
  name: "display_data",
  render: ({ args }) => <DataVisualization data={args.data} />
})
```

### 4. Implement Error Handling
Use CopilotKit error observability:
```typescript
```typescript
<CopilotKit
  onError={(errorEvent) => {
    console.error("Error:", errorEvent);
    // Send to monitoring service
  }}
>
```

## Documentation References

### Getting Started
- Quickstart: https://docs.copilotkit.ai/direct-to-llm/guides/quickstart
- Pydantic AI: https://docs.copilotkit.ai/pydantic-ai

### Features
- Shared State: https://docs.copilotkit.ai/pydantic-ai/shared-state
- Generative UI: https://docs.copilotkit.ai/pydantic-ai/generative-ui
- Frontend Actions: https://docs.copilotkit.ai/pydantic-ai/frontend-actions
- Human-in-the-Loop: https://docs.copilotkit.ai/pydantic-ai/human-in-the-loop

### Advanced
- CopilotKit Premium: https://docs.copilotkit.ai/premium/overview
- Observability: https://docs.copilotkit.ai/premium/observability
- Headless UI: https://docs.copilotkit.ai/premium/headless-ui

## Codebase Integration Points

### Frontend (Next.js)
1. **Provider**: `src/app/layout.tsx` - Wraps app with CopilotKit
2. **API Route**: `src/app/api/copilotkit/route.ts` - Connects to agent
3. **Main UI**: `src/app/page.tsx` - Demonstrates features
4. **Components**: `src/components/` - Reusable React components

### Backend (Python)
1. **Agent**: `agent/src/agent.py` - Define tools and state
2. **Server**: `agent/src/main.py` - FastAPI with AG-UI
3. **Database**: Optional integration for persistence

## Template Location
The project follows patterns from CopilotKit examples:
- `examples/coagents-starter` - Similar starter setup
- `examples/coagents-travel` - Travel app with full features
- `examples/coagents-qa-text` - Q&A implementation

## Key Hooks Reference

### State Management
- `useCoAgent<T>()` - Connect to agent state
- `useCopilotReadable()` - Share app context
- `useCopilotChat()` - Chat interface (if not using CopilotSidebar)

### Actions & Tools
- `useCopilotAction()` - Frontend actions with Generative UI
- `useCoAgentStateRender()` - Render agent state changes
- `useHumanInTheLoop()` - Wait for user response

### Advanced
- `useCopilotAuthenticatedAction_c()` - Require authentication
- `useLangGraphInterrupt()` - LangGraph-specific interrupts
- `useCopilotAdditionalInstructions()` - Dynamic instructions

## Architecture Flow

```
User → UI Component → useCoAgent/useCopilotAction
                      ↓
              CopilotKit Runtime
                      ↓
              API Route (Next.js)
                      ↓
              AG-UI Protocol
                      ↓
              PydanticAI Agent
                      ↓
              FastAPI Server
```

## Best Practices

1. **State Management**: Use `useCoAgent` for bidirectional state
2. **Tool Design**: Keep agent tools focused and atomic
3. **Error Handling**: Implement proper error boundaries
4. **Type Safety**: Leverage TypeScript throughout
5. **Testing**: Test agent tools independently
6. **Documentation**: Document custom tools and state structures

## Common Patterns

### Pattern: CRUD Operations
```python
@agent.tool
def create_item(ctx: RunContext, name: str) -> StateSnapshotEvent:
    # Add item to state
    ctx.deps.state.items.append(name)
    return StateSnapshotEvent(...)

@agent.tool  
def read_items(ctx: RunContext) -> list[str]:
    return ctx.deps.state.items

@agent.tool
def delete_item(ctx: RunContext, index: int) -> StateSnapshotEvent:
    # Remove item
    return StateSnapshotEvent(...)
```

### Pattern: Conditional UI Rendering
```typescript
useCopilotAction({
  name: "conditional_render",
  render: ({ args, status }) => {
    if (status === "executing") return <LoadingSpinner />
    if (status === "complete") return <ResultDisplay {...args} />
    return <WaitingState />
  }
})
```

### Pattern: Multi-Step Workflows
```typescript
useCopilotAction({
  name: "multi_step",
  renderAndWaitForResponse: ({ respond, status, args }) => {
    // Step 1: Collect info
    // Step 2: Show preview
    // Step 3: Request confirmation
    return <WorkflowStep steps={args.currentStep} />
  }
})
```

