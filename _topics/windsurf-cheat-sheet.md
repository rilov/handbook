---
title: "Windsurf IDE Cheat Sheet"
category: GenAI Dev Tools
tags:
  - windsurf
  - ide
  - ai-coding
  - cascade
summary: Print-friendly quick reference for Windsurf IDE - keyboard shortcuts, Cascade commands, and essential features.
---

# Windsurf IDE Cheat Sheet

**Windsurf** - AI-native IDE with Cascade (agentic AI flow) 

---

## ESSENTIAL SHORTCUTS

| **General** | | **Cascade AI** | | **Editing** | |
|-------------|---|----------------|---|-------------|---|
| `Cmd+Shift+P` | Command Palette | `Cmd+L` | Cascade Chat | `Cmd+/` | Toggle Comment |
| `Cmd+P` | Quick Open | `Cmd+I` | Inline Edit | `Cmd+D` | Select Next |
| `Cmd+,` | Settings | `Cmd+Shift+L` | New Session | `Cmd+X` | Cut Line |
| `Cmd+B` | Toggle Sidebar | `Cmd+K` | Quick Command | `Alt+Up/Down` | Move Line |
| `Cmd+J` | Toggle Panel | `Esc` | Cancel AI | `Cmd+Enter` | Insert Below |
| `Ctrl+\`` | Terminal | | | `Cmd+Shift+K` | Delete Line |

| **Navigation** | | **Multi-Cursor** | | **Search** | |
|----------------|---|------------------|---|------------|---|
| `Cmd+G` | Go to Line | `Alt+Click` | Add Cursor | `Cmd+F` | Find |
| `Cmd+Shift+O` | Go to Symbol | `Cmd+Alt+Up/Down` | Cursor Above/Below | `Cmd+H` | Replace |
| `Cmd+T` | Symbol in Workspace | `Cmd+D` | Select Next | `Cmd+Shift+F` | Find in Files |
| `F12` | Go to Definition | `Cmd+Shift+L` | Select All Occurrences | `Cmd+Shift+H` | Replace in Files |
| `Shift+F12` | Go to References | `Cmd+U` | Undo Cursor | `Alt+Enter` | Select All Matches |

---

## CASCADE COMMANDS & PROMPTS

| **@mentions** | **Description** | **Common Prompts** | **Use Case** |
|---------------|-----------------|-------------------|--------------|
| `@workspace` | Reference workspace | `Explain this code` | Understand logic |
| `@file` | Reference file | `Add comments` | Document code |
| `@folder` | Reference folder | `Refactor this` | Improve structure |
| `@code` | Reference selection | `Fix this bug` | Debug issues |
| `@terminal` | Reference terminal | `Write tests` | Generate tests |
| `@problems` | Reference errors | `Optimize this` | Improve performance |
| `@web` | Search web | `Add error handling` | Make robust |

**Cascade Modes:** Chat (Q&A) • Edit (Modify) • Generate (Create) • Debug (Fix) • Refactor (Restructure)

---

## QUICK ACTIONS

