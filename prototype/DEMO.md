# Demo Script - Einstein AI Coding Agent Prototype

## Pre-Demo Checklist

Before starting the demo, ensure:

- [ ] LM Studio is running with Qwen Coder 32B loaded
- [ ] Microphone is working and permissions granted
- [ ] Terminal window is maximized for visibility
- [ ] `~/ai-projects/` directory is clean (or clear old test projects)
- [ ] All dependencies installed and tested
- [ ] Internet connection stable (if needed for demo context)

## Demo Flow (5-10 minutes)

### 1. Introduction (30 seconds)

**Script:**
> "Today I'm going to show you Einstein AI Coding Agent - a prototype that generates working code from voice commands in under 30 seconds. Let's see it in action."

### 2. Show the Starting Point (30 seconds)

```bash
# Show current projects directory (empty or minimal)
ls -la ~/ai-projects/

# Show prototype structure
cd ~/.openclaw/workspace/docs/ai-coding-agent/prototype
tree -L 2
```

**Script:**
> "Here's our prototype. It has four main modules: voice input, LLM integration, code execution, and storage. Let's start it up."

### 3. Start the Agent (15 seconds)

```bash
python3 main.py
```

**Script:**
> "The agent starts up and verifies all systems are ready. You can see it checks the microphone, LM Studio connection, and execution capabilities."

### 4. Demo #1: Simple Python Script (2 minutes)

**Voice Command:**
> "Write a Python script to print hello world with a timestamp"

**Steps:**
1. Press ENTER when prompted
2. Speak the command clearly
3. Show transcription
4. Wait for code generation
5. Show generated code preview
6. Show saved project

```bash
# After generation completes:
cd ~/ai-projects/print-hello-world-with-timestamp/
cat print_hello_world_with_timestamp.py
cat README.md

# Run it
python3 print_hello_world_with_timestamp.py
```

**Script:**
> "In about 15-20 seconds, we have a working Python script with proper structure, imports, and error handling. The agent automatically created a project directory, saved the code, generated a README, and initialized a git repository. Let's run it..."

### 5. Demo #2: Web Scraper (2 minutes)

**Voice Command:**
> "Write a Python script to scrape HackerNews top stories and save them to a JSON file"

**Steps:**
1. Press ENTER
2. Speak command
3. Show more complex code generation
4. Highlight code quality (imports, error handling, comments)

```bash
cd ~/ai-projects/scrape-hackernews-top-stories/
cat scrape_hackernews_top_stories.py | head -50

# Show it has proper structure
grep -E "^import|^def|^class" scrape_hackernews_top_stories.py
```

**Script:**
> "This is more complex - it includes HTTP requests, HTML parsing, JSON file operations, and comprehensive error handling. All generated in under 30 seconds from a simple voice command."

### 6. Demo #3: JavaScript Function (1.5 minutes)

**Voice Command:**
> "Write a JavaScript function to validate email addresses with test cases"

**Steps:**
1. Generate code
2. Show JavaScript-specific handling

```bash
cd ~/ai-projects/validate-email-addresses/
cat validate_email_addresses.js

# Run it
node validate_email_addresses.js
```

**Script:**
> "The system isn't limited to Python - it works with multiple languages. Here's JavaScript with regex validation and test cases."

### 7. Show Project Organization (1 minute)

```bash
# List all generated projects
ls -la ~/ai-projects/

# Show a complete project structure
cd ~/ai-projects/scrape-hackernews-top-stories/
tree
```

**Script:**
> "Every project is self-contained with code, documentation, metadata, and version control. You could immediately push these to GitHub or deploy them."

### 8. Performance Metrics (30 seconds)

**Script:**
> "Let's look at the numbers. Each request completes in under 30 seconds:
> - Voice capture: ~5 seconds
> - Transcription: 2-3 seconds
> - Code generation: 8-15 seconds
> - Total: 15-25 seconds average
>
> We've achieved our goal of voice-to-code in under 30 seconds."

