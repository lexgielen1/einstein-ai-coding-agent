# AI Coding Agent System - Architecture

**Version:** 1.0  
**Date:** April 19, 2026  
**Status:** Planning Phase

---

## Executive Summary

This document defines the architecture for a comprehensive local AI coding and automation system that combines:
- **AI Code Editor** (Cursor-style intelligent coding assistance)
- **Full-Stack App Builder** (Lovable-style natural language to application)
- **Computer Use Automation** (Claude-style browser/desktop automation)
- **Voice Interface** (Jarvis-style conversational control)

The system leverages existing infrastructure (OpenClaw, OpenJarvis, Ollama, LM Studio) running on Mac Studio M3 Ultra to deliver 90%+ local processing while maintaining cloud fallback for complex tasks.

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                         │
├──────────────┬──────────────────┬──────────────┬───────────────┤
│ Voice Input  │  Chat Interface  │  Web Dashboard │  IDE Plugin  │
│ (Jarvis)     │  (OpenJarvis)    │  (Monitoring)  │  (VSCode)    │
└──────┬───────┴────────┬─────────┴───────┬──────┴───────┬───────┘
       │                │                 │              │
       └────────────────┴─────────────────┴──────────────┘
                              ▼
       ┌────────────────────────────────────────────────────┐
       │         EINSTEIN (OpenClaw Orchestrator)           │
       │  - Sub-agent spawning & lifecycle management      │
       │  - Task routing & prioritization                  │
       │  - Context management & memory                    │
       │  - Error handling & recovery                      │
       └────────────────┬───────────────────────────────────┘
                        ▼
       ┌────────────────────────────────────────────────────┐
       │              INTELLIGENCE LAYER                    │
       ├────────────┬──────────────┬──────────────┬─────────┤
       │ LM Studio  │   Ollama     │   Claude     │ Vision  │
       │ Qwen Coder │ Qwen/Llama   │   Sonnet     │ LLaVA   │
       │   (Local)  │   (Local)    │   (Cloud)    │ (Local) │
       └─────┬──────┴──────┬───────┴──────┬───────┴────┬────┘
             │             │              │            │
       ┌─────┴─────────────┴──────────────┴────────────┴─────┐
       │                 EXECUTION MODULES                    │
       ├──────────────┬──────────────┬───────────────────────┤
       │ Code Editor  │ App Builder  │  Computer Use Agent   │
       │  Module      │   Module     │       Module          │
       └──────┬───────┴──────┬───────┴──────────┬────────────┘
              │              │                  │
       ┌──────┴──────────────┴──────────────────┴────────────┐
       │              INFRASTRUCTURE LAYER                    │
       ├──────────────┬──────────────┬──────────────┬────────┤
       │ OpenJarvis   │  Playwright  │  Git/GitHub  │ Storage│
       │ (Sandbox)    │  (Browser)   │  (Version)   │ (Files)│
       └──────────────┴──────────────┴──────────────┴────────┘