| **Files** | | **Git** | | **Debug** | |
|-----------|---|---------|---|-----------|---|
| `Cmd+N` | New File | `Ctrl+Shift+G` | Source Control | `F9` | Toggle Breakpoint |
| `Cmd+S` | Save | `Cmd+Enter` | Commit (SCM) | `F5` | Start/Continue |
| `Cmd+W` | Close | `+` icon | Stage | `F10` | Step Over |
| `Cmd+Shift+T` | Reopen | `-` icon | Unstage | `F11` | Step Into |
| `Cmd+\` | Split Editor | | | `Shift+F5` | Stop Debug |

---

## CASCADE BEST PRACTICES

**✅ DO:**
• Be specific • Use `@file` and `@workspace` • Break tasks into steps • Review before accepting

**❌ DON'T:**
• Give vague instructions • Accept without understanding • Skip testing • Forget context

**Example Workflow:**
```
1. Select code → Cmd+L
2. "Fix this bug: [describe]"
3. Review → Accept/Iterate
```

---

## CASCADE CAPABILITIES

| **Can Do ✅** | **Cannot Do ❌** |
|---------------|------------------|
| Generate code, functions, tests | Run code directly |
| Explain algorithms, document | Access external APIs |
| Refactor, extract functions | Make architecture decisions |
| Debug, suggest fixes | Replace code review |
| Generate unit tests, mocks | Execute without review |

---

## PRODUCTIVITY TIPS

1. **Repetitive Tasks:** `"Update all API endpoints to new base URL"`
2. **@mentions:** `"@workspace find all TODO comments"`
3. **Multi-Cursor:** `Cmd+D` to select next, edit all at once
4. **Split Editors:** `Cmd+\` for side-by-side
5. **Zen Mode:** `Cmd+K Z` for focus
6. **Snippets:** Settings → User Snippets

---

## COMMON ISSUES

| **Issue** | **Fix** |
|-----------|---------|
| Cascade not responding | Restart Windsurf |
| Slow performance | Close unused editors |
| Git conflicts | Use Source Control panel |
| Extension errors | Disable/reinstall |
| Terminal not working | `Ctrl+\`` to toggle |

---

## ADVANCED SHORTCUTS

| **Selection** | | **Code Folding** | | **Display** | |
|---------------|---|------------------|---|-------------|---|
| `Cmd+A` | Select All | `Cmd+Alt+[` | Fold | `Cmd+K Z` | Zen Mode |
| `Cmd+L` | Select Line | `Cmd+Alt+]` | Unfold | `Cmd+=` | Zoom In |
| `Alt+Shift+Right` | Expand Selection | `Cmd+K Cmd+0` | Fold All | `Cmd+-` | Zoom Out |
| `Alt+Shift+Left` | Shrink Selection | `Cmd+K Cmd+J` | Unfold All | `Cmd+0` | Reset Zoom |

---

## WORKSPACE & SETTINGS

| **Workspace** | | **Essential Settings** | |
|---------------|---|------------------------|---|
| `Cmd+O` | Open Folder | Font Size | Settings → Editor: Font Size |
| File → Add Folder | Add to Workspace | Theme | `Cmd+K Cmd+T` |
| File → Save Workspace | Save | Auto Save | Settings → Files: Auto Save |
| File → Open Recent | Switch | Format on Save | Settings → Editor: Format On Save |

**Recommended Extensions:** Prettier • ESLint • GitLens • Python • Docker

---

## WINDSURF-SPECIFIC FEATURES

### Prompt Files (.prompt)

**Location:** `.windsurf/prompts/` or project root

| **Feature** | **Description** |
|-------------|----------------|
| Reusable prompts | Save common prompts as files |
| Template variables | Use `{{variable}}` for dynamic content |
| Share across team | Version control prompt files |
| Quick access | Reference with `@prompt` |

**Example `.windsurf/prompts/review.prompt`:**
```
Review this code for:
- Security vulnerabilities
- Performance issues
- Best practices
- Code smells
```

**Usage:** `@prompt review` in Cascade

### Instruction Files (.instructions)

**Location:** `.windsurf/instructions/` or project root

| **Type** | **Purpose** | **Example** |
|----------|-------------|-------------|
| Project instructions | Project-specific rules | `project.instructions` |
| Component instructions | Component guidelines | `api.instructions` |
| Style instructions | Coding style rules | `style.instructions` |

**Example `.windsurf/instructions/project.instructions`:**
```
Project: E-commerce API
Language: TypeScript
Framework: Express.js

Rules:
- Always use async/await, never callbacks
- All API endpoints must have error handling
- Use Zod for validation
- Write tests for all endpoints
```

**Cascade automatically reads these files for context**

### .windsurfrules File

**Location:** Project root (`.windsurfrules`)

**Purpose:** Global project rules for Cascade

**Example `.windsurfrules`:**
```yaml
# Code Style
indent: 2 spaces
quotes: single
semicolons: true

# Conventions
naming:
  functions: camelCase
  classes: PascalCase
  constants: UPPER_SNAKE_CASE

# Preferences
testing: Jest
linter: ESLint
formatter: Prettier

# AI Behavior
code_generation:
  - Add TypeScript types
  - Include error handling
  - Write inline comments for complex logic
  - Generate tests alongside code
```

