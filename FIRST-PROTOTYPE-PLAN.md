# First Prototype Plan - Voice → Code Pipeline

**Goal:** Minimal viable demo in 1-2 days  
**Date:** April 19, 2026  
**Status:** Ready to implement

---

## Objective

Create a working proof-of-concept that demonstrates:

**Input:** Voice command → "Write a Python script to scrape HackerNews"  
**Output:** Working script saved to file in <30 seconds

This proves the core value proposition and validates the architecture before building the full system.

---

## Scope (Minimal)

### What's Included ✅

- ✅ Wake word detection ("Hey Einstein")
- ✅ Voice capture (microphone)
- ✅ Speech-to-text (Whisper local)
- ✅ Intent parsing (extract: language, task)
- ✅ Code generation (LM Studio / Qwen Coder 32B)
- ✅ File save (~/ai-projects/)
- ✅ Text-to-speech response (pyttsx3)

### What's NOT Included ❌

- ❌ Chat interface (Phase 1 later)
- ❌ Web dashboard (Phase 5)
- ❌ Code editor suggestions (Phase 2)
- ❌ App builder (Phase 3)
- ❌ Browser automation (Phase 4)
- ❌ Error recovery (basic only)
- ❌ Multi-file context (simple tasks only)

---

## Architecture (Simplified)

```
┌──────────────┐
│  Microphone  │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ Wake Word Detect │  "Hey Einstein"
│   (Porcupine)    │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Audio Capture   │  Record 5 seconds after wake word
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Whisper STT     │  Audio → Text
│   (whisper.cpp)  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Intent Parser   │  Extract: language, task
│  (Regex/Simple)  │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  LM Studio API   │  Generate code
│ Qwen Coder 32B   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  File Manager    │  Save to ~/ai-projects/
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│   TTS (pyttsx3)  │  "Script ready at ..."
└──────────────────┘
```

---

## Implementation Steps

### Day 1: Voice Input → Text

#### Step 1.1: Setup Environment

```bash
# Create prototype directory
mkdir -p ~/.openclaw/workspace/prototype-voice-to-code
cd ~/.openclaw/workspace/prototype-voice-to-code

# Install Python dependencies
pip install SpeechRecognition pyttsx3 pvporcupine openai-whisper requests

# Test microphone
python -c "import speech_recognition as sr; print('Mic test:', sr.Microphone.list_microphone_names())"
```

#### Step 1.2: Wake Word Detection

**File:** `wake_word.py`

```python
import pvporcupine
import pyaudio
import struct

# Initialize Porcupine (wake word: "jarvis" - free tier)
porcupine = pvporcupine.create(keywords=['jarvis'])

# Audio stream
pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("Listening for wake word 'Hey Jarvis'...")

try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        
        keyword_index = porcupine.process(pcm)
        
        if keyword_index >= 0:
            print("Wake word detected!")
            return True  # Signal to start voice capture
            
except KeyboardInterrupt:
    pass
finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
```

**Test:**
```bash
python wake_word.py
# Say: "Hey Jarvis"
# Expected: "Wake word detected!"
```

#### Step 1.3: Voice Capture

**File:** `voice_capture.py`

```python
import speech_recognition as sr

def capture_voice_command():
    """Capture audio after wake word"""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening... (speak now)")
        
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        # Listen for command (max 10 seconds)
        audio = recognizer.listen(source, timeout=10)
        
        print("Processing...")
        
        try:
            # Use local Whisper model
            text = recognizer.recognize_whisper(audio, model="base")
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error: {e}")
            return None

if __name__ == "__main__":
    command = capture_voice_command()
    if command:
        print(f"Command: {command}")
```

**Test:**
```bash
python voice_capture.py
# Say: "Write a Python script to print hello world"
# Expected: "You said: write a python script to print hello world"
```

---

### Day 2: Text → Code → File

#### Step 2.1: Intent Parser

**File:** `intent_parser.py`