```

---

## Core Components

### 1. Orchestration Layer (Einstein/OpenClaw)

**Responsibility:** Central coordinator for all operations

**Key Functions:**
- **Task Decomposition:** Break complex requests into sub-tasks
- **Agent Spawning:** Create specialized sub-agents for each module
- **Context Management:** Maintain conversation history, file context, project state
- **Resource Allocation:** Route tasks to local vs cloud based on complexity
- **Error Recovery:** Handle failures, retry logic, rollback mechanisms
- **Memory System:** Long-term storage of preferences, patterns, project metadata

**Integration Points:**
- Voice interface (Jarvis) for natural language input
- Chat interface (OpenJarvis web UI) for text-based interaction
- Web dashboard for monitoring active tasks
- Memory system (`~/.openclaw/workspace/memory/`)

---

### 2. Intelligence Layer (Multi-Model LLM System)

**Local Models (Mac Studio M3 Ultra):**

| Model | Provider | Use Case | Speed | Quality |
|-------|----------|----------|-------|---------|
| Qwen Coder 32B | LM Studio | Code generation, refactoring | Fast | High |
| Qwen 2.5 32B | Ollama | General reasoning, planning | Fast | High |
| Llama 3.1 70B | Ollama | Complex logic, architecture | Medium | Very High |
| LLaVA 7B | Ollama | Screenshot analysis, UI understanding | Fast | Medium |

**Cloud Fallback:**
- **Claude Sonnet 4.5:** Complex reasoning, large context needs, multi-step planning
- **Claude Vision:** High-accuracy visual tasks (form recognition, complex UI)

**Routing Logic:**
```python
def select_model(task_type, complexity, context_size):
    if task_type == "code_generation":
        if complexity < 500 and context_size < 8000:
            return "lmstudio/qwen-coder-32b"  # Local, fast
        else:
            return "anthropic/claude-sonnet-4-5"  # Cloud, complex
    
    elif task_type == "vision":
        if requires_high_accuracy:
            return "anthropic/claude-vision"
        else:
            return "ollama/llava:7b"  # Local, good enough
    
    elif task_type == "reasoning":
        if context_size < 16000:
            return "ollama/qwen2.5:32b"
        else:
            return "ollama/llama3.1:70b"  # More context capacity
