---
enact: "2.0.0"
name: "alice/analysis/code-reviewer"
description: "AI-powered code review tool that analyzes code quality, suggests improvements, and identifies potential issues"
version: "1.0.0"
license: "MIT"
tags: ["llm", "code-review", "analysis", "ai"]

inputSchema:
  type: object
  properties:
    code:
      type: string
      description: "Source code to review"
    language:
      type: string
      description: "Programming language"
      enum: ["python", "javascript", "typescript", "go", "rust", "java"]
    focus:
      type: string
      description: "Specific focus area for the review"
      enum: ["security", "performance", "readability", "best-practices", "all"]
      default: "all"
  required: ["code", "language"]

outputSchema:
  type: object
  properties:
    summary:
      type: string
      description: "Overall assessment"
    issues:
      type: array
      items:
        type: object
        properties:
          severity:
            type: string
            enum: ["critical", "high", "medium", "low", "info"]
          category:
            type: string
          description:
            type: string
          suggestion:
            type: string
    score:
      type: number
      description: "Code quality score (0-100)"

annotations:
  title: "AI Code Reviewer"
  readOnlyHint: true
  idempotentHint: false
  destructiveHint: false
  openWorldHint: false
---

# AI Code Reviewer

An LLM-driven tool that performs comprehensive code reviews. This tool has **no `command` field**, meaning it's executed by having an LLM interpret these instructions.

## What This Tool Does

Analyzes source code and provides:
1. **Quality Assessment** - Overall code quality score
2. **Issue Detection** - Security, performance, and maintainability issues
3. **Improvement Suggestions** - Specific recommendations with examples
4. **Best Practices** - Language-specific conventions and patterns

## Instructions for LLM Execution

When executing this tool, follow these steps:

### 1. Parse the Input
Extract the `code`, `language`, and optional `focus` parameters from the input.

### 2. Analyze the Code

Perform analysis based on the focus area:

#### Security Review
- SQL injection vulnerabilities
- XSS vulnerabilities
- Insecure cryptography
- Hardcoded secrets
- Input validation issues

#### Performance Review
- Inefficient algorithms (O(n²) vs O(n log n))
- Unnecessary loops or iterations
- Memory leaks
- Database query optimization
- Caching opportunities

#### Readability Review
- Clear variable and function names
- Code organization and structure
- Comment quality and coverage
- Consistent formatting
- Function complexity (cyclomatic complexity)

#### Best Practices Review
- Language-specific idioms
- Design patterns
- Error handling
- Testing coverage considerations
- Documentation completeness

### 3. Assign Severity Levels

Use these criteria:
- **Critical** - Security vulnerabilities, data loss risks
- **High** - Significant performance issues, major bugs
- **Medium** - Code smells, maintainability concerns
- **Low** - Minor style issues, small optimizations
- **Info** - Suggestions, alternative approaches

### 4. Calculate Quality Score

Base score on:
- Number and severity of issues (40%)
- Code organization and clarity (30%)
- Best practices adherence (20%)
- Documentation quality (10%)

### 5. Format Output

Return a JSON object matching the `outputSchema`:
```json
{
  "summary": "Overall assessment...",
  "issues": [
    {
      "severity": "high",
      "category": "security",
      "description": "SQL injection vulnerability on line 42",
      "suggestion": "Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))"
    }
  ],
  "score": 73
}
```

## Example Usage

```bash
enact run alice/analysis/code-reviewer --args '{
  "code": "def get_user(user_id):\n    query = \"SELECT * FROM users WHERE id = \" + user_id\n    return db.execute(query)",
  "language": "python",
  "focus": "security"
}'
```

Expected output:
```json
{
  "summary": "Critical security vulnerability detected: SQL injection risk",
  "issues": [
    {
      "severity": "critical",
      "category": "security",
      "description": "SQL injection vulnerability in get_user function",
      "suggestion": "Use parameterized queries instead of string concatenation"
    }
  ],
  "score": 20
}
```

## LLM-Driven Tool Characteristics

This tool demonstrates key features of LLM-driven tools:

1. **No deterministic command** - Execution depends on LLM interpretation
2. **Rich instructions** - Detailed guidance in the Markdown body
3. **Flexible analysis** - Can adapt to different code patterns and contexts
4. **Natural language output** - Human-readable explanations
5. **Complex reasoning** - Multi-step analysis requiring understanding of code semantics

## Progressive Disclosure

For more detailed guidance on specific review types, see [RESOURCES.md](RESOURCES.md).

---

**Note:** This is an LLM-driven tool. The quality and accuracy of reviews depend on the capabilities of the executing LLM.