```python
import re

def parse_intent(transcript):
    """
    Extract intent from voice transcript
    
    Returns: {
        'action': 'generate_code',
        'language': 'python',
        'task': 'print hello world'
    }
    """
    transcript = transcript.lower()
    
    # Pattern: "write a [language] script to [task]"
    pattern = r'write\s+(?:a\s+)?(\w+)\s+(?:script|function|program)\s+to\s+(.+)'
    match = re.search(pattern, transcript)
    
    if match:
        language = match.group(1)
        task = match.group(2)
        
        # Map common variations
        language_map = {
            'python': 'python',
            'javascript': 'javascript',
            'js': 'javascript',
            'bash': 'bash',
            'shell': 'bash'
        }
        
        language = language_map.get(language, language)
        
        return {
            'action': 'generate_code',
            'language': language,
            'task': task,
            'project_name': task.replace(' ', '-')[:30]  # First 30 chars
        }
    
    return {'action': 'unknown'}

# Test
if __name__ == "__main__":
    test_cases = [
        "write a python script to scrape hackernews",
        "write a javascript function to validate email addresses",
        "create a bash script to backup my documents"
    ]
    
    for test in test_cases:
        result = parse_intent(test)
        print(f"Input: {test}")
        print(f"Result: {result}\n")
```

**Test:**
```bash
python intent_parser.py
# Should parse all test cases correctly
```

#### Step 2.2: Code Generator

**File:** `code_generator.py`

```python
import requests
import json
import re

def generate_code(task, language='python'):
    """
    Generate code using LM Studio (Qwen Coder 32B)
    """
    # LM Studio API endpoint
    url = "http://localhost:1234/v1/chat/completions"
    
    # Build prompt
    system_prompt = f"You are an expert {language} developer. Generate clean, working code with comments."
    
    user_prompt = f"""Write a {language} script to {task}.

Requirements:
- Include error handling
- Add helpful comments
- Make it production-ready
- Return ONLY the code, no explanations

Code:"""
    
    # Call LM Studio
    response = requests.post(url, json={
        "model": "qwen-coder-32b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,  # Low temp for consistent code
        "max_tokens": 2000
    })
    
    if response.status_code != 200:
        raise Exception(f"LM Studio error: {response.status_code}")
    
    # Extract code
    data = response.json()
    code = data['choices'][0]['message']['content']
    
    # Remove markdown code blocks if present
    code_match = re.search(r'```(?:\w+)?\n(.*?)\n```', code, re.DOTALL)
    if code_match:
        code = code_match.group(1)
    
    return code.strip()

# Test
if __name__ == "__main__":
    code = generate_code("print hello world", "python")
    print("Generated code:")
    print(code)
```

**Test:**
```bash
# Make sure LM Studio is running on port 1234 with qwen-coder-32b

python code_generator.py
# Expected: Working Python hello world script
```

#### Step 2.3: File Manager

**File:** `file_manager.py`

```python
import os
from pathlib import Path

def save_code(code, language, project_name):
    """
    Save generated code to ~/ai-projects/
    
    Returns: file path
    """
    # Extension map
    ext_map = {
        'python': 'py',
        'javascript': 'js',
        'bash': 'sh',
        'typescript': 'ts'
    }
    
    extension = ext_map.get(language, 'txt')
    
    # Create project directory
    base_dir = Path.home() / 'ai-projects' / project_name
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine filename
    filename = f"{project_name.replace('-', '_')}.{extension}"
    filepath = base_dir / filename
    
    # Write file
    filepath.write_text(code)
    
    # Make executable if shell script
    if extension == 'sh':
        os.chmod(filepath, 0o755)
    
    # Create simple README
    readme = f"""# {project_name}

Generated by Einstein AI Coding Agent

## Usage

```bash
{'python' if extension == 'py' else 'bash'} {filename}
```

## Generated on
{os.popen('date').read().strip()}
"""
    
    (base_dir / 'README.md').write_text(readme)
    
    # Initialize git
    os.system(f"cd {base_dir} && git init && git add . && git commit -m 'Initial commit by Einstein'")
    
    return str(filepath)

# Test
if __name__ == "__main__":
    test_code = "print('Hello, World!')"
    filepath = save_code(test_code, 'python', 'test-project')
    print(f"Saved to: {filepath}")
    print(f"File exists: {os.path.exists(filepath)}")
```