```

**Cost Optimization:**
- Target: 90% local processing
- Cloud calls only for: complex multi-file refactoring, high-stakes code, critical accuracy needs
- Estimated cost: <$5/month for typical usage

---

### 3. Execution Modules

#### Module 1: AI Code Editor

**Architecture:**
```
┌─────────────────────────────────────────┐
│         Code Editor Module              │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────┐    ┌───────────────┐  │
│  │ File Watcher│───▶│Context Builder│  │
│  └─────────────┘    └───────┬───────┘  │
│                              │          │
│  ┌─────────────┐    ┌───────▼───────┐  │
│  │Code Analyzer│◀──▶│  LLM Engine   │  │
│  └─────────────┘    └───────┬───────┘  │
│                              │          │
│  ┌─────────────┐    ┌───────▼───────┐  │
│  │  Diff Gen   │◀───│  Suggestion   │  │
│  └──────┬──────┘    │    Engine     │  │
│         │           └───────────────┘  │
│         ▼                               │
│  ┌─────────────┐                       │
│  │Apply Changes│                       │
│  └─────────────┘                       │
└─────────────────────────────────────────┘
```

**Data Flow:**
1. **File Watcher** detects code changes (save, cursor position)
2. **Context Builder** gathers:
   - Current file content
   - Imported dependencies
   - Related files (same folder, imports)
   - Git history (recent changes)
   - Cursor position & selection
3. **Code Analyzer** extracts:
   - AST (abstract syntax tree)
   - Function signatures
   - Type information
   - Code smells/issues
4. **LLM Engine** generates:
   - Inline completions
   - Refactoring suggestions
   - Bug fixes
   - Documentation
5. **Suggestion Engine** ranks by confidence
6. **Diff Generator** creates precise edits
7. **Apply Changes** writes to file (with undo buffer)

**Key Features:**
- **Multi-file context:** Understands project structure
- **Smart completions:** Context-aware, not just autocomplete
- **Refactoring:** Rename, extract function, change signature
- **Live error detection:** Syntax + logic issues
- **Git integration:** Commit suggestions, diff view

---

#### Module 2: Full-Stack App Builder

**Architecture:**
```
┌──────────────────────────────────────────────┐
│          App Builder Module                  │
├──────────────────────────────────────────────┤
│                                              │
│  Natural Language Input                      │
│          │                                   │
│          ▼                                   │
│  ┌──────────────┐                           │
│  │ Intent Parser│                           │
│  └──────┬───────┘                           │
│         │                                    │
│         ▼                                    │
│  ┌──────────────┐    ┌─────────────────┐   │
│  │ App Planner  │───▶│ Tech Stack      │   │
│  │ (Architect)  │    │ Selector        │   │
│  └──────┬───────┘    └─────────────────┘   │
│         │                                    │
│         ▼                                    │
│  ┌──────────────────────────────────────┐  │
│  │     Component Generation Pipeline     │  │
│  ├──────────────────────────────────────┤  │
│  │ 1. Project scaffolding               │  │
│  │ 2. Database schema                   │  │
│  │ 3. API routes                        │  │
│  │ 4. React components                  │  │
│  │ 5. Styling (Tailwind)                │  │
│  │ 6. Auth setup                        │  │
│  └──────┬───────────────────────────────┘  │
│         │                                    │
│         ▼                                    │
│  ┌──────────────┐    ┌─────────────────┐   │
│  │ Code Gen     │───▶│ File Writer     │   │
│  │ (Multi-step) │    │ (Git init)      │   │
│  └──────────────┘    └─────────────────┘   │
│                                              │
│         │                                    │
│         ▼                                    │
│  ┌──────────────┐    ┌─────────────────┐   │
│  │ Dev Server   │───▶│ Browser Preview │   │
│  │ (Vite)       │    │ (Auto-open)     │   │
│  └──────────────┘    └─────────────────┘   │
└──────────────────────────────────────────────┘
```

**Standard Stack:**
- **Frontend:** React 18 + Vite + Tailwind CSS
- **Backend:** Node.js + Express OR Supabase (for simple CRUD)
- **Database:** PostgreSQL (Supabase) OR SQLite (local dev)
- **Auth:** Supabase Auth OR Clerk
- **Deployment:** Vercel (frontend) + Supabase (backend)

**Generation Pipeline:**
1. **Intent Parser:** Extract app requirements
   - "Recipe app with user accounts" → 
     - Entities: User, Recipe
     - Features: Auth, CRUD recipes, search
     - UI: List view, detail view, form

2. **App Planner:** Create architecture
   - Database schema (tables, relations)
   - API endpoints (REST or GraphQL)
   - Component tree (pages, layouts, components)
   - State management (Context, Zustand, or none)

3. **Component Generation:**
   ```
   For each component:
     - Generate JSX structure
     - Add Tailwind styling
     - Implement state logic
     - Connect to API
     - Add error handling
   ```

4. **File Writing:**
   - Project structure creation
   - Install dependencies (npm)
   - Git initialization
   - Environment setup (.env template)

5. **Dev Server:**
   - `npm run dev`
   - Open browser at localhost:5173
   - Live reload enabled

**Example Output:**
```
~/ai-projects/recipe-app/
├── src/
│   ├── components/
│   │   ├── RecipeList.jsx
│   │   ├── RecipeCard.jsx
│   │   ├── AddRecipeForm.jsx
│   │   └── AuthForm.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── RecipeDetail.jsx
│   │   └── Login.jsx
│   ├── lib/
│   │   └── supabase.js
│   ├── App.jsx
│   └── main.jsx
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

---

#### Module 3: Computer Use Automation

**Architecture:**
```
┌────────────────────────────────────────────┐
│      Computer Use Automation Module        │
├────────────────────────────────────────────┤
│                                            │
│  Task Input (Natural Language)             │
│          │                                 │
│          ▼                                 │
│  ┌──────────────┐                         │
│  │Task Planner  │                         │
│  │ (Multi-step) │                         │
│  └──────┬───────┘                         │
│         │                                  │
│         ▼                                  │
│  ┌──────────────────────────────────┐    │
│  │     Execution Loop                │    │
│  ├──────────────────────────────────┤    │
│  │  While task not complete:         │    │
│  │    1. Take screenshot             │    │
│  │    2. Analyze with LLaVA          │    │
│  │    3. Decide next action          │    │
│  │    4. Execute (click/type/scroll) │    │
│  │    5. Verify result               │    │
│  │    6. Update task state           │    │
│  └──────┬───────────────────────────┘    │
│         │                                  │
│         ▼                                  │
│  ┌──────────────┐    ┌────────────────┐  │
│  │Playwright    │───▶│ Browser        │  │
│  │Controller    │    │ (Chromium)     │  │
│  └──────────────┘    └────────────────┘  │
│                                            │
│  ┌──────────────┐    ┌────────────────┐  │
│  │Vision Model  │───▶│ Action Decider │  │
│  │(LLaVA/Claude)│    │ (LLM)          │  │
│  └──────────────┘    └────────────────┘  │
└────────────────────────────────────────────┘
```

