# Frontend Building Guide - ProjTrack2

## What Was Indexed

### CopilotKit Documentation
- ✅ Complete documentation indexed from docs.copilotkit.ai
- ✅ Codebase patterns reviewed from GitHub examples
- ✅ Key features and patterns identified

### Key Findings

#### 1. **Architecture Pattern** (Current Implementation)
```
Frontend (Next.js + React)
    ↓ useCoAgent / useCopilotAction
CopilotKit Runtime (runtimeUrl="/api/copilotkit")
    ↓ HttpAgent (AG-UI Protocol)
Backend (PydanticAI + FastAPI)
```

#### 2. **Current Features Implemented**
- ✅ Shared State (proverbs list)
- ✅ Generative UI (weather cards)
- ✅ Frontend Actions (theme color changes)
- ✅ Human-in-the-Loop (moon mission confirmation)
- ✅ Agent tools in Python

#### 3. **Available CopilotKit Patterns**

**A. Provider Setup** (Already Done)
```typescript
// src/app/layout.tsx
<CopilotKit runtimeUrl="/api/copilotkit" agent="my_agent">
  {children}
</CopilotKit>
```

**B. Shared State** (Already Used)
```typescript
const { state, setState } = useCoAgent<AgentState>({
  name: "my_agent",
  initialState: { proverbs: [...] }
})
```

**C. Frontend Actions** (Already Used)
```typescript
useCopilotAction({
  name: "action_name",
  parameters: [...],
  handler: ({ param }) => { /* logic */ }
})
```

## How to Continue Building

### Step 1: Add Context to Agent

**Pattern**: Use `useCopilotReadable` to share app state

```typescript
// In any component
import { useCopilotReadable } from "@copilotkit/react-core";

export function YourComponent() {
  const [userData, setUserData] = useState({
    id: "123",
    name: "John",
    role: "developer"
  });

  // Make this available to agent
  useCopilotReadable({
    description: "Current user information",
    value: userData,
  });

  return <YourUI />;
}
```

### Step 2: Add New Agent Tools

**In Python** (`agent/src/agent.py`):

```python
@agent.tool
def your_new_tool(ctx: RunContext[StateDeps[ProverbsState]], param: str) -> str:
    """Description of what this tool does."""
    # Your logic here
    return "result"
```

### Step 3: Create New Generative UI Components

**In TypeScript** (`src/app/page.tsx` or new component):

```typescript
useCopilotAction({
  name: "display_custom_component",
  parameters: [
    { name: "data", type: "string", required: true }
  ],
  render: ({ args }) => {
    return <CustomComponent data={args.data} />
  }
})
```

### Step 4: Add Human-in-the-Loop Confirmations

```typescript
useCopilotAction({
  name: "sensitive_operation",
  renderAndWaitForResponse: ({ respond, status, args }) => {
    if (status === "complete") {
      return <SuccessMessage />
    }
    return (
      <ConfirmationDialog
        onConfirm={() => respond("confirmed")}
        onCancel={() => respond("canceled")}
      />
    );
  }
})
```

## Recommended Features to Add

### 1. **User Profile Management**
```typescript
// Frontend
useCopilotAction({
  name: "update_profile",
  parameters: [
    { name: "name", type: "string" },
    { name: "email", type: "string" }
  ],
  handler: ({ name, email }) => {
    // Update user profile
  }
})

// Backend (Python)
@agent.tool
def update_user_profile(
  ctx: RunContext[StateDeps[YourState]], 
  name: str, 
  email: str
) -> StateSnapshotEvent:
    """Update user profile"""
    ctx.deps.state.userProfile = { name, email }
    return StateSnapshotEvent(...)
```

### 2. **Data Visualization**
```typescript
useCopilotAction({
  name: "show_chart",
  parameters: [
    { name: "data", type: "object" },
    { name: "chart_type", type: "string" }
  ],
  render: ({ args }) => (
    <Chart 
      data={args.data} 
      type={args.chart_type}
    />
  )
})
```

### 3. **File Operations**
```typescript
useCopilotAction({
  name: "handle_file",
  parameters: [
    { name: "filename", type: "string" },
    { name: "content", type: "string" }
  ],
  handler: async ({ filename, content }) => {
    // Save file or process content
  }
})
```

### 4. **Multi-Step Workflows**
```typescript
useCopilotAction({
  name: "complex_workflow",
  renderAndWaitForResponse: ({ respond, status, args }) => {
    const currentStep = args.step || 1;
    
    switch (currentStep) {
      case 1:
        return <Step1 onNext={(data) => respond({ step: 2, ...data })} />
      case 2:
        return <Step2 onNext={(data) => respond({ step: 3, ...data })} />
      case 3:
        return <Step3 onComplete={() => respond({ done: true })} />
      default:
        return <Complete />
    }
  }
})
```

## Component Structure Template

### New Component File Structure
```
src/components/your-feature/
├── index.tsx           # Main component
├── types.ts           # TypeScript types
└── hooks.ts           # Custom hooks (optional)
```

### Example Component
```typescript
// src/components/your-feature/index.tsx
"use client";

import { useCopilotAction } from "@copilotkit/react-core";

export function YourFeature() {
  useCopilotAction({
    name: "feature_action",
    description: "Performs a feature action",
    parameters: [
      { name: "input", type: "string", required: true }
    ],
    handler: ({ input }) => {
      console.log("Action triggered with:", input);
    },
    render: ({ args, status }) => {
      return (
        <div>
          <p>Status: {status}</p>
          <p>Input: {args.input}</p>
        </div>
      );
    }
  });

  return <div>Your Feature UI</div>;
}
```

## Testing Patterns

### Test Agent Tools
```python
# agent/tests/test_tools.py
async def test_get_proverbs():
    state = ProverbsState(proverbs=["Test"])
    result = await get_proverbs(ctx_deps(state))
    assert result == ["Test"]
```

### Test Frontend Actions
```typescript
// src/components/__tests__/your-feature.test.tsx
describe("YourFeature", () => {
  it("renders correctly", () => {
    render(<YourFeature />);
    // assertions
  });
});
```

## Debugging Tools

### 1. Enable Dev Console
```typescript
<CopilotKit 
  runtimeUrl="/api/copilotkit" 
  agent="my_agent"
  showDevConsole={true}
>
```

### 2. Add Console Logging
```typescript
useCopilotAction({
  name: "debug_action",
  handler: ({ param }) => {
    console.log("Action called with:", param);
  }
})
```

### 3. Python Debugging
```python
@agent.tool
def debug_tool(ctx: RunContext[StateDeps[ProverbsState]], param: str) -> str:
    print(f"Tool called with: {param}")
    print(f"Current state: {ctx.deps.state}")
    return "debugged"
```

## Documentation Links

- **Quickstart**: https://docs.copilotkit.ai/direct-to-llm/guides/quickstart
- **Shared State**: https://docs.copilotkit.ai/pydantic-ai/shared-state
- **Generative UI**: https://docs.copilotkit.ai/pydantic-ai/generative-ui
- **Frontend Actions**: https://docs.copilotkit.ai/pydantic-ai/frontend-actions
- **Human-in-the-Loop**: https://docs.copilotkit.ai/pydantic-ai/human-in-the-loop
- **Pydantic AI Docs**: https://docs.copilotkit.ai/pydantic-ai

## Next Steps Checklist

- [ ] Decide on new features to implement
- [ ] Design state structure in Python
- [ ] Create new React components
- [ ] Add agent tools in Python
- [ ] Implement useCopilotAction hooks
- [ ] Test state synchronization
- [ ] Add error handling
- [ ] Document new features
- [ ] Test with real user flows