### Context Files

| **File** | **Purpose** |
|----------|-------------|
| `.windsurf/context.md` | Project context for AI |
| `.windsurf/architecture.md` | System architecture |
| `.windsurf/conventions.md` | Team conventions |
| `README.md` | Auto-included by Cascade |

### Cascade Memory

**Windsurf remembers:**
- Previous conversations (session-based)
- File edits and context
- Project structure
- Common patterns you use

**Clear memory:** Start new session with `Cmd+Shift+L`

### Workspace Settings

**`.vscode/settings.json` (Windsurf-specific):**
```json
{
  "cascade.autoContext": true,
  "cascade.includeTests": true,
  "cascade.maxTokens": 4096,
  "cascade.temperature": 0.7,
  "cascade.model": "claude-3-5-sonnet"
}
```

---

## WINDSURF PROJECT STRUCTURE

```
project/
├── .windsurf/
│   ├── prompts/           # Reusable prompt files
│   │   ├── review.prompt
│   │   ├── test.prompt
│   │   └── refactor.prompt
│   ├── instructions/      # Context instructions
│   │   ├── project.instructions
│   │   ├── api.instructions
│   │   └── style.instructions
│   ├── context.md         # Project context
│   └── architecture.md    # System design
├── .windsurfrules         # Global project rules
├── .vscode/
│   └── settings.json      # Windsurf settings
└── README.md              # Auto-included
```

---

## ADVANCED CASCADE FEATURES

### Multi-File Operations

| **Command** | **Action** |
|-------------|------------|
| `@workspace refactor X to Y` | Refactor across all files |
| `@folder update imports` | Update folder imports |
| `@workspace find pattern` | Search entire workspace |

### Cascade Agents

**Specialized agents for tasks:**
- **Code Agent** - Write/modify code
- **Review Agent** - Code review
- **Test Agent** - Generate tests
- **Debug Agent** - Fix bugs
- **Docs Agent** - Write documentation

**Trigger:** Cascade auto-selects based on prompt

### Cascade Modes Deep Dive

| **Mode** | **When to Use** | **Example** |
|----------|-----------------|-------------|
| **Chat** | Questions, explanations | "How does auth work?" |
| **Edit** | Modify existing code | Select code + "Refactor this" |
| **Generate** | Create new code | "Create user model" |
| **Debug** | Fix errors | "Fix this TypeError" |
| **Refactor** | Improve structure | "Extract to function" |

---

## QUICK REFERENCE CARD

**Most Used:**
```
Cmd+L          → Cascade Chat       @workspace    → Reference workspace
Cmd+I          → Inline Edit        @file         → Reference file
Cmd+P          → Quick Open         Explain this  → Understand code
Cmd+Shift+P    → Command Palette    Fix this      → Debug
Cmd+F          → Find               Refactor      → Improve structure
Cmd+D          → Select Next        Add tests     → Generate tests
Ctrl+`         → Terminal
```

---

## CASCADE FLOWS

**Sequential Tasks:**
```
1. "@workspace analyze codebase"
2. "Create refactoring plan"
3. "Implement step by step"
4. "Generate tests"
```

**Custom Commands (settings):**
```json
{
  "cascade.customCommands": {
    "review": "Review for security and performance",
    "doc": "Add comprehensive documentation",
    "test": "Generate unit tests with edge cases"
  }
}
```

**Using Prompt Files:**
```
1. Create .windsurf/prompts/review.prompt
2. In Cascade: "@prompt review @file mycode.ts"
3. Cascade uses prompt template + file context
```

---

**Resources:** [windsurf.ai/docs](https://windsurf.ai/docs) • `Cmd+K Cmd+S` (Shortcuts) • `Cmd+,` (Settings)  
**Version:** Windsurf 1.0+ • **Updated:** January 2026

**💡 Pro Tip:** Print landscape, laminate for durable desk reference!