**Action Primitives:**
- **Navigation:** `goto(url)`, `back()`, `forward()`, `refresh()`
- **Interaction:** `click(selector)`, `type(selector, text)`, `select(selector, value)`
- **Scrolling:** `scroll(direction, amount)`
- **Waiting:** `wait_for(selector)`, `wait_for_navigation()`
- **Extraction:** `get_text(selector)`, `get_attribute(selector, attr)`
- **Screenshot:** `take_screenshot(region)`

**Vision-Guided Execution:**
1. **Screenshot Analysis:**
   - Take screenshot (full page or region)
   - Send to LLaVA: "What elements are visible? Where is the login button?"
   - Parse response → element locations

2. **Action Planning:**
   - LLM decides: "To login, I need to: 1) Click email field, 2) Type email, 3) Click password field, 4) Type password, 5) Click submit"
   - Generate action sequence

3. **Execution with Verification:**
   ```python
   for action in action_sequence:
       execute(action)
       screenshot = take_screenshot()
       success = verify_action_completed(screenshot, expected_state)
       if not success:
           retry_with_alternative(action)
   ```

**Error Recovery:**
- **Element not found:** Take screenshot → ask LLaVA for alternative selector
- **Action failed:** Screenshot → analyze error message → suggest fix
- **Unexpected state:** Re-plan remaining steps based on current state

**Safety Mechanisms:**
- **Confirmation prompts** for destructive actions (delete, payment, send)
- **Dry-run mode** (simulate without executing)
- **Action logging** (audit trail)
- **Timeout limits** (max 5min per task)

---

#### Module 4: Voice Interface (Jarvis Integration)

**Architecture:**
```
┌────────────────────────────────────────────┐
│          Voice Interface Module            │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────┐                         │
│  │Wake Word     │  "Hey Einstein"         │
│  │(Porcupine)   │                         │
│  └──────┬───────┘                         │
│         │                                  │
│         ▼                                  │
│  ┌──────────────┐                         │
│  │Audio Capture │  (Microphone)           │
│  └──────┬───────┘                         │
│         │                                  │
│         ▼                                  │
│  ┌──────────────┐                         │
│  │ Whisper STT  │  (Local/OpenAI)         │
│  │ Transcription│                         │
│  └──────┬───────┘                         │
│         │                                  │
│         ▼                                  │
│  ┌──────────────────────────────────┐    │
│  │    Einstein Orchestrator          │    │
│  │  (Process command → spawn agent)  │    │
│  └──────┬───────────────────────────┘    │
│         │                                  │
│         ▼                                  │
│  ┌──────────────┐    ┌────────────────┐  │
│  │ Task Result  │───▶│ Response Gen   │  │
│  │  (JSON)      │    │ (Natural Lang) │  │
│  └──────────────┘    └────────┬───────┘  │
│                               │           │
│                               ▼           │
│  ┌──────────────┐    ┌────────────────┐  │
│  │ TTS Engine   │◀───│ Audio Renderer │  │
│  │(pyttsx3/EL)  │    └────────────────┘  │
│  └──────┬───────┘                         │
│         │                                  │
│         ▼                                  │
│  ┌──────────────┐                         │
│  │ Speaker Out  │                         │
│  └──────────────┘                         │
└────────────────────────────────────────────┘
```

