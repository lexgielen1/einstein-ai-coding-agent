# Implementation Roadmap - AI Coding Agent System

**Version:** 1.0  
**Date:** April 19, 2026  
**Timeline:** 5 weeks (modular, can adjust)

---

## Overview

This roadmap breaks down the implementation into 5 phases, each building on the previous. Each phase has clear deliverables and success criteria.

**Estimated Timeline:** 5 weeks (full-time) or 10 weeks (part-time)  
**Team Size:** 1-2 developers  
**Dependencies:** Mac Studio M3 Ultra, OpenClaw, OpenJarvis, Ollama, LM Studio (already set up)

---

## Phase 0: Pre-Implementation Setup (2-3 days)

**Goal:** Ensure all dependencies are configured and tested

### Tasks

#### 1. Verify Infrastructure

```bash
# Check OpenClaw
openclaw --version
openclaw gateway status

# Check Ollama models
ollama list
# Expected: qwen2.5:32b, llama3.1:70b, llava:7b

# Check LM Studio
curl http://localhost:1234/v1/models
# Expected: qwen-coder-32b

# Check OpenJarvis
cd /path/to/openjarvis
python --version  # Should be 3.10+
```

#### 2. Create Project Structure

```bash
cd ~/.openclaw/workspace

# Create directory structure
mkdir -p ai-coding-system/{modules,scripts,tests,docs}
mkdir -p ai-coding-system/modules/{code-editor,app-builder,computer-use,voice-interface}
mkdir -p ai-projects  # For generated projects
mkdir -p code-editor/{context-cache,suggestions,undo-buffer}
mkdir -p automation-logs/{task-recordings,action-logs}
mkdir -p voice-interface/{audio-cache,conversation-history}
```

#### 3. Install Dependencies

```bash
# Node.js dependencies
npm init -y
npm install express ws playwright @anthropic-ai/sdk dotenv

# Python dependencies (for OpenJarvis integration)
pip install openai anthropic beautifulsoup4 requests

# Voice interface
pip install SpeechRecognition pyttsx3 pvporcupine  # Wake word
```

#### 4. Configuration Files

**config.json:**
```json
{
  "models": {
    "code_generation": {
      "primary": "lmstudio/qwen-coder-32b",
      "fallback": "anthropic/claude-sonnet-4-5"
    },
    "reasoning": {
      "primary": "ollama/qwen2.5:32b",
      "fallback": "ollama/llama3.1:70b"
    },
    "vision": {
      "primary": "ollama/llava:7b",
      "fallback": "anthropic/claude-vision"
    }
  },
  "thresholds": {
    "local_complexity_max": 500,
    "local_context_max": 8000,
    "cloud_fallback_enabled": true
  },
  "paths": {
    "projects": "~/ai-projects",
    "cache": "~/.openclaw/workspace/code-editor/context-cache"
  }
}
```

### Deliverables

- ✅ All models responding (Ollama, LM Studio)
- ✅ Project directory structure created
- ✅ Dependencies installed
- ✅ Config file created
- ✅ Test script passes (connects to all services)

### Success Criteria

```bash
# Run health check
node scripts/health-check.js
# Expected output:
# ✓ OpenClaw: OK
# ✓ Ollama: OK (3 models)
# ✓ LM Studio: OK (qwen-coder-32b)
# ✓ OpenJarvis: OK
```

---

## Phase 1: Foundation - Voice to Code Pipeline (Week 1)

**Goal:** Create minimal working system: voice command → code generation → file save

### Architecture Focus

```
Voice Input → Whisper → Einstein → LM Studio → Generated Code → File System
```

### Tasks

#### Day 1-2: Voice Input Integration

**Script:** `voice-interface/voice-capture.py`

```python
import speech_recognition as sr
import pvporcupine

# Wake word detection
porcupine = pvporcupine.create(keywords=['jarvis'])

def listen_for_wake_word():
    """Listen for 'Hey Einstein' wake word"""
    # Implementation using Porcupine
    pass

def capture_voice_command():
    """Capture audio after wake word"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            # Option 1: Local Whisper (slower, private)
            text = recognizer.recognize_whisper(audio)
            # Option 2: OpenAI Whisper API (faster, $)
            # text = recognizer.recognize_whisper_api(audio)
            return text
        except Exception as e:
            return None
```

**Integration with Einstein:**
```javascript
// modules/voice-interface/voice-handler.js
const { exec } = require('child_process');

async function processVoiceCommand(transcript) {
    // Send to Einstein orchestrator
    const response = await fetch('http://localhost:8080/api/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            source: 'voice',
            command: transcript 
        })
    });
    
    return response.json();
}
```

#### Day 3-4: Code Generation Pipeline

**Script:** `modules/code-editor/code-generator.js`