**Test:**
```bash
python file_manager.py
# Should create ~/ai-projects/test-project/test_project.py
ls -la ~/ai-projects/test-project/
```

#### Step 2.4: Text-to-Speech

**File:** `tts.py`

```python
import pyttsx3

def speak(text):
    """Speak text using pyttsx3"""
    engine = pyttsx3.init()
    
    # Optional: Configure voice
    voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[0].id)  # Male
    engine.setProperty('voice', voices[1].id)  # Female (if available)
    
    # Adjust rate (speed)
    engine.setProperty('rate', 175)  # Default is ~200
    
    print(f"Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

# Test
if __name__ == "__main__":
    speak("Script ready at your projects folder")
```

**Test:**
```bash
python tts.py
# Should hear: "Script ready at your projects folder"
```

---

### Day 2 Afternoon: Integration

#### Main Orchestrator

**File:** `main.py`

```python
#!/usr/bin/env python3
"""
Einstein AI Coding Agent - Prototype
Voice → Code pipeline
"""

import sys
from wake_word import listen_for_wake_word
from voice_capture import capture_voice_command
from intent_parser import parse_intent
from code_generator import generate_code
from file_manager import save_code
from tts import speak

def main():
    print("Einstein AI Coding Agent - Prototype")
    print("=" * 50)
    print("Say 'Hey Jarvis' to start")
    print("=" * 50)
    
    while True:
        try:
            # 1. Wait for wake word
            print("\n[Listening for wake word...]")
            if not listen_for_wake_word():
                continue
            
            # Chime sound (optional)
            print("🔔 Wake word detected!")
            
            # 2. Capture voice command
            transcript = capture_voice_command()
            if not transcript:
                speak("I didn't catch that. Please try again.")
                continue
            
            print(f"\n📝 You said: {transcript}")
            
            # 3. Parse intent
            intent = parse_intent(transcript)
            
            if intent['action'] == 'unknown':
                speak("I'm not sure what you want me to do. Try saying 'write a python script to...'")
                continue
            
            print(f"\n🎯 Intent: {intent['action']}")
            print(f"   Language: {intent['language']}")
            print(f"   Task: {intent['task']}")
            
            # Confirm
            speak(f"Generating {intent['language']} script for {intent['task']}")
            
            # 4. Generate code
            print("\n⚙️  Generating code...")
            code = generate_code(intent['task'], intent['language'])
            
            print("\n📄 Generated code:")
            print("-" * 50)
            print(code)
            print("-" * 50)
            
            # 5. Save to file
            print("\n💾 Saving to file...")
            filepath = save_code(code, intent['language'], intent['project_name'])
            
            print(f"✅ Saved to: {filepath}")
            
            # 6. Respond
            response = f"Script ready at {filepath}"
            speak(response)
            
            print(f"\n🎉 Done! Total time: [measure this]")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            speak("Sorry, something went wrong. Check the logs.")

if __name__ == "__main__":
    main()
```

**Test:**
```bash
python main.py

# Full flow:
# 1. Say: "Hey Jarvis"
# 2. Hear chime
# 3. Say: "Write a Python script to scrape HackerNews top stories"
# 4. Wait ~10-15 seconds
# 5. Hear: "Script ready at ..."
# 6. Check ~/ai-projects/scrape-hackernews-top-stories/
```

---

## Success Criteria

✅ **Functional:**
- Wake word detection works 90%+ of the time
- Voice recognition accuracy >85%
- Code compiles/runs successfully
- File saved in correct location
- TTS response is clear

✅ **Performance:**
- Total time: <30 seconds (wake word to file saved)
- Voice recognition: <3 seconds
- Code generation: <10 seconds
- File operations: <1 second

✅ **User Experience:**
- Clear audio feedback at each step
- Helpful error messages
- Easy to use (no technical knowledge needed)

---

## Testing Checklist