**Voice Processing Pipeline:**

1. **Wake Word Detection:**
   - Porcupine (local, always listening)
   - Low CPU usage (~5%)
   - Custom wake word: "Hey Einstein"

2. **Speech-to-Text (STT):**
   - **Option A:** Whisper local (via whisper.cpp)
     - Pro: Private, offline, free
     - Con: Slower (~2-3s), less accurate
   - **Option B:** OpenAI Whisper API
     - Pro: Fast (<1s), accurate
     - Con: Costs $0.006/min, requires internet

3. **Intent Processing:**
   - Send transcript to Einstein orchestrator
   - Parse intent + parameters
   - Route to appropriate module

4. **Task Execution:**
   - Spawn sub-agent for module
   - Stream progress updates
   - Capture result/error

5. **Response Generation:**
   - LLM converts result to natural language
   - Template: "I've completed [task]. [Result summary]."
   - Handle errors gracefully: "I ran into an issue with [step]. [Suggestion]."

6. **Text-to-Speech (TTS):**
   - **Option A:** pyttsx3 (local)
     - Pro: Free, offline, fast
     - Con: Robotic voice
   - **Option B:** ElevenLabs API
     - Pro: Natural voice, customizable
     - Con: Costs ~$0.01/min

**Conversation Memory:**
- Store context in OpenClaw memory system
- Remember: current project, recent commands, user preferences
- Clear context: "Forget previous conversation"
- Retrieve context: "What was I working on?"

**Voice Commands Examples:**
```
"Write a Python script to scrape HackerNews"
→ Spawns Code Editor module → generates script → saves file → reports

"Build me a todo app with React"
→ Spawns App Builder → creates project → starts dev server → reports

"Check my Gmail for invoice emails"
→ Spawns Computer Use module → opens Gmail → searches → reports count

"What's the status of my current project?"
→ Queries OpenClaw memory → reads task state → reports verbally

"Edit the HomePage component to add a hero section"
→ Spawns Code Editor → modifies component → reports change
```

---

## Data Flow Architecture

### High-Level Flow (Voice → Code → Execution)

```
┌─────────────────────────────────────────────────────────────────┐
│                      DATA FLOW DIAGRAM                          │
└─────────────────────────────────────────────────────────────────┘

User Voice Input
      │
      ▼
[Wake Word Detection] ──✓──▶ [Audio Capture]
      │                           │
      │                           ▼
      │                    [Whisper STT]
      │                           │
      │                           ▼
      │                    "Build a calculator app"
      │                           │
      └───────────────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │  Einstein Orchestrator  │
                    │  (OpenClaw)             │
                    └──────────┬──────────────┘
                               │
                               ├─── Parse intent: "app_builder"
                               │
                               ├─── Extract params: {type: "calculator", stack: "react"}
                               │
                               ├─── Select model: "lmstudio/qwen-coder-32b"
                               │
                               └─── Spawn sub-agent: "app-builder-calculator"
                                              │
                                              ▼
                              ┌───────────────────────────────┐
                              │   App Builder Sub-Agent       │
                              └───────────┬───────────────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    ▼                     ▼                     ▼
            [Plan Architecture]    [Generate Code]      [Setup Project]
                    │                     │                     │
                    │              ┌──────┴──────┐             │
                    │              │             │             │
                    │              ▼             ▼             │
                    │         [Frontend]   [Backend]          │
                    │              │             │             │
                    └──────────────┴─────────────┴─────────────┘
                                          │
                                          ▼
                            ┌──────────────────────────┐
                            │   File System Write      │
                            │  ~/ai-projects/calc-app/ │
                            └───────────┬──────────────┘
                                        │
                                        ▼
                            ┌──────────────────────────┐
                            │  Start Dev Server        │
                            │  (npm run dev)           │
                            └───────────┬──────────────┘
                                        │
                                        ▼
                            ┌──────────────────────────┐
                            │  Open Browser            │
                            │  localhost:5173          │
                            └───────────┬──────────────┘
                                        │
                                        ▼
                    ┌───────────────────────────────────┐
                    │   Report to Einstein              │
                    │   Status: Success                 │
                    │   Location: ~/ai-projects/calc-app│
                    │   URL: http://localhost:5173      │
                    └────────────┬──────────────────────┘
                                 │
                                 ▼
                    ┌───────────────────────────────────┐
                    │   Einstein → Response Generator   │
                    │   "Calculator app ready!"         │
                    └────────────┬──────────────────────┘
                                 │
                                 ▼
                    ┌───────────────────────────────────┐
                    │   TTS Engine                      │
                    │   Audio: "Calculator app ready at │
                    │   localhost 5173"                 │
                    └────────────┬──────────────────────┘
                                 │
                                 ▼
                          [Speaker Output]
```

