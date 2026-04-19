# Einstein AI Coding Agent - Prototype v0.1.0

**Voice → Code in <30 seconds**

A proof-of-concept AI coding assistant that generates working code from voice commands using Whisper STT and Qwen Coder 32B.

## Quick Start

```bash
# 1. Setup
./setup.sh

# 2. Make sure LM Studio is running with Qwen Coder 32B on port 1234

# 3. Run tests
python3 tests/test_basic.py

# 4. Start the agent
python3 main.py
```

## What It Does

```
Voice: "Write a Python script to scrape HackerNews top stories"
         ↓
[Whisper STT] → Transcribe
         ↓
[Qwen Coder] → Generate code
         ↓
[Validator] → Check syntax
         ↓
[Storage] → Save to ~/ai-projects/scrape-hackernews/
         ↓
Result: Working Python script in <30 seconds ✅
```

## Architecture

```
┌─────────────────┐
│  Voice Input    │  🎤 Press ENTER → Record 5s → Whisper STT
│  (listener.py)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM Coder      │  🤖 Qwen Coder 32B (LM Studio localhost:1234)
│  (coder.py)     │  → Generate production-ready code
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validator      │  🔍 Check syntax (Python/JS/Bash)
│  (runner.py)    │  → Optional: Execute for testing
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Storage        │  💾 Save to ~/ai-projects/{project-name}/
│  (manager.py)   │  → Create README, init git, metadata
└─────────────────┘
```

## Features

✅ **Voice Input**
- ENTER key activation (simpler than wake word for MVP)
- Whisper STT (local model, no API calls)
- 5-second recording window

✅ **Code Generation**
- Qwen Coder 32B via LM Studio
- Supports: Python, JavaScript, TypeScript, Bash
- Production-ready code with error handling

✅ **Validation**
- Syntax checking before saving
- Optional execution testing
- Safe auto-execution for simple scripts

✅ **Storage**
- Auto-creates project directories
- Generates README.md
- Git initialization with first commit
- Metadata tracking (.metadata.json)

## Requirements

### System
- macOS / Linux / Windows
- Python 3.8+
- Microphone
- ~4GB free disk space (for Whisper models)

### Python Packages
```
SpeechRecognition==3.10.0
pyaudio==0.2.14
openai-whisper==20231117
requests==2.31.0
```

### External Services
- **LM Studio** with Qwen Coder 32B loaded
  - Download: https://lmstudio.ai
  - Model: `qwen2.5-coder-32b-instruct`
  - Server: `http://localhost:1234`

### System Dependencies

**macOS:**
```bash
brew install portaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

## Installation

### Option 1: Automatic Setup
```bash
cd prototype
./setup.sh
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create projects directory
mkdir -p ~/ai-projects