### 9. Future Vision (1 minute)

**Script:**
> "This is just a prototype. The full implementation will add:
> - Chat interface for iterative refinement
> - Multi-file project support
> - Code editor integration
> - App builder capabilities
> - Browser automation
>
> Imagine saying: 'Build me a todo app with React and save it to GitHub' - and it just works."

### 10. Wrap Up (30 seconds)

```bash
# Show final statistics
# (Exit the agent with Ctrl+C if still running - shows stats)
```

**Script:**
> "That's Einstein AI Coding Agent. From voice to working code in seconds. Questions?"

## Backup Demos (If Time Permits)

### Bash Script Demo
**Command:** "Write a bash script to backup all Python files in the current directory to a zip file"

### Error Handling Demo
**Command:** [Speak unclearly or very quietly]
**Shows:** Graceful error handling and recovery

### Code Validation Demo
```bash
# Show validation in action
python3 executor/runner.py
```

## Common Questions & Answers

**Q: What if the LLM generates bad code?**
A: The validator catches syntax errors, and you can always edit the code manually. In the full implementation, we'll add iterative refinement.

**Q: Can it handle multi-file projects?**
A: Not in this prototype - that's Phase 2. Currently it's single-file scripts optimized for <30 second turnaround.

**Q: What about security/sandboxing?**
A: Code executes in a subprocess with timeout. For production, we'd add Docker isolation and code review workflows.

**Q: How accurate is the voice recognition?**
A: Whisper STT is industry-leading. In testing, we see >85% accuracy in normal environments. It struggles with heavy background noise.

**Q: Can it handle follow-up requests?**
A: Not yet - each request is independent. Chat-based iteration is Phase 1 of the full roadmap.

**Q: What languages are supported?**
A: Currently: Python, JavaScript, TypeScript, Bash. Easily extensible to any language with a validator.

**Q: Cost?**
A: This prototype is 100% local (Whisper + LM Studio), so zero API costs. Full implementation may use cloud LLMs for advanced features.

## Troubleshooting During Demo

### If voice recognition fails:
- "Let me try that again - sometimes background noise can interfere"
- Speak more clearly and closer to microphone
- Have a backup command typed in case needed

### If LM Studio is slow:
- "The LLM is working hard on this one - complex code takes a bit longer"
- Explain that local inference is slower but has zero API cost

### If code validation fails:
- "The validator caught a syntax issue - good example of the safety checks"
- "The code is still saved and we can fix it manually"

### If demo machine acts up:
- Have screenshots/screen recording as backup
- Can walk through code and architecture instead

## Post-Demo Discussion Points

1. **Success Metrics**
   - End-to-end time: <30s ✅
   - Code quality: Compiles and runs ✅
   - User experience: Simple and clear ✅

2. **Lessons Learned**
   - Local LLM is viable for code generation
   - Voice input works well for simple commands
   - Project automation saves significant time

3. **Next Steps**
   - Gather feedback from this demo
   - Iterate on prototype based on input
   - Plan Phase 1 implementation (5 weeks)

4. **Investment Needed**
   - Developer time: 5-8 weeks for full MVP
   - Infrastructure: Cloud GPU for faster inference (optional)
   - Design: UI/UX for chat and editor integration

---

## Recording Checklist

If recording the demo:

- [ ] Screen resolution set to 1920x1080 (good for video)
- [ ] Terminal font size increased (readable on video)
- [ ] Hide unnecessary desktop clutter
- [ ] Close unrelated applications
- [ ] Test microphone levels
- [ ] Record in quiet environment
- [ ] Have backup plan if something fails
- [ ] Include cursor highlighting (for video)

**Recording Tools:**
- macOS: QuickTime Player, ScreenFlow
- Linux: OBS Studio, SimpleScreenRecorder
- Windows: OBS Studio, Xbox Game Bar

---

**Ready to demo?**

```bash
# Final check
python3 tests/test_basic.py

# Start the show
python3 main.py
```

Break a leg! 🚀