---

## Storage Architecture

### File System Organization

```
~/.openclaw/workspace/
├── memory/                           # Long-term memory
│   ├── project-contexts/             # Per-project state
│   │   ├── calc-app.json
│   │   └── recipe-app.json
│   ├── user-preferences.json         # Coding style, frameworks
│   └── task-history/                 # Completed tasks log
│
├── ai-projects/                      # Generated projects
│   ├── calc-app/
│   ├── recipe-app/
│   └── hn-scraper/
│
├── code-editor/                      # Code editor module
│   ├── context-cache/                # File contexts (AST, deps)
│   ├── suggestions/                  # Generated suggestions
│   └── undo-buffer/                  # Change history
│
├── automation-logs/                  # Computer use logs
│   ├── task-recordings/              # Screenshot sequences
│   └── action-logs/                  # Executed actions
│
└── voice-interface/                  # Voice module
    ├── audio-cache/                  # Temp audio files
    └── conversation-history/         # Recent dialogs
```

### Database Schema (SQLite - Optional)

```sql
-- Project metadata
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    path TEXT NOT NULL,
    stack TEXT,                    -- "react-vite-tailwind"
    created_at TIMESTAMP,
    last_modified TIMESTAMP,
    status TEXT                    -- "active", "archived"
);

-- Code generation history
CREATE TABLE code_generations (
    id INTEGER PRIMARY KEY,
    project_id INTEGER,
    file_path TEXT,
    prompt TEXT,
    generated_code TEXT,
    model_used TEXT,
    accepted BOOLEAN,
    created_at TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Automation task logs
CREATE TABLE automation_tasks (
    id INTEGER PRIMARY KEY,
    task_description TEXT,
    steps_planned TEXT,            -- JSON array
    steps_executed TEXT,           -- JSON array
    success BOOLEAN,
    error_message TEXT,
    screenshots_path TEXT,         -- Folder with screenshots
    created_at TIMESTAMP,
    duration_seconds INTEGER
);

-- Voice commands
CREATE TABLE voice_commands (
    id INTEGER PRIMARY KEY,
    transcript TEXT,
    intent TEXT,                   -- "code_editor", "app_builder"
    params TEXT,                   -- JSON
    result TEXT,
    created_at TIMESTAMP
);
```

---

## Security & Safety

### Code Execution Sandbox (OpenJarvis)

**Isolation:**
- All generated code runs in OpenJarvis sandbox
- Restricted file system access (only ~/ai-projects/)
- No network access by default (opt-in for API calls)
- Resource limits (CPU, memory, disk)

**Approval System:**
```python
# Before executing generated code
if requires_approval(code):
    show_preview(code)
    user_approval = await prompt_user("Execute this code?")
    if not user_approval:
        cancel_execution()
```

**Approval Triggers:**
- File system writes outside ~/ai-projects/
- Network requests
- System commands (npm install, git commit)
- Database modifications
- Deployment actions

### Browser Automation Safety

**Confirmation Required For:**
- Form submissions (especially payments, emails)
- Deletions
- Account changes
- Data exports