### Test Case 1: Simple Script
```
Voice: "Write a Python script to print hello world"
Expected:
  ✅ File: ~/ai-projects/print-hello-world/print_hello_world.py
  ✅ Code: print("Hello, World!")
  ✅ README.md created
  ✅ Git initialized
  ✅ TTS response: "Script ready at ..."
```

### Test Case 2: Web Scraper
```
Voice: "Write a Python script to scrape HackerNews top stories"
Expected:
  ✅ File: ~/ai-projects/scrape-hackernews/scrape_hackernews.py
  ✅ Code includes: requests, BeautifulSoup, error handling
  ✅ Code has comments
  ✅ Can run: python scrape_hackernews.py
```

### Test Case 3: JavaScript Function
```
Voice: "Write a JavaScript function to validate email addresses"
Expected:
  ✅ File: ~/ai-projects/validate-email-addresses/validate_email_addresses.js
  ✅ Code: regex-based validation
  ✅ Can run: node validate_email_addresses.js
```

### Test Case 4: Error Handling
```
Voice: [mumble unclear command]
Expected:
  ✅ TTS: "I didn't catch that. Please try again."
  ✅ Returns to listening state
```

### Test Case 5: Unsupported Language
```
Voice: "Write a Rust script to parse JSON"
Expected:
  ✅ Generates code (even if not optimized for Rust)
  ✅ OR: "I'm not familiar with Rust yet, trying anyway..."
```

---

## Metrics to Measure

Track during testing:

- **Wake word accuracy:** X detections / Y attempts
- **STT accuracy:** X correct / Y commands
- **Code quality:** X compiles / Y generated
- **Average time:** Total time from wake word to file saved
- **User satisfaction:** Subjective rating (1-10)

---

## Known Limitations (Acceptable for Prototype)

❌ **No context awareness** - Each command is independent  
❌ **Simple intent parsing** - Only handles "write a [lang] script to [task]"  
❌ **No error recovery** - If code generation fails, just reports error  
❌ **No code execution** - Doesn't test if code runs (manual for now)  
❌ **Basic TTS** - Robotic voice (pyttsx3)  

**Mitigation:** These are addressed in later phases (see roadmap)

---

## Next Steps After Prototype

If prototype succeeds (2-3 days):

1. **Measure & document** - Time, accuracy, user feedback
2. **Demo video** - Record full workflow
3. **Present findings** - Show to stakeholders
4. **Decision point:**
   - ✅ If successful → Proceed to Phase 1 (full implementation)
   - ❌ If issues → Iterate on prototype, address blockers

---

## Deliverables

After 2 days, you should have:

1. ✅ **Working prototype** - Voice → Code in <30 seconds
2. ✅ **Test results** - 5+ successful test cases
3. ✅ **Demo video** - Screen recording of full flow
4. ✅ **Metrics** - Performance data (time, accuracy)
5. ✅ **Lessons learned** - What worked, what didn't

---

## Timeline

**Day 1:**
- Morning: Wake word + voice capture (3-4 hours)
- Afternoon: Test voice input thoroughly (2-3 hours)

**Day 2:**
- Morning: Code generation + file management (3-4 hours)
- Afternoon: Integration + testing (3-4 hours)

**Total: ~12-16 hours** (spread over 2 days)

---

## Risk Mitigation

**Risk:** Wake word doesn't work reliably  
**Mitigation:** Use keyboard trigger as fallback (press spacebar instead)

**Risk:** Whisper STT too slow  
**Mitigation:** Use OpenAI Whisper API ($0.006/min) temporarily

**Risk:** LM Studio not responding  
**Mitigation:** Verify model loaded, warm up with test request

**Risk:** Generated code doesn't compile  
**Mitigation:** Add syntax validation, retry with better prompt

---

## Success Definition

**Prototype is successful if:**

✅ End-to-end flow works 8 out of 10 times  
✅ Total time <30 seconds (wake word to file saved)  
✅ Generated code compiles/runs for simple tasks  
✅ User experience is smooth (no frustrating errors)  

**If successful → Proceed to full implementation (5-week roadmap)**

---

**Status:** Ready to Build  
**Start Date:** [Your choice]  
**Target Completion:** 2 days  
**Owner:** You + Einstein