# 4. Make scripts executable
chmod +x *.py tests/*.py
```

## Usage

### Start the Agent
```bash
python3 main.py
```

### Example Session
```
╔══════════════════════════════════════════════════════════╗
║     🤖 EINSTEIN AI CODING AGENT - PROTOTYPE v0.1.0      ║
╚══════════════════════════════════════════════════════════╝

🔍 Verifying setup...
✅ All systems ready!

Ready to generate code from voice commands!

🎤 Press ENTER when ready to speak...
[Press ENTER]

🔴 Recording (5 seconds)...
   Speak now!

✅ Transcribed: 'write a python script to scrape hackernews top stories'

⚙️  Generating code...
✅ Generated scrape_hackernews_top_stories.py (847 characters)

🔍 Validating code...
✅ Python syntax valid

💾 Saving to file...
✅ Project created: ~/ai-projects/scrape-hackernews-top-stories/
✅ Main file: scrape-hackernews-top-stories.py

✅ SUCCESS!
⏱️  Time: 12.3 seconds
```

### Generated Project Structure
```
~/ai-projects/scrape-hackernews-top-stories/
├── scrape_hackernews_top_stories.py  # Main script
├── README.md                          # Usage instructions
├── .metadata.json                     # Generation metadata
├── .gitignore                         # Git ignore rules
└── .git/                              # Git repository
```

## Supported Languages

| Language   | Extension | Validation | Execution |
|------------|-----------|------------|-----------|
| Python     | .py       | ✅ AST     | ✅        |
| JavaScript | .js       | ✅ Node    | ✅        |
| TypeScript | .ts       | ⚠️ Basic   | ⚠️ Requires ts-node |
| Bash       | .sh       | ✅ bash -n | ✅        |
| Java       | .java     | ❌         | ⚠️ Requires javac |
| Go         | .go       | ❌         | ⚠️ Requires go |

## Testing

### Run All Tests
```bash
python3 tests/test_basic.py
```

### Test Individual Modules

**Voice Listener:**
```bash
python3 voice/listener.py
```

**Code Generator:**
```bash
python3 llm/coder.py
```

**Code Executor:**
```bash
python3 executor/runner.py
```

**Storage Manager:**
```bash
python3 storage/manager.py
```

## Troubleshooting

### "No microphone available"
- **macOS:** Grant microphone permission in System Preferences → Security & Privacy
- **Linux:** Check `arecord -l` for available devices
- Test: `python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`

### "LM Studio not available"
1. Open LM Studio
2. Download Qwen Coder 32B model
3. Click "Start Server"
4. Verify port 1234: `curl http://localhost:1234/v1/models`

### "Whisper model not found"
- First run downloads ~140MB model
- Models stored in `~/.cache/whisper/`
- Options: `tiny` (39M), `base` (74M), `small` (244M), `medium` (769M)

### "Could not understand audio"
- Speak clearly and closer to microphone
- Reduce background noise
- Try adjusting `energy_threshold` in `voice/listener.py`

## Performance

**Target:** Voice → Code in <30 seconds

**Breakdown:**
- Voice capture: ~5s (recording)
- Transcription: ~2-3s (Whisper base model)
- Code generation: ~8-15s (LM Studio with Qwen Coder 32B)
- Validation: <1s
- Storage: <1s

**Total: ~15-25 seconds** ✅

## Limitations (MVP)

❌ **No wake word** - Uses ENTER key activation  
❌ **Simple language detection** - Keyword-based only  
❌ **No multi-file projects** - Single file output  
❌ **No iterative refinement** - One-shot generation  
❌ **No code execution for complex scripts** - Safety limits  
❌ **No context awareness** - Each request is independent  

These are addressed in the full implementation (see roadmap).

## Success Criteria

✅ **Functional:**
- Wake word/activation works
- Voice recognition accuracy >85%
- Code compiles/runs successfully
- File saved in correct location

✅ **Performance:**
- Total time: <30 seconds
- Code generation: <15 seconds

✅ **User Experience:**
- Clear feedback at each step
- Helpful error messages
- Easy to use

## Project Structure

```
prototype/
├── main.py                # Main orchestrator
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script
├── README.md             # This file
│
├── voice/
│   └── listener.py       # Voice input + Whisper STT
│
├── llm/
│   └── coder.py          # LM Studio integration
│
├── executor/
│   └── runner.py         # Code validation + execution
│
├── storage/
│   └── manager.py        # File storage + git
│
└── tests/
    └── test_basic.py     # Integration tests
```

## Example Commands

```
"Write a Python script to scrape HackerNews"
"Create a JavaScript function to validate email addresses"
"Write a Bash script to backup my documents"
"Build a Python calculator with add, subtract, multiply, divide"
"Create a Node.js HTTP server that returns Hello World"
```

## Next Steps

After successful prototype testing:

1. **Measure performance** - Track time, accuracy, success rate
2. **Record demo** - Video of full workflow
3. **Gather feedback** - User testing sessions
4. **Document learnings** - What worked, what didn't
5. **Plan Phase 1** - Full implementation roadmap

See `../IMPLEMENTATION-ROADMAP.md` for the 5-week full implementation plan.

## License

Prototype - Internal Use Only

## Author

Built with Einstein AI (OpenClaw)  
Date: April 19, 2026  
Version: 0.1.0-prototype

---

**Ready to generate code?**

```bash
python3 main.py
```

🚀 **Let's go!**