**Dry-Run Mode:**
- Simulate actions without executing
- Show preview of what would happen
- User can review then confirm

**Rate Limiting:**
- Max 10 actions per minute (prevent abuse)
- Max 100 actions per task (prevent runaway loops)

---

## Performance Optimization

### Local Model Caching

**Model Warmup:**
```bash
# Pre-load models on system startup
ollama pull qwen2.5:32b
ollama pull llama3.1:70b
ollama pull llava:7b

# Keep in memory (faster inference)
ollama run qwen2.5:32b "" --keepalive 24h
```

**Context Caching:**
- Cache file contexts (AST, dependencies) to avoid re-parsing
- Invalidate on file modification
- Store in `code-editor/context-cache/`

### Response Time Targets

| Task Type | Target | Local Model | Cloud Fallback |
|-----------|--------|-------------|----------------|
| Inline completion | <500ms | Qwen Coder 32B | - |
| Simple script | <10s | Qwen Coder 32B | Claude (rare) |
| Full app generation | <60s | Qwen Coder 32B | Claude (complex) |
| Browser automation step | <3s | LLaVA + Playwright | Claude vision (ambiguous) |
| Voice response | <2s | Qwen 2.5 32B | - |

### Concurrency

**Sub-Agent Limits:**
- Max 3 concurrent sub-agents (Mac Studio capacity)
- Queue additional tasks
- Priority: Voice commands > Chat > Background

**Model Sharing:**
- Multiple sub-agents can share same model instance
- Ollama handles request queuing internally

---

## Monitoring & Observability

### Metrics to Track

**Performance:**
- Response time per module
- Local vs cloud usage ratio
- Model inference time
- Task success rate

**Quality:**
- Code compilation success rate
- User acceptance rate (suggestions)
- Task completion rate (automation)
- Error frequency

**Usage:**
- Commands per day
- Projects created
- Lines of code generated
- Automation tasks executed

### Dashboard (Web UI)

**Real-Time View:**
```
┌─────────────────────────────────────────┐
│    Einstein AI Coding System            │
├─────────────────────────────────────────┤
│                                         │
│  Active Tasks:                          │
│  ✓ App Builder: recipe-app (85%)       │
│  ⏳ Code Editor: main.jsx (analyzing)   │
│                                         │
│  Models Status:                         │
│  🟢 Qwen Coder 32B (LM Studio)         │
│  🟢 Qwen 2.5 32B (Ollama)              │
│  🟢 LLaVA 7B (Ollama)                  │
│  🔵 Claude Sonnet (Cloud - idle)       │
│                                         │
│  Today's Stats:                         │
│  📊 12 tasks completed                  │
│  💾 95% local processing                │
│  ⚡ Avg response: 8.2s                  │
│  ✅ 92% success rate                    │
│                                         │
│  Recent Projects:                       │
│  • recipe-app (React + Supabase)       │
│  • calc-app (React + local state)      │
│  • hn-scraper (Python + BeautifulSoup) │
└─────────────────────────────────────────┘
```

---

## Integration Points

### OpenClaw Integration

**Memory System:**
```javascript
// Store project context
memory.store('project-contexts/recipe-app.json', {
    name: 'recipe-app',
    stack: 'react-vite-supabase',
    components: ['RecipeList', 'AddRecipe', 'Auth'],
    lastWorkedOn: '2026-04-19T10:30:00Z'
});

// Retrieve context
const context = memory.load('project-contexts/recipe-app.json');
```

**Sub-Agent Spawning:**
```javascript
// Spawn app builder sub-agent
const agent = await openclaw.spawnSubAgent({
    module: 'app-builder',
    task: 'Generate recipe app with React + Supabase',
    model: 'lmstudio/qwen-coder-32b',
    context: {
        userPreferences: { framework: 'react', styling: 'tailwind' },
        projectName: 'recipe-app'
    }
});

// Monitor progress
agent.on('progress', (update) => {
    console.log(`Progress: ${update.step} - ${update.percentage}%`);
});

// Get result
const result = await agent.waitForCompletion();
```