```javascript
async function generateCode(prompt, language = 'python') {
    // Call LM Studio (Qwen Coder)
    const response = await fetch('http://localhost:1234/v1/chat/completions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            model: 'qwen-coder-32b',
            messages: [
                { 
                    role: 'system', 
                    content: `You are an expert ${language} developer. Generate clean, working code.` 
                },
                { 
                    role: 'user', 
                    content: prompt 
                }
            ],
            temperature: 0.3,
            max_tokens: 2000
        })
    });
    
    const data = await response.json();
    const code = data.choices[0].message.content;
    
    // Extract code from markdown if needed
    const codeMatch = code.match(/```(?:python|javascript|bash)?\n([\s\S]*?)\n```/);
    return codeMatch ? codeMatch[1] : code;
}
```

#### Day 5: File Management & Execution

**Script:** `modules/code-editor/file-manager.js`

```javascript
const fs = require('fs').promises;
const path = require('path');

async function saveGeneratedCode(code, filename, projectName = 'default') {
    const projectPath = path.join(
        process.env.HOME, 
        'ai-projects', 
        projectName
    );
    
    // Create project directory if needed
    await fs.mkdir(projectPath, { recursive: true });
    
    const filePath = path.join(projectPath, filename);
    await fs.writeFile(filePath, code, 'utf8');
    
    return filePath;
}

async function executeCode(filePath) {
    // Use OpenJarvis sandbox
    const result = await fetch('http://localhost:8085/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            file: filePath,
            timeout: 30
        })
    });
    
    return result.json();
}
```

#### Day 6-7: End-to-End Integration & Testing

**Main orchestrator:** `modules/voice-interface/voice-orchestrator.js`

```javascript
async function handleVoiceCommand(transcript) {
    console.log(`Received: "${transcript}"`);
    
    // Parse intent
    const intent = parseIntent(transcript);
    // Example: "write a python script to scrape hackernews"
    // → { action: 'generate_code', language: 'python', task: 'scrape hackernews' }
    
    if (intent.action === 'generate_code') {
        // Generate code
        const code = await generateCode(
            intent.task, 
            intent.language
        );
        
        // Save to file
        const filename = `${intent.task.replace(/\s+/g, '_')}.${intent.language === 'python' ? 'py' : 'js'}`;
        const filePath = await saveGeneratedCode(
            code, 
            filename, 
            intent.task.replace(/\s+/g, '-')
        );
        
        // Execute (optional)
        if (intent.execute !== false) {
            const result = await executeCode(filePath);
            console.log('Execution result:', result);
        }
        
        // Generate voice response
        const response = `Script ready at ${filePath}`;
        await speakResponse(response);
        
        return { success: true, filePath, code };
    }
}

function parseIntent(transcript) {
    // Simple regex-based parsing (improve later with LLM)
    const match = transcript.match(/write a (\w+) script to (.+)/i);
    if (match) {
        return {
            action: 'generate_code',
            language: match[1].toLowerCase(),
            task: match[2],
            execute: true
        };
    }
    return { action: 'unknown' };
}

async function speakResponse(text) {
    // TTS using pyttsx3
    const { exec } = require('child_process');
    return new Promise((resolve) => {
        exec(`python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('${text}'); engine.runAndWait()"`, resolve);
    });
}
```

### Testing Scenarios

**Test 1: Simple Python Script**
```
Voice: "Write a Python script to print hello world"
Expected:
  - File: ~/ai-projects/print-hello-world/print_hello_world.py
  - Content: print("Hello, World!")
  - Voice: "Script ready at ~/ai-projects/print-hello-world/print_hello_world.py"
```

**Test 2: Web Scraper**
```
Voice: "Write a Python script to scrape HackerNews top stories"
Expected:
  - File: ~/ai-projects/scrape-hackernews/scrape_hackernews.py
  - Code includes: requests, BeautifulSoup
  - Execution: Successfully fetches and prints stories
```

### Deliverables

- ✅ Voice capture working (wake word + STT)
- ✅ Code generation from natural language
- ✅ File save to ~/ai-projects/
- ✅ Optional execution in sandbox
- ✅ Voice feedback (TTS)
- ✅ 5+ test scripts generated successfully

### Success Criteria

- End-to-end flow completes in <30 seconds
- Code compiles/runs successfully 80%+ of the time
- Voice recognition accuracy >90%
- TTS response sounds natural enough

---

## Phase 2: AI Code Editor (Week 2)

**Goal:** Context-aware code editing with AI suggestions

### Architecture Focus

```
File Watcher → Context Builder → LLM → Suggestions → Apply Edits
```

### Tasks

#### Day 1-2: File Watching & Context Building

**Script:** `modules/code-editor/file-watcher.js`

```javascript
const chokidar = require('chokidar');
const parser = require('@babel/parser');  // For JavaScript
// Use ast-parser for Python, etc.

class FileWatcher {
    constructor(projectPath) {
        this.projectPath = projectPath;
        this.watcher = null;
        this.contextCache = new Map();
    }
    
    start() {
        this.watcher = chokidar.watch(`${this.projectPath}/**/*.{js,jsx,py,ts,tsx}`, {
            ignored: /node_modules|\.git/,
            persistent: true
        });
        
        this.watcher.on('change', async (filePath) => {
            console.log(`File changed: ${filePath}`);
            await this.updateContext(filePath);
            await this.generateSuggestions(filePath);
        });
    }
    
    async updateContext(filePath) {
        const content = await fs.readFile(filePath, 'utf8');
        
        // Parse AST
        const ast = parser.parse(content, {
            sourceType: 'module',
            plugins: ['jsx', 'typescript']
        });
        
        // Extract context
        const context = {
            functions: extractFunctions(ast),
            imports: extractImports(ast),
            exports: extractExports(ast),
            dependencies: await this.findDependencies(filePath)
        };
        
        this.contextCache.set(filePath, context);
    }
    
    async findDependencies(filePath) {
        // Find imported files
        const context = this.contextCache.get(filePath);
        const deps = [];
        
        for (const imp of context.imports) {
            const depPath = resolvePath(imp.source, filePath);
            if (depPath) {
                deps.push(depPath);
            }
        }
        
        return deps;
    }
}
```

#### Day 3-4: AI Suggestion Engine

**Script:** `modules/code-editor/suggestion-engine.js`

```javascript
class SuggestionEngine {
    async generateSuggestions(filePath, cursorPosition) {
        // Get file context
        const content = await fs.readFile(filePath, 'utf8');
        const context = contextCache.get(filePath);
        
        // Build prompt with context
        const prompt = this.buildPrompt(content, cursorPosition, context);
        
        // Call LLM (Qwen Coder)
        const suggestions = await this.callLLM(prompt);
        
        // Rank suggestions
        const ranked = this.rankSuggestions(suggestions);
        
        return ranked;
    }
    
    buildPrompt(content, cursorPosition, context) {
        const linesBefore = content.slice(0, cursorPosition).split('\n').slice(-10);
        const linesAfter = content.slice(cursorPosition).split('\n').slice(0, 5);
        
        return `
# Context
Functions in file: ${context.functions.map(f => f.name).join(', ')}
Imports: ${context.imports.map(i => i.source).join(', ')}

# Code Before Cursor
${linesBefore.join('\n')}
<CURSOR>

# Code After Cursor
${linesAfter.join('\n')}

# Task
Suggest the most likely code completion at <CURSOR>. Consider:
- Function signatures and types
- Code patterns in this file
- Imported libraries

Return only the completion code, no explanation.
        `;
    }
    
    async callLLM(prompt) {
        const response = await fetch('http://localhost:1234/v1/chat/completions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: 'qwen-coder-32b',
                messages: [{ role: 'user', content: prompt }],
                temperature: 0.3,
                max_tokens: 200
            })
        });
        
        const data = await response.json();
        return data.choices[0].message.content;
    }
    
    rankSuggestions(suggestions) {
        // Simple ranking (improve later)
        return suggestions.map(s => ({
            code: s,
            confidence: 0.8  // TODO: Calculate real confidence
        }));
    }
}
```

#### Day 5: Multi-File Editing

**Script:** `modules/code-editor/multi-file-editor.js`

```javascript
async function refactorAcrossFiles(instruction, projectPath) {
    // Example: "Rename function 'fetchData' to 'getData' across all files"
    
    // 1. Find all files
    const files = await findRelevantFiles(instruction, projectPath);
    
    // 2. Generate refactoring plan
    const plan = await generateRefactoringPlan(instruction, files);
    
    // 3. Apply changes
    const results = [];
    for (const change of plan.changes) {
        const result = await applyChange(change);
        results.push(result);
    }
    
    return results;
}

async function generateRefactoringPlan(instruction, files) {
    // Build context from all files
    const contextPrompt = files.map(f => `
File: ${f.path}
\`\`\`
${f.content}
\`\`\`
    `).join('\n\n');
    
    const prompt = `
${contextPrompt}

Task: ${instruction}

Generate a refactoring plan as JSON:
{
  "changes": [
    {
      "file": "path/to/file.js",
      "line": 10,
      "oldCode": "function fetchData()",
      "newCode": "function getData()"
    }
  ]
}
    `;
    
    const response = await callLLM(prompt);
    return JSON.parse(response);
}
```

#### Day 6-7: IDE Integration (VSCode Extension - Optional)

**Extension:** `vscode-extension/src/extension.js`

```javascript
const vscode = require('vscode');

function activate(context) {
    // Register inline completion provider
    const provider = vscode.languages.registerInlineCompletionItemProvider(
        { pattern: '**' },
        {
            async provideInlineCompletionItems(document, position, context, token) {
                // Get suggestions from our engine
                const suggestions = await fetch('http://localhost:3000/api/suggestions', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        filePath: document.uri.fsPath,
                        content: document.getText(),
                        position: document.offsetAt(position)
                    })
                }).then(r => r.json());
                
                return suggestions.map(s => ({
                    insertText: s.code,
                    range: new vscode.Range(position, position)
                }));
            }
        }
    );
    
    context.subscriptions.push(provider);
}
```

### Testing Scenarios

**Test 1: Inline Completion**
```javascript
// File: src/utils.js
function fetchUser
// Expected suggestion: (id) { return fetch(`/api/users/${id}`).then(r => r.json()); }
```

**Test 2: Refactoring**
```
Instruction: "Extract this code into a separate function"
Selected code:
  const data = await fetch('/api/data');
  const json = await data.json();
  return json;

Expected:
  async function fetchData() {
      const data = await fetch('/api/data');
      const json = await data.json();
      return json;
  }
```

**Test 3: Multi-File Rename**
```
Instruction: "Rename 'UserService' to 'UserRepository' across all files"
Expected:
  - Updated in UserService.js → UserRepository.js
  - All imports updated
  - All references updated
```

### Deliverables

- ✅ File watcher detecting changes
- ✅ Context cache (AST, dependencies)
- ✅ Inline suggestions working
- ✅ Multi-file refactoring
- ✅ (Optional) VSCode extension

### Success Criteria

- Suggestions appear within 500ms
- Accuracy >70% (user accepts suggestion)
- Multi-file refactoring correct 90%+ of the time

---

## Phase 3: App Builder (Week 3)

**Goal:** Natural language → full working application

### Architecture Focus

```
NL Input → App Planner → Code Generator → Project Setup → Dev Server
```

### Tasks

#### Day 1-2: App Planning & Architecture

**Script:** `modules/app-builder/app-planner.js`

```javascript
async function planApp(description) {
    const prompt = `
You are an expert full-stack architect. Given a description, create a detailed app plan.

Description: "${description}"

Generate a JSON plan:
{
  "name": "app-name",
  "type": "webapp",
  "stack": {
    "frontend": "react",
    "backend": "supabase",
    "styling": "tailwind"
  },
  "entities": [
    {
      "name": "User",
      "fields": ["id", "email", "password_hash", "created_at"]
    },
    {
      "name": "Recipe",
      "fields": ["id", "user_id", "title", "ingredients", "instructions", "created_at"]
    }
  ],
  "features": [
    "User authentication",
    "Create/edit/delete recipes",
    "Search recipes",
    "View recipe details"
  ],
  "components": [
    {
      "name": "RecipeList",
      "type": "page",
      "props": []
    },
    {
      "name": "RecipeDetail",
      "type": "page",
      "props": ["recipeId"]
    },
    {
      "name": "AddRecipeForm",
      "type": "component",
      "props": ["onSubmit"]
    }
  ],
  "routes": [
    { "path": "/", "component": "Home" },
    { "path": "/recipes", "component": "RecipeList" },
    { "path": "/recipes/:id", "component": "RecipeDetail" }
  ]
}
    `;
    
    const response = await callLLM(prompt, 'ollama/llama3.1:70b');  // Use Llama for planning
    return JSON.parse(response);
}
```

#### Day 3-4: Code Generation Pipeline

**Script:** `modules/app-builder/code-generator.js`

```javascript
class AppCodeGenerator {
    async generateApp(plan) {
        const projectPath = path.join(process.env.HOME, 'ai-projects', plan.name);
        
        // 1. Initialize project
        await this.initProject(projectPath, plan);
        
        // 2. Generate database schema
        await this.generateDatabase(projectPath, plan);
        
        // 3. Generate components
        for (const component of plan.components) {
            await this.generateComponent(projectPath, component, plan);
        }
        
        // 4. Generate routes
        await this.generateRoutes(projectPath, plan);
        
        // 5. Setup auth (if needed)
        if (plan.features.includes('User authentication')) {
            await this.setupAuth(projectPath, plan);
        }
        
        return projectPath;
    }
    
    async initProject(projectPath, plan) {
        // Create directory
        await fs.mkdir(projectPath, { recursive: true });
        
        // Initialize Vite + React
        await exec(`cd ${projectPath} && npm create vite@latest . -- --template react`);
        
        // Install dependencies
        const deps = ['react-router-dom', 'tailwindcss', '@supabase/supabase-js'];
        await exec(`cd ${projectPath} && npm install ${deps.join(' ')}`);
        
        // Setup Tailwind
        await exec(`cd ${projectPath} && npx tailwindcss init`);
    }
    
    async generateComponent(projectPath, component, plan) {
        const code = await this.generateComponentCode(component, plan);
        const filePath = path.join(projectPath, 'src', 'components', `${component.name}.jsx`);
        await fs.writeFile(filePath, code, 'utf8');
    }
    
    async generateComponentCode(component, plan) {
        const prompt = `
Generate a React component for: ${component.name}

Context:
- App: ${plan.name}
- Type: ${component.type}
- Props: ${component.props.join(', ')}
- Stack: React + Tailwind CSS
- Entities: ${plan.entities.map(e => e.name).join(', ')}

Requirements:
- Use Tailwind for styling
- Include error handling
- Add loading states
- Use modern React (hooks)

Return only the component code.
        `;
        
        const code = await callLLM(prompt, 'lmstudio/qwen-coder-32b');
        return code;
    }
    
    async generateDatabase(projectPath, plan) {
        // Generate Supabase migration
        const migration = plan.entities.map(entity => `
create table ${entity.name.toLowerCase()}s (
  ${entity.fields.map(f => `${f} ${getFieldType(f)}`).join(',\n  ')}
);
        `).join('\n\n');
        
        const migrationPath = path.join(projectPath, 'supabase', 'migrations', '001_initial.sql');
        await fs.mkdir(path.dirname(migrationPath), { recursive: true });
        await fs.writeFile(migrationPath, migration, 'utf8');
    }
}
```

#### Day 5: Template System

**Templates:** `modules/app-builder/templates/`

Create reusable templates for common patterns:

```javascript
// templates/react-crud-page.js
module.exports = {
    generate(entityName, fields) {
        return `
import { useState, useEffect } from 'react';
import { supabase } from '../lib/supabase';

export default function ${entityName}List() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        fetchItems();
    }, []);
    
    async function fetchItems() {
        const { data, error } = await supabase
            .from('${entityName.toLowerCase()}s')
            .select('*');
        
        if (error) {
            console.error('Error:', error);
            return;
        }
        
        setItems(data);
        setLoading(false);
    }
    
    if (loading) return <div>Loading...</div>;
    
    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">${entityName}s</h1>
            <div className="grid gap-4">
                {items.map(item => (
                    <div key={item.id} className="border p-4 rounded">
                        {/* Render fields */}
                    </div>
                ))}
            </div>
        </div>
    );
}
        `;
    }
};
```

#### Day 6-7: Integration & Testing

**End-to-end test:**

```javascript
async function testAppBuilder() {
    const description = "Build a recipe app with user accounts";
    
    // 1. Plan
    const plan = await planApp(description);
    console.log('Plan:', JSON.stringify(plan, null, 2));
    
    // 2. Generate
    const projectPath = await generateApp(plan);
    console.log('Generated at:', projectPath);
    
    // 3. Start dev server
    const server = await startDevServer(projectPath);
    console.log('Running at:', server.url);
    
    // 4. Test in browser
    await testInBrowser(server.url);
}
```

### Testing Scenarios

**Test 1: Todo App**
```
Input: "Build a todo app with user accounts"
Expected:
  - Project: ~/ai-projects/todo-app/
  - Components: TodoList, AddTodoForm, Login
  - Database: users, todos tables
  - Features: CRUD todos, user auth
  - Running at: http://localhost:5173
```

**Test 2: Recipe App**
```
Input: "Build a recipe app with ingredients and instructions"
Expected:
  - Entities: User, Recipe
  - CRUD operations
  - Search functionality
  - Responsive design (Tailwind)
```

**Test 3: Blog Platform**
```
Input: "Create a simple blog with posts and comments"
Expected:
  - Entities: User, Post, Comment
  - Rich text editor
  - Comment threading
  - Author pages
```

### Deliverables

- ✅ App planner (NL → JSON architecture)
- ✅ Code generator (components, routes, DB)
- ✅ Template system (reusable patterns)
- ✅ Project scaffolding automation
- ✅ Dev server auto-start
- ✅ 3+ test apps generated successfully

### Success Criteria

- Apps compile without errors 90%+ of the time
- Generated code is clean and follows best practices
- Apps are functional out-of-the-box (80%+ features work)
- Total generation time <60 seconds

---

## Phase 4: Computer Use Automation (Week 4)

**Goal:** Automate browser/desktop tasks with vision-guided execution

### Architecture Focus

```
Task → Planner → [Screenshot → LLaVA → Action → Verify] Loop → Result
```

### Tasks

#### Day 1-2: Vision-Guided Browser Control

**Script:** `modules/computer-use/browser-controller.js`

```javascript
const playwright = require('playwright');

class VisionGuidedBrowser {
    constructor() {
        this.browser = null;
        this.page = null;
    }
    
    async init() {
        this.browser = await playwright.chromium.launch({ headless: false });
        this.page = await this.browser.newPage();
    }
    
