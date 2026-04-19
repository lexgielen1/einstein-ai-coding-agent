# User Guide - Einstein AI Coding Agent System

**Version:** 1.0  
**Date:** April 19, 2026  
**For:** End Users & Developers

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Voice Interface](#voice-interface)
3. [Chat Interface](#chat-interface)
4. [Code Editor Mode](#code-editor-mode)
5. [App Builder](#app-builder)
6. [Browser Automation](#browser-automation)
7. [Dashboard](#dashboard)
8. [Tips & Best Practices](#tips--best-practices)
9. [Troubleshooting](#troubleshooting)
10. [FAQ](#faq)

---

## Getting Started

### Prerequisites

✅ **Mac Studio M3 Ultra** (or compatible Mac with sufficient RAM)  
✅ **OpenClaw installed** and running  
✅ **Ollama** with models: qwen2.5:32b, llama3.1:70b, llava:7b  
✅ **LM Studio** with qwen-coder-32b model  
✅ **OpenJarvis** (code execution sandbox)

### Quick Start (30 seconds)

```bash
# 1. Verify all services are running
cd ~/.openclaw/workspace/ai-coding-system
node scripts/health-check.js

# Expected output:
# ✓ OpenClaw: OK
# ✓ Ollama: OK (3 models loaded)
# ✓ LM Studio: OK (qwen-coder-32b ready)
# ✓ OpenJarvis: OK
# ✓ Voice Interface: OK (Jarvis running)

# 2. Start the dashboard (optional)
npm run dashboard

# 3. Test voice interface
# Say: "Hey Einstein, are you there?"
# Expected response: "Yes, I'm here! How can I help?"
```

### First Time Setup

If this is your first time using the system:

```bash
# Initialize workspace
cd ~/.openclaw/workspace
mkdir -p ai-projects  # Your generated projects go here

# Configure preferences (optional)
node scripts/configure.js

# This will ask:
# - Default framework (React/Vue/Svelte) → React
# - Default styling (Tailwind/CSS/Styled-components) → Tailwind
# - Default backend (Supabase/Express/None) → Supabase
# - Voice preferences (local Whisper vs API) → Local
# - TTS preferences (pyttsx3 vs ElevenLabs) → pyttsx3

# Start voice interface (if not auto-started)
cd ~/jarvis-prototype
python voice_interface.py
```

---

## Voice Interface

### Wake Word

**Default wake word:** "Hey Einstein"

### How to Use

1. **Say the wake word:**  
   "Hey Einstein"

2. **Wait for the chime** (audio feedback)

3. **Speak your command clearly:**  
   Examples:
   - "Write a Python script to scrape HackerNews"
   - "Build a recipe app with user authentication"
   - "Check my Gmail for invoice emails"

4. **Wait for confirmation:**  
   Einstein will repeat your command and confirm understanding

5. **Listen to the response:**  
   Einstein will report results via text-to-speech

### Voice Commands Reference

#### Code Generation

```
"Write a [language] script to [task]"
Examples:
  - "Write a Python script to fetch weather data"
  - "Write a JavaScript function to validate email addresses"
  - "Create a bash script to backup my Documents folder"
```

#### App Building

```
"Build a [type] app with [features]"
Examples:
  - "Build a todo app with local storage"
  - "Build a blog with user authentication and comments"
  - "Create a recipe sharing app with search"
```

#### Code Editing

```
"Refactor [file/component] to [changes]"
Examples:
  - "Refactor UserProfile.jsx to use hooks instead of classes"
  - "Add error handling to the API calls in app.js"
  - "Extract the form validation into a separate utility file"
```

#### Browser Automation

```
"Go to [website] and [task]"
Examples:
  - "Check my Gmail for emails from John"
  - "Fill out the contact form at example.com with my details"
  - "Search Amazon for wireless keyboards and save the results"
```

#### Project Management

```
"[Action] project [name]"
Examples:
  - "Show me the status of my current project"
  - "Open the recipe app in the browser"
  - "Deploy my blog to production"
```

### Voice Tips

✅ **Do:**
- Speak clearly and at normal pace
- Use specific commands ("Build a todo app" not "Make something")
- Wait for the chime before speaking
- Say "repeat that" if you didn't hear the response

❌ **Don't:**
- Speak too fast or mumble
- Use very long commands (>20 words) - break into steps
- Interrupt while Einstein is responding
- Use ambiguous terms ("fix this" - fix what?)

### Voice Settings

```bash
# Change wake word
node scripts/configure-voice.js --wake-word "Computer"

# Adjust microphone sensitivity
node scripts/configure-voice.js --sensitivity 0.7  # 0.0-1.0

# Change TTS voice (pyttsx3)
node scripts/configure-voice.js --voice female  # male/female

# Enable/disable voice confirmation
node scripts/configure-voice.js --confirm-commands true
```

---

## Chat Interface

### Access

**OpenJarvis Web UI:** http://localhost:8085

**OR Telegram:** Message @EinsteinBot (if configured)

### How to Use

1. **Open the chat interface**
2. **Type your command** (same format as voice, but text)
3. **Press Enter**
4. **View real-time progress** (streaming responses)
5. **Review results** (code, screenshots, errors)

### Chat Commands

#### Interactive Commands

```
# Generate code interactively
User: "Write a Python script to process CSV files"
Einstein: "What should the script do with the CSV? Extract specific columns, 
           transform data, or generate a report?"
User: "Extract columns 'name' and 'email' and save to a new file"
Einstein: [generates script]
```

#### File Operations

```
# Read file
"Show me the contents of ~/ai-projects/todo-app/src/App.jsx"

# Edit file
"In App.jsx, change the primary color from blue to green"

# Create file
"Create a new component called SearchBar.jsx with an input field and search button"
```

#### System Commands

```
# Status
"What are you working on?"
"Show me active tasks"

# History
"What projects have I created today?"
"Show me the last 5 commands"

# Help
"How do I deploy an app?"
"What can you help me with?"
```

### Advanced Chat Features

#### Code Blocks

When Einstein responds with code, you'll see syntax-highlighted blocks:

```jsx
// Example response
export default function SearchBar({ onSearch }) {
    const [query, setQuery] = useState('');
    
    return (
        <div className="flex gap-2">
            <input 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="border px-4 py-2 rounded"
            />
            <button onClick={() => onSearch(query)}
                    className="bg-blue-500 text-white px-4 py-2 rounded">
                Search
            </button>
        </div>
    );
}
```

#### Inline Actions

Click buttons in responses:

- **[Copy Code]** - Copy to clipboard
- **[Save File]** - Save to project
- **[Run]** - Execute in sandbox
- **[Open in Editor]** - Open in VSCode (if installed)

#### Multi-Step Conversations

Einstein remembers context within a conversation:

```
User: "Build a calculator app"
Einstein: [creates calculator app]

User: "Add a history feature"
Einstein: [adds history to the SAME calculator app]

User: "Make the buttons bigger"
Einstein: [modifies the SAME app's styles]
```

---

## Code Editor Mode

### Overview

Real-time AI suggestions while you code, similar to GitHub Copilot or Cursor.

### Setup

#### Option 1: VSCode Extension (Recommended)

```bash
# Install extension
code --install-extension einstein-ai-coder.vsix

# Configure
# Open VSCode Settings (Cmd+,)
# Search: "Einstein"
# Set: Einstein Server URL → http://localhost:3000
```

#### Option 2: File Watcher (No IDE Plugin Needed)

```bash
# Start file watcher for a project
cd ~/ai-projects/recipe-app
node ~/.openclaw/workspace/ai-coding-system/scripts/start-watcher.js

# This watches for file changes and provides suggestions
```

### Features

#### 1. Inline Completions

**Triggers:**
- Pause typing for 500ms
- Press `Tab` (VSCode extension)
- Save file (file watcher mode)

**Example:**

```javascript
// You type:
function fetchUser

// Einstein suggests (press Tab to accept):
function fetchUserById(id) {
    return fetch(`/api/users/${id}`)
        .then(response => response.json())
        .catch(error => console.error('Error:', error));
}
```

#### 2. Code Explanations

**Usage:** Select code → Right-click → "Explain with Einstein"

**Example:**

```javascript
// Selected code:
const memoized = useMemo(() => expensiveCalculation(data), [data]);

// Einstein explains:
"This uses React's useMemo hook to cache the result of expensiveCalculation.
 It only recalculates when 'data' changes, improving performance by avoiding
 unnecessary re-computations on every render."
```

#### 3. Refactoring Suggestions

**Usage:** Select code → Right-click → "Refactor"

**Options:**
- Extract to function
- Extract to component (React)
- Rename variable
- Convert to arrow function
- Add error handling
- Add TypeScript types

#### 4. Bug Detection

Real-time error detection beyond syntax:

```javascript
// Code:
const user = await getUser();
console.log(user.name);  // ⚠️ Warning: user might be null

// Einstein suggests:
const user = await getUser();
if (!user) {
    console.error('User not found');
    return;
}
console.log(user.name);  // ✓ Safe now
```

### Code Editor Settings

```javascript
// .einstein.config.js (in project root)
module.exports = {
    // Suggestion behavior
    suggestions: {
        enabled: true,
        delay: 500,  // ms after typing stops
        minChars: 3,  // minimum chars before suggesting
        maxSuggestions: 3
    },
    
    // Context
    context: {
        includeImports: true,
        includeNearbyFunctions: true,
        includeTypes: true,
        maxContextSize: 8000  // tokens
    },
    
    // Refactoring
    refactoring: {
        autoSuggest: true,  // Proactive suggestions
        confidenceThreshold: 0.7  // Only show high-confidence
    },
    
    // Style
    style: {
        framework: 'react',  // react, vue, svelte
        styling: 'tailwind',  // tailwind, css, styled-components
        indentation: 2,  // spaces
        quotes: 'single'  // single, double
    }
};
```

---

## App Builder

### Quick Start

```
# Voice
"Hey Einstein, build a [description] app"

# Chat
"Create a task management app with user authentication"
```

### Detailed Specification

For more control, provide a structured description:

```
"Build an app with these requirements:

Name: Recipe Sharing App

Entities:
- User (email, name, avatar)
- Recipe (title, ingredients, instructions, cook time, image)
- Comment (user, recipe, text, timestamp)

Features:
- User signup/login
- Create, edit, delete recipes
- Search recipes by title or ingredient
- Comment on recipes
- Favorite recipes
- User profiles

Stack:
- Frontend: React + Vite
- Backend: Supabase
- Styling: Tailwind CSS
- Deployment: Vercel"
```

### Generated Output

Every generated app includes:

```
~/ai-projects/[app-name]/
├── src/                    # Source code
├── public/                 # Static assets
├── supabase/              # Database migrations (if using Supabase)
├── .env.template          # Environment variables template
├── README.md              # Setup instructions
├── package.json           # Dependencies
└── .git/                  # Git repository (initialized)
```

### Post-Generation Steps

1. **Review README.md** - Setup instructions
2. **Configure environment** - Copy `.env.template` to `.env`
3. **Install dependencies** - `npm install`
4. **Run dev server** - `npm run dev`
5. **Review generated code**
6. **Make refinements** - Use chat/voice to request changes

### Customization Options

```
# Choose stack
"Build a [app] using Vue instead of React"
"Build a [app] with Express backend instead of Supabase"
"Build a [app] with styled-components instead of Tailwind"

# Add features
"Add a dark mode toggle"
"Add pagination to the recipe list"
"Add image upload for recipe photos"

# Modify existing
"Change the primary color to purple"
"Make the buttons rounded instead of square"
"Add a loading spinner while recipes are loading"
```

### App Templates

Pre-built templates for common patterns:

```
# CRUD app
"Build a [entity] manager"
Example: "Build a contact manager"
→ List, create, edit, delete contacts

# Blog/Content
"Build a blog"
→ Posts, comments, authors, tags

# Dashboard
"Build an admin dashboard"
→ Charts, tables, filters, exports

# E-commerce
"Build a shop"
→ Products, cart, checkout (note: payment integration manual)

# Social
"Build a [type] social app"
Example: "Build a photo sharing app"
→ Posts, likes, comments, profiles
```

---

## Browser Automation

### Safety First

⚠️ **Important:** Browser automation has access to your accounts. Always:
- Review plans before executing
- Use dry-run mode for unfamiliar tasks
- Never automate financial transactions without confirmation
- Check screenshots in logs afterward

### How to Use

#### Voice
```
"Go to [website] and [task]"
```

#### Chat
```
"Automate: [detailed task description]"
```

### Common Tasks

#### Email Management

```
# Read emails
"Check my Gmail for emails from John Smith"
"Find unread emails in my Inbox from the last week"

# Download attachments
"Download all PDF attachments from emails labeled 'Invoices'"

# Send emails (requires confirmation)
"Reply to the last email from Jane saying 'Thanks, received!'"
```

#### Form Filling

```
"Fill out the contact form at example.com with:
 Name: John Doe
 Email: john@example.com
 Message: Interested in your services"

# Einstein will:
# 1. Navigate to example.com
# 2. Find the form
# 3. Fill in the fields
# 4. Ask: "Submit form?" → User confirms: "Yes"
# 5. Click submit
# 6. Verify success
```

#### Data Extraction

```
"Search Google for 'best coffee shops Seattle' and save the top 10 results to a CSV"

"Go to HackerNews, get the top 20 stories, and save them to a file"

"Check the price of [product] on Amazon and notify me if it's under $50"
```

#### Testing

```
"Test the signup flow on localhost:5173"

# Einstein will:
# 1. Open the local app
# 2. Fill out signup form
# 3. Submit
# 4. Verify account created
# 5. Take screenshots at each step
# 6. Report results
```

### Dry-Run Mode

**Test automation without executing:**

```
"Dry run: Book a flight on airline.com from NYC to LAX"

# Einstein will:
# 1. Show you the step-by-step plan
# 2. Take screenshots at each step
# 3. NOT actually submit forms or make purchases
# 4. Give you a preview of what WOULD happen
```

### Confirmation Prompts

Certain actions always require confirmation:

- ✋ Form submissions (payment, account changes)
- ✋ Email sending
- ✋ Deletions
- ✋ Purchases
- ✋ Account settings changes

**Example:**

```
User: "Send an email to boss@company.com saying 'I quit'"
Einstein: "⚠️ This will send an email. Are you sure?
           Preview:
           To: boss@company.com
           Subject: (no subject)
           Body: I quit
           
           Send? (yes/no)"
User: "No, cancel that"
Einstein: "Cancelled. No email sent."
```

### Screenshot Logs

Every browser automation task creates a log:

```
~/automation-logs/task-recordings/[task-id]/
├── step-001-navigate.png
├── step-002-fill-form.png
├── step-003-submit.png
├── step-004-success.png
└── summary.json  # Action log with timestamps
```

**View logs:**

```bash
# List recent tasks
ls -lt ~/automation-logs/task-recordings/ | head

# View specific task
open ~/automation-logs/task-recordings/gmail-invoices-2026-04-19/
```

---

## Dashboard

### Access

**URL:** http://localhost:3000

### Overview Screen

```
┌─────────────────────────────────────────────┐
│    Einstein AI Coding System                │
├─────────────────────────────────────────────┤
│                                             │
│  🎯 Active Tasks                            │
│  ├─ App Builder: recipe-app (85%)          │
│  └─ Code Editor: main.jsx (analyzing...)   │
│                                             │
│  📊 Today's Activity                        │
│  ├─ 12 tasks completed                     │
│  ├─ 3 apps generated                       │
│  ├─ 8 code edits                           │
│  └─ 1 automation task                      │
│                                             │
│  🖥️ Model Status                            │
│  ├─ 🟢 Qwen Coder 32B (LM Studio)          │
│  ├─ 🟢 Qwen 2.5 32B (Ollama)               │
│  ├─ 🟢 LLaVA 7B (Ollama)                   │
│  └─ 🔵 Claude Sonnet (Cloud - idle)        │
│                                             │
│  📈 Performance                             │
│  ├─ Avg response time: 8.2s                │
│  ├─ Local processing: 95%                  │
│  └─ Success rate: 92%                      │
│                                             │
│  💰 Cost (This Month)                       │
│  └─ $4.50 (Cloud API usage)                │
│                                             │
│  📁 Recent Projects                         │
│  ├─ recipe-app (React + Supabase)          │
│  ├─ todo-app (React + localStorage)        │
│  └─ hn-scraper (Python)                    │
│                                             │
└─────────────────────────────────────────────┘
```

### Tabs

#### Projects

- **List all generated projects**
- **Quick actions:**
  - Open in browser
  - Open in VSCode
  - Run dev server
  - Deploy

#### Tasks

- **View active tasks**
- **Task history (last 7 days)**
- **Filter by type** (code gen, app build, automation)
- **Task details** (duration, model used, cost)

#### Models

- **Model status** (online/offline)
- **Performance metrics** (tokens/sec, latency)
- **Usage stats** (tokens used, cost)
- **Switch models** (change defaults)

#### Logs

- **Real-time logs** (streaming)
- **Filter by level** (info, warning, error)
- **Search logs**
- **Export logs**

#### Settings

- **Voice settings** (wake word, TTS)
- **Code preferences** (framework, styling)
- **Model routing** (local vs cloud thresholds)
- **Safety settings** (confirmations, dry-run default)

---

## Tips & Best Practices

### Voice Commands

✅ **Be specific:**
```
❌ "Make an app"
✅ "Build a todo app with categories and due dates"
```

✅ **Use clear pronunciation:**
```
❌ "Writascriptforscrapingnews"
✅ "Write a script for scraping news"  (speak slowly)
```

✅ **Break complex tasks into steps:**
```
❌ "Build a social network with posts, comments, likes, shares, 
     messaging, notifications, and user profiles"
✅ Step 1: "Build a social network with posts and comments"
   Step 2: "Add likes and shares to posts"
   Step 3: "Add user messaging"
```

### Chat Commands

✅ **Provide context:**
```
❌ "Fix this bug"
✅ "In RecipeCard.jsx, the favorite button doesn't toggle. 
    Fix the state update logic."
```

✅ **Use code examples:**
```
❌ "Add validation"
✅ "Add email validation like this example:
    const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)"
```

### Code Generation

✅ **Specify requirements:**
```
❌ "Write a function to fetch data"
✅ "Write an async function to fetch user data from /api/users/:id
    - Include error handling
    - Return null if user not found
    - Use fetch API
    - Add TypeScript types"
```

✅ **Review generated code:**
- Always review before deploying
- Test edge cases
- Check error handling
- Verify security (no hardcoded credentials)

### Browser Automation

✅ **Start with dry-run:**
```
✅ "Dry run: [task]"  (see what would happen)
   Review → Then: "[task]"  (actually execute)
```

✅ **Provide selectors if known:**
```
❌ "Click the submit button"
✅ "Click the submit button with class 'btn-primary'"
```

✅ **Check screenshot logs:**
- Verify actions completed correctly
- Debug failed automations
- Learn from successful patterns

---

## Troubleshooting

### Voice Not Responding

**Problem:** Wake word not detected

**Solutions:**
1. Check microphone permissions
2. Adjust sensitivity: `node scripts/configure-voice.js --sensitivity 0.8`
3. Reduce background noise
4. Restart voice interface: `pkill python && python ~/jarvis-prototype/voice_interface.py`

---

### Slow Code Generation

**Problem:** Responses take >30 seconds

**Solutions:**
1. Check model status: `ollama ps`  (are models loaded?)
2. Check RAM usage: `top`  (is system swapping?)
3. Warm up models: `ollama run qwen-coder-32b "test"`
4. Consider cloud fallback for complex tasks

---

### App Won't Build

**Problem:** Generated app has compile errors

**Solutions:**
1. Check dependencies: `npm install` (did it complete?)
2. Review console errors
3. Ask Einstein: "Fix the build errors in [app-name]"
4. Check README.md for manual setup steps (e.g., Supabase config)

---

### Browser Automation Fails

**Problem:** Can't find elements or clicks wrong things

**Solutions:**
1. Use dry-run to debug: "Dry run: [task]"
2. Provide specific selectors: "Click button with id 'submit-btn'"
3. Check screenshot logs: `~/automation-logs/task-recordings/[task]/`
4. Try again with Claude Vision: "Use high-accuracy vision mode"

---

### Dashboard Won't Load

**Problem:** http://localhost:3000 doesn't respond

**Solutions:**
```bash
# Check if dashboard is running
lsof -i :3000

# If not running, start it
cd ~/.openclaw/workspace/ai-coding-system/dashboard
npm run dev

# If port is in use by another app
npm run dev -- --port 3001
```

---

## FAQ

### General

**Q: How much does it cost to run?**  
A: Infrastructure is free (runs on your Mac Studio). Cloud API usage is ~$5-15/month depending on usage (90%+ tasks run locally).

**Q: Does it work offline?**  
A: Yes! 90% of features work offline. Only complex tasks that require Claude Sonnet need internet.

**Q: Is my code private?**  
A: Yes. All code generation happens locally. Only when falling back to Claude (for complex tasks) does code leave your machine (and it's sent over encrypted connection to Anthropic).

**Q: Can I use this for work/client projects?**  
A: Yes. Generated code is yours to use commercially. Always review code before deploying to production.

---

### Voice Interface

**Q: Can I change the wake word?**  
A: Yes. `node scripts/configure-voice.js --wake-word "Computer"`

**Q: Can I use a different TTS voice?**  
A: Yes. pyttsx3 has male/female options. Or upgrade to ElevenLabs for natural voices ($).

**Q: Does it work with accents?**  
A: Whisper (STT) is good with most English accents. If accuracy is low, try slowing down or using chat instead.

---

### Code Generation

**Q: What languages are supported?**  
A: Qwen Coder excels at: Python, JavaScript, TypeScript, React, Vue, HTML/CSS, Bash. Also good at: Java, Go, Rust, C++.

**Q: Can it read my existing codebase?**  
A: Yes! Use Code Editor mode or ask: "Read ~/my-project/ and suggest improvements"

**Q: Will it overwrite my files?**  
A: Only if you explicitly ask it to. Otherwise it shows changes as diffs and asks for confirmation.

---

### App Builder

**Q: What stacks are supported?**  
A: Default: React + Vite + Tailwind + Supabase. Also: Vue, Express, Next.js (with explicit request).

**Q: Can I modify generated apps?**  
A: Yes! Generated apps are fully editable. Use Code Editor mode or manual editing.

**Q: How do I deploy generated apps?**  
A: Instructions in each app's README.md. Usually: `npm run build && vercel deploy`

---

### Browser Automation

**Q: Is it safe?**  
A: Yes, with confirmation prompts for critical actions. Always use dry-run first for unfamiliar tasks.

**Q: Can it handle CAPTCHAs?**  
A: No. Automation will stop at CAPTCHAs and ask for manual completion.

**Q: Can it buy things?**  
A: Technically yes, but requires explicit confirmation. Not recommended for purchases.

---

### Performance

**Q: Why is [task] slow?**  
A: Check model status (dashboard). Slow response usually means model isn't warmed up or system is low on RAM.

**Q: How can I make it faster?**  
A: 1) Warm up models, 2) Use faster models for simple tasks, 3) Upgrade to faster hardware

**Q: What's the accuracy rate?**  
A: Code generation: 85% compile on first try. Browser automation: 80-90% success rate.

---

## Getting Help

### Support Channels

1. **Dashboard Help** - Click "?" icon for context-specific help
2. **Ask Einstein** - "How do I [task]?" (Einstein can self-document)
3. **Logs** - Check `~/.openclaw/workspace/logs/` for errors
4. **Community** - (Add Discord/forum link if available)

### Reporting Issues

When reporting an issue, include:

1. **What you tried** (voice/chat command)
2. **What happened** (error message, unexpected behavior)
3. **Logs** (from dashboard or `~/logs/`)
4. **Screenshot** (if UI issue)

### Feature Requests

Have an idea? Ask Einstein to document it:

```
"Add to feature requests: [your idea]"
```

Einstein will save it to `~/.openclaw/workspace/feature-requests.md`

---

## Keyboard Shortcuts

### Dashboard

- `Cmd+K` - Quick command palette
- `Cmd+L` - View logs
- `Cmd+P` - Projects list
- `Cmd+N` - New task
- `Cmd+/` - Help

### VSCode Extension

- `Tab` - Accept suggestion
- `Esc` - Dismiss suggestion
- `Cmd+Shift+E` - Explain selection
- `Cmd+Shift+R` - Refactor selection
- `Cmd+Shift+A` - Ask Einstein (chat)

---

## Advanced Usage

### Custom Models

Want to use a different model?

```javascript
// Edit config
cd ~/.openclaw/workspace/ai-coding-system
vim config.json

// Change models.code_generation.primary
{
  "models": {
    "code_generation": {
      "primary": "ollama/deepseek-coder:33b",  // Changed
      "fallback": "anthropic/claude-sonnet-4-5"
    }
  }
}
```

### API Access

Use Einstein programmatically:

```bash
# cURL
curl -X POST http://localhost:3000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"task": "Write a Python hello world", "language": "python"}'

# Response:
{
  "code": "print('Hello, World!')",
  "language": "python",
  "model": "lmstudio/qwen-coder-32b",
  "tokensUsed": 45,
  "duration": 1.2
}
```

### Custom Workflows

Create automation scripts:

```bash
#!/bin/bash
# daily-briefing.sh

# Generate code for all pending GitHub issues
einstein "Review GitHub issues and create branches for each"

# Check emails and create projects
einstein "Check work email for client requests and create project stubs"

# Deploy updated apps
einstein "Deploy all apps with uncommitted changes"
```

Run via cron:
```cron
0 9 * * * ~/.openclaw/workspace/scripts/daily-briefing.sh
```

---

## Changelog

### Version 1.0 (April 19, 2026)
- Initial release
- Voice interface (Jarvis integration)
- Chat interface (OpenJarvis)
- Code Editor mode
- App Builder (React + Vite + Tailwind)
- Browser Automation
- Dashboard

### Upcoming Features
- VSCode extension (currently in beta)
- Multi-language support (voice recognition)
- Team collaboration features
- Fine-tuned models (on your codebase)
- Mobile app (iOS/Android)

---

**Document Status:** Complete  
**Last Updated:** April 19, 2026  
**Version:** 1.0  
**Need Help?** Ask Einstein: "How do I [task]?"