### OpenJarvis Integration

**Code Execution:**
```python
# Execute generated code in sandbox
result = openjarvis.execute(
    code=generated_script,
    language='python',
    timeout=30,
    allowed_paths=['~/ai-projects/hn-scraper/']
)

if result.success:
    print(result.output)
else:
    print(f"Error: {result.error}")
```

### LM Studio Integration

**Code Generation API:**
```javascript
const response = await fetch('http://localhost:1234/v1/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        model: 'qwen-coder-32b',
        messages: [
            { role: 'system', content: 'You are an expert Python developer.' },
            { role: 'user', content: 'Write a script to scrape HackerNews top stories.' }
        ],
        temperature: 0.3,
        max_tokens: 2000
    })
});

const code = response.choices[0].message.content;
```

---

## Deployment Architecture

### Single-Machine Setup (Mac Studio)

All components run locally on Mac Studio M3 Ultra:

**Services:**
- OpenClaw orchestrator (port 8080)
- OpenJarvis sandbox (port 8085)
- LM Studio (port 1234)
- Ollama (port 11434)
- Web dashboard (port 3000)
- Jarvis voice interface (port 5000)

**Resource Allocation:**
- **CPU:** 24 cores (M3 Ultra)
  - 8 cores: LM Studio (Qwen Coder)
  - 8 cores: Ollama (Qwen/Llama)
  - 4 cores: OpenClaw + OpenJarvis
  - 4 cores: System + other
- **RAM:** 128GB
  - 40GB: LM Studio model
  - 40GB: Ollama models
  - 20GB: System cache
  - 28GB: Available
- **GPU:** 76-core GPU (shared)

### Network Architecture

```
Internet
    │
    ▼
[Cloudflare Tunnel] (optional - for remote access)
    │
    ▼
Mac Studio (192.168.1.100)
    │
    ├─── OpenClaw :8080
    ├─── OpenJarvis :8085
    ├─── LM Studio :1234
    ├─── Ollama :11434
    ├─── Dashboard :3000
    └─── Jarvis :5000
```

**Remote Access (Optional):**
- Cloudflare Tunnel for secure remote access
- Access coding system from anywhere
- Voice commands via mobile app

---

## Future Expansion

### Multi-Machine Scaling

**Scenario:** When local capacity insufficient

**Architecture:**
```
Mac Studio (Orchestrator)
    │
    ├─── Local: Code Editor, Voice Interface
    │
    └─── Remote Compute Cluster:
            ├─── GPU Server 1: LLaVA vision (high throughput)
            ├─── GPU Server 2: Code generation (Qwen Coder)
            └─── CPU Server: Browser automation
```

### Cloud Hybrid

**Bursting Strategy:**
- Normalize local capacity at 80%
- Burst to cloud for peaks (Claude API)
- Cost monitoring (alert if >$10/day)

### IDE Plugins

**VSCode Extension:**
- Real-time suggestions
- Inline AI chat
- One-click app generation
- Voice command integration

**Features:**
- Same backend (Einstein orchestrator)
- Native IDE integration
- Faster UX (no browser switch)

---

## Conclusion

This architecture provides a comprehensive foundation for building a local-first AI coding and automation system. Key strengths:

✅ **Local-first:** 90%+ processing on Mac Studio (privacy, speed, cost)  
✅ **Modular:** Clear separation of concerns (easy to extend)  
✅ **Practical:** Leverages existing infrastructure (OpenClaw, OpenJarvis, Ollama)  
✅ **Safe:** Sandboxing, approval systems, dry-run modes  
✅ **Scalable:** Can expand to multi-machine or cloud hybrid  

Next steps: See **IMPLEMENTATION-ROADMAP.md** for phase-by-phase execution plan.