    async analyzeScreen() {
        // Take screenshot
        const screenshot = await this.page.screenshot({ encoding: 'base64' });
        
        // Analyze with LLaVA
        const analysis = await this.askVision(
            screenshot,
            "Describe what you see. List all interactive elements (buttons, links, forms) and their locations."
        );
        
        return analysis;
    }
    
    async askVision(screenshot, question) {
        // Call Ollama LLaVA
        const response = await fetch('http://localhost:11434/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: 'llava:7b',
                prompt: question,
                images: [screenshot],
                stream: false
            })
        });
        
        const data = await response.json();
        return data.response;
    }
    
    async performAction(action) {
        switch (action.type) {
            case 'click':
                await this.page.click(action.selector);
                break;
            case 'type':
                await this.page.fill(action.selector, action.text);
                break;
            case 'navigate':
                await this.page.goto(action.url);
                break;
            case 'scroll':
                await this.page.mouse.wheel(0, action.amount);
                break;
        }
        
        // Wait for page to settle
        await this.page.waitForLoadState('networkidle');
    }
}
```

#### Day 3-4: Multi-Step Task Execution

**Script:** `modules/computer-use/task-executor.js`

```javascript
async function executeTask(taskDescription) {
    const browser = new VisionGuidedBrowser();
    await browser.init();
    
    // Generate plan
    const plan = await generateTaskPlan(taskDescription);
    console.log('Task plan:', plan);
    
    // Execute steps
    const results = [];
    for (const step of plan.steps) {
        try {
            // Analyze current state
            const screenAnalysis = await browser.analyzeScreen();
            
            // Decide action
            const action = await decideAction(step, screenAnalysis);
            
            // Execute
            await browser.performAction(action);
            
            // Verify
            const verification = await verifyStepCompleted(step, browser);
            
            results.push({
                step,
                action,
                success: verification.success,
                screenshot: await browser.page.screenshot({ encoding: 'base64' })
            });
            
            if (!verification.success) {
                // Retry logic
                console.log('Step failed, retrying...');
                await retryStep(step, browser);
            }
            
        } catch (error) {
            console.error(`Step failed: ${step.description}`, error);
            results.push({ step, success: false, error: error.message });
        }
    }
    
    await browser.close();
    return results;
}

async function generateTaskPlan(taskDescription) {
    const prompt = `
Break down this task into steps:
"${taskDescription}"

Return JSON:
{
  "steps": [
    { "action": "navigate", "target": "URL", "description": "..." },
    { "action": "click", "target": "selector", "description": "..." },
    { "action": "type", "target": "selector", "text": "...", "description": "..." }
  ]
}
    `;
    
    const response = await callLLM(prompt, 'ollama/qwen2.5:32b');
    return JSON.parse(response);
}

async function decideAction(step, screenAnalysis) {
    // Use LLM to convert step + screen state → precise action
    const prompt = `
Current screen: ${screenAnalysis}

Goal: ${step.description}

What action should I take? Return JSON:
{
  "type": "click" | "type" | "navigate" | "scroll",
  "selector": "CSS selector",
  "text": "text to type (if applicable)"
}
    `;
    
    const response = await callLLM(prompt);
    return JSON.parse(response);
}
```

#### Day 5: Error Recovery & Retries

**Script:** `modules/computer-use/error-recovery.js`

```javascript
async function retryStep(step, browser, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        console.log(`Retry attempt ${i + 1}/${maxRetries}`);
        
        // Re-analyze screen
        const analysis = await browser.analyzeScreen();
        
        // Ask LLM for alternative approach
        const alternative = await getAlternativeAction(step, analysis, i);
        
        // Try alternative
        try {
            await browser.performAction(alternative);
            const verification = await verifyStepCompleted(step, browser);
            
            if (verification.success) {
                console.log('Retry successful');
                return true;
            }
        } catch (error) {
            console.error(`Retry ${i + 1} failed:`, error);
        }
    }
    
    return false;  // All retries failed
}

async function getAlternativeAction(step, screenAnalysis, attemptNumber) {
    const prompt = `
Previous attempt ${attemptNumber} failed for: ${step.description}

Current screen: ${screenAnalysis}

Suggest an alternative approach. Return JSON action.
    `;
    
    const response = await callLLM(prompt);
    return JSON.parse(response);
}
```

#### Day 6-7: Real-World Automation Tasks

**Example tasks:**

```javascript
// Task 1: Gmail invoice extraction
await executeTask("Check my Gmail for invoice emails and save PDFs to Downloads");

// Task 2: Form filling
await executeTask("Fill out the contact form on example.com with my details");

// Task 3: Data extraction
await executeTask("Go to HackerNews, scrape top 10 stories, save to CSV");

// Task 4: Social media posting
await executeTask("Post this message to Twitter: 'Hello from Einstein!'");
```

### Testing Scenarios

**Test 1: Gmail Search**
```
Task: "Check Gmail for emails with subject containing 'invoice'"
Expected:
  - Navigate to gmail.com
  - Login (if needed)
  - Use search box
  - Report count of results
```

**Test 2: Form Submission**
```
Task: "Fill contact form at example.com with name 'John' and email 'john@example.com'"
Expected:
  - Navigate to example.com
  - Find form fields
  - Fill name and email
  - Click submit
  - Verify success message
```

**Test 3: E-commerce**
```
Task: "Add product 'Laptop' to cart on amazon.com (DRY RUN)"
Expected:
  - Search for laptop
  - Click first result
  - Find 'Add to Cart' button
  - Click (with confirmation prompt)
```

### Deliverables

- ✅ Vision-guided browser control
- ✅ Multi-step task execution
- ✅ Error recovery system
- ✅ Screenshot logging
- ✅ Safety mechanisms (confirmation prompts)
- ✅ 5+ automation tasks tested

### Success Criteria

- Task completion rate >85%
- No accidental destructive actions (payment, deletion)
- Average task time <3 minutes
- Vision accuracy >80% (correct element identification)

---

## Phase 5: Integration & Polish (Week 5)

**Goal:** Unified system with all modules working together

### Tasks

#### Day 1-2: Unified Interface

**Web Dashboard:** `dashboard/src/App.jsx`

```jsx
import { useState, useEffect } from 'react';

export default function EinsteinDashboard() {
    const [activeTasks, setActiveTasks] = useState([]);
    const [systemStatus, setSystemStatus] = useState({});
    
    useEffect(() => {
        // Fetch active tasks
        fetchActiveTasks();
        
        // Fetch system status
        fetchSystemStatus();
        
        // Poll every 5 seconds
        const interval = setInterval(() => {
            fetchActiveTasks();
            fetchSystemStatus();
        }, 5000);
        
        return () => clearInterval(interval);
    }, []);
    
    return (
        <div className="min-h-screen bg-gray-900 text-white p-8">
            <h1 className="text-4xl font-bold mb-8">Einstein AI Coding System</h1>
            
            {/* System Status */}
            <div className="grid grid-cols-3 gap-4 mb-8">
                <StatusCard 
                    title="Qwen Coder" 
                    status={systemStatus.qwenCoder} 
                />
                <StatusCard 
                    title="Ollama" 
                    status={systemStatus.ollama} 
                />
                <StatusCard 
                    title="LLaVA" 
                    status={systemStatus.llava} 
                />
            </div>
            
            {/* Active Tasks */}
            <div className="bg-gray-800 rounded-lg p-6">
                <h2 className="text-2xl font-bold mb-4">Active Tasks</h2>
                {activeTasks.map(task => (
                    <TaskCard key={task.id} task={task} />
                ))}
            </div>
            
            {/* Quick Actions */}
            <div className="mt-8">
                <h2 className="text-2xl font-bold mb-4">Quick Actions</h2>
                <div className="grid grid-cols-2 gap-4">
                    <ActionButton 
                        label="Generate Code" 
                        onClick={() => openModal('code-gen')} 
                    />
                    <ActionButton 
                        label="Build App" 
                        onClick={() => openModal('app-builder')} 
                    />
                    <ActionButton 
                        label="Automate Task" 
                        onClick={() => openModal('automation')} 
                    />
                    <ActionButton 
                        label="View Projects" 
                        onClick={() => navigate('/projects')} 
                    />
                </div>
            </div>
        </div>
    );
}
```

#### Day 3: Cross-Module Workflows

**Example workflow:** Voice → App Builder → Code Editor refinement

```javascript
async function hybridWorkflow() {
    // 1. Voice command: "Build a recipe app"
    const voiceCommand = await captureVoiceCommand();
    
    // 2. App Builder creates initial app
    const plan = await planApp(voiceCommand);
    const projectPath = await generateApp(plan);
    
    // 3. Start dev server
    await startDevServer(projectPath);
    
    // 4. User reviews in browser, requests changes via voice
    const refinement = await captureVoiceCommand();
    // "Add a search feature to the recipe list"
    
    // 5. Code Editor modifies existing code
    await refineApp(projectPath, refinement);
    
    // 6. Voice feedback
    await speak("Search feature added to recipe list");
}
```

#### Day 4-5: Error Handling & Recovery

**Global error handler:**

```javascript
class GlobalErrorHandler {
    async handleError(error, context) {
        console.error('Error:', error);
        
        // Log error
        await this.logError(error, context);
        
        // Determine recovery strategy
        const recovery = await this.determineRecovery(error, context);
        
        switch (recovery.action) {
            case 'retry':
                return await this.retry(context);
            case 'fallback':
                return await this.fallback(context, recovery.fallbackModel);
            case 'user_input':
                return await this.askUser(recovery.question);
            case 'abort':
                return await this.abort(context, recovery.reason);
        }
    }
    
    async determineRecovery(error, context) {
        // Use LLM to decide recovery strategy
        const prompt = `
Error occurred: ${error.message}
Context: ${JSON.stringify(context)}

Determine the best recovery strategy. Return JSON:
{
  "action": "retry" | "fallback" | "user_input" | "abort",
  "reason": "...",
  "fallbackModel": "..." (if action=fallback),
  "question": "..." (if action=user_input)
}
        `;
        
        const response = await callLLM(prompt);
        return JSON.parse(response);
    }
}
```

#### Day 6: Performance Optimization

**Optimizations:**

1. **Model caching**
```bash
# Keep models warm
ollama run qwen2.5:32b "" --keepalive 24h
ollama run llava:7b "" --keepalive 24h
```

2. **Context caching**
```javascript
// Cache file contexts
const contextCache = new LRU({ max: 100 });

async function getFileContext(filePath) {
    const cached = contextCache.get(filePath);
    if (cached && !fileModifiedSince(filePath, cached.timestamp)) {
        return cached.context;
    }
    
    const context = await buildContext(filePath);
    contextCache.set(filePath, { context, timestamp: Date.now() });
    return context;
}
```

3. **Parallel processing**
```javascript
// Generate multiple components in parallel
const components = await Promise.all(
    plan.components.map(c => generateComponent(c, plan))
);
```

#### Day 7: Documentation & Demo

**Create comprehensive docs:**

1. **User Guide** (see USER-GUIDE.md)
2. **Tech Decisions** (see TECH-DECISIONS.md)
3. **Example Workflows** (see EXAMPLE-WORKFLOWS.md)
4. **Demo Video**
   - Voice command → app generation
   - Code editing with AI suggestions
   - Browser automation task

### Deliverables

- ✅ Unified web dashboard
- ✅ Cross-module workflows
- ✅ Global error handling
- ✅ Performance optimizations
- ✅ Complete documentation
- ✅ Demo video

### Success Criteria

- All modules integrate seamlessly
- Error recovery works in 90%+ of cases
- Performance targets met (see Phase 1-4)
- Documentation is clear and comprehensive

---

## Success Metrics Summary

### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Local processing** | >90% | Tasks handled locally vs cloud |
| **Code quality** | >80% | First-time compilation success |
| **Task accuracy** | >90% | Correct execution rate |
| **Response time** | <30s | Simple tasks |
| **Response time** | <5min | Complex apps |
| **User satisfaction** | >80% | Can replace manual coding for 50%+ tasks |

### Quality Gates

Before moving to next phase:
- ✅ All deliverables completed
- ✅ Success criteria met
- ✅ Tests passing
- ✅ Documentation updated
- ✅ No critical bugs

---

## Risk Mitigation

### Technical Risks

**Risk:** Local models produce low-quality code  
**Mitigation:**
- Use Qwen Coder 32B (high-quality model)
- Fallback to Claude for complex tasks
- User review before execution

**Risk:** Vision accuracy insufficient  
**Mitigation:**
- Use confidence thresholds
- Fallback to Claude Vision for critical tasks
- Ask user confirmation for ambiguous cases

**Risk:** Execution safety (accidental destructive actions)  
**Mitigation:**
- Sandboxing (OpenJarvis)
- Confirmation prompts for destructive actions
- Dry-run mode
- Action logging & undo

### UX Risks

**Risk:** Voice commands ambiguous  
**Mitigation:**
- Confirmation prompts ("Did you mean...?")
- Show plan before execution
- Allow refinement

**Risk:** Task complexity exceeds system capability  
**Mitigation:**
- Break down into smaller steps
- Provide step-by-step guidance
- Suggest alternatives

---

## Timeline Overview

```
Week 0: Setup (2-3 days)
    ├── Verify infrastructure
    ├── Install dependencies
    └── Create project structure

Week 1: Foundation
    ├── Voice capture
    ├── Code generation
    ├── File management
    └── TTS response

Week 2: Code Editor
    ├── File watching
    ├── Context building
    ├── AI suggestions
    └── Multi-file refactoring

Week 3: App Builder
    ├── App planning
    ├── Code generation pipeline
    ├── Template system
    └── Integration testing

Week 4: Computer Use
    ├── Vision-guided browser
    ├── Multi-step execution
    ├── Error recovery
    └── Real-world tasks

Week 5: Integration
    ├── Unified dashboard
    ├── Cross-module workflows
    ├── Error handling
    ├── Optimization
    └── Documentation
```

---

## Next Steps

1. **Review this roadmap** with stakeholders
2. **Adjust timeline** based on resources
3. **Start Phase 0** (setup)
4. **Begin weekly sprints** with clear deliverables
5. **Iterate based on feedback**

---

**Document Status:** Ready for implementation  
**Last Updated:** April 19, 2026  
**Version:** 1.0
