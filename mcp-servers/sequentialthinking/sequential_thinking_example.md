# Sequential Thinking MCP Server Example

This file demonstrates how to use the Sequential Thinking MCP server with Claude.

## Basic Usage Example

When using the Sequential Thinking tool, you'll follow this pattern:

1. Start with an initial thought
2. Continue with subsequent thoughts, building on previous thinking
3. Optionally revise previous thoughts when needed
4. Conclude when you've reached a solution

## Sample Prompt Structure

```javascript
// Initial thought
{
  "thought": "I need to understand how to solve this problem...",
  "nextThoughtNeeded": true,
  "thoughtNumber": 1,
  "totalThoughts": 5
}

// Subsequent thought
{
  "thought": "Building on my previous thinking, I can see that...",
  "nextThoughtNeeded": true,
  "thoughtNumber": 2,
  "totalThoughts": 5
}

// Revising a previous thought
{
  "thought": "Upon further reflection, I need to reconsider...",
  "nextThoughtNeeded": true,
  "thoughtNumber": 3,
  "totalThoughts": 6,
  "isRevision": true,
  "revisesThought": 1
}

// Final thought with solution
{
  "thought": "Therefore, the solution is...",
  "nextThoughtNeeded": false,
  "thoughtNumber": 6,
  "totalThoughts": 6
}
```

## Sample Problems to Try

1. **Problem Decomposition**: Break down a complex programming task into manageable steps
2. **Algorithm Design**: Work through designing an algorithm step by step
3. **Debugging**: Analyze possible causes of a bug systematically
4. **System Architecture**: Plan out components of a system with dependencies

## Benefits of Sequential Thinking

- Captures evolving understanding as you work through a problem
- Allows for revision when initial assumptions prove incorrect
- Provides a clear history of your reasoning process
- Helps avoid jumping to conclusions before considering all aspects