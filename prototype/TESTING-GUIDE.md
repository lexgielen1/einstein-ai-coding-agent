# Testing Guide - Einstein AI Coding Agent Prototype

## Test Plan Overview

This guide covers how to test the Einstein AI Coding Agent prototype to ensure all components work correctly and meet the success criteria.

## Pre-Test Checklist

Before running tests, ensure:

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Microphone available and working
- [ ] LM Studio running with Qwen Coder 32B on port 1234
- [ ] `~/ai-projects/` directory exists

## Automated Tests

### Run All Tests

```bash
python3 tests/test_basic.py
```

**Expected Output:**
```
TEST SUMMARY
══════════════════════════════════════════════════════════════════════
✅ PASS - Code Generator
✅ PASS - Code Executor
✅ PASS - Storage Manager

Total: 3/3 tests passed

🎉 All tests passed!
```

### Individual Component Tests

#### 1. Voice Listener Test
```bash
python3 voice/listener.py
```

**Test Steps:**
1. Script starts and lists microphones
2. Press ENTER when prompted
3. Speak a clear command: "write a python script to print hello world"
4. Wait for transcription

**Expected:**
- Microphone list displayed
- Recording indicator shown
- Accurate transcription of your command

**Pass Criteria:**
- ✅ Microphone detected
- ✅ Recording completes without error
- ✅ Transcription accuracy >85%

#### 2. Code Generator Test
```bash
python3 llm/coder.py
```

**Test Steps:**
1. Script connects to LM Studio
2. Generates code for 3 test cases

**Expected:**
- Connection successful
- Code generated for each test case
- Code includes imports, docstrings, error handling

**Pass Criteria:**
- ✅ LM Studio connection successful
- ✅ Generated code >50 characters
- ✅ Code is syntactically valid
- ✅ Filename generated correctly

#### 3. Code Executor Test
```bash
python3 executor/runner.py
```

**Test Steps:**
1. Validates Python code syntax
2. Executes simple Python script
3. Validates JavaScript code
4. Executes simple JavaScript script
5. Validates Bash code
6. Executes simple Bash script

**Expected:**
- All validations pass
- All executions produce expected output

**Pass Criteria:**
- ✅ Python validation & execution works
- ✅ JavaScript validation & execution works
- ✅ Bash validation & execution works
- ✅ Output captured correctly

#### 4. Storage Manager Test
```bash
python3 storage/manager.py
```

**Test Steps:**
1. Creates test project
2. Saves code file
3. Creates README.md
4. Initializes git repository

**Expected:**
- Project directory created in `~/ai-projects/`
- All files present
- Git repository initialized

**Pass Criteria:**
- ✅ Project directory created
- ✅ Code file saved correctly
- ✅ README.md generated
- ✅ .metadata.json created
- ✅ Git repository initialized

## Integration Tests

### Full Pipeline Test

```bash
python3 main.py
```

Run these test cases and verify results:

#### Test Case 1: Simple Python Script
**Command:** "Write a Python script to print hello world"

**Expected:**
- Transcription accurate
- Code generated quickly (<15s)
- Code validates successfully
- Project created at `~/ai-projects/print-hello-world/`
- File: `print_hello_world.py`
- README.md present
- Git initialized

**Pass Criteria:**
- ✅ End-to-end time <30 seconds
- ✅ Code runs without errors
- ✅ Output: "Hello, World!" (or similar)

#### Test Case 2: Web Scraper
**Command:** "Write a Python script to scrape HackerNews top stories"

**Expected:**
- More complex code generated
- Includes `requests` or `urllib` imports
- Has error handling
- Includes comments
- Project: `~/ai-projects/scrape-hackernews-top-stories/`

**Pass Criteria:**
- ✅ Code includes HTTP library imports
- ✅ Has error handling (try/except)
- ✅ Code is well-structured with functions
- ✅ Comments explain key parts

#### Test Case 3: JavaScript Function
**Command:** "Write a JavaScript function to validate email addresses"

**Expected:**
- JavaScript code generated
- Includes regex pattern for email validation
- Has test cases or examples
- File: `validate_email_addresses.js`

**Pass Criteria:**
- ✅ Valid JavaScript syntax
- ✅ Uses regex for email validation
- ✅ Can run with `node validate_email_addresses.js`

#### Test Case 4: Bash Script
**Command:** "Write a bash script to list all Python files in a directory"

**Expected:**
- Bash script with shebang
- Uses `find` or similar commands
- Executable permissions set
- File: `list_python_files.sh`

**Pass Criteria:**
- ✅ Valid bash syntax
- ✅ Executable permissions set
- ✅ Script runs without errors

## Performance Tests

### Time Measurements

Track these metrics for each test case:

1. **Voice capture time** (should be ~5s)
2. **Transcription time** (should be <3s)
3. **Code generation time** (should be <15s)
4. **Total time** (should be <30s)

**How to Measure:**
- Main script prints timing automatically
- Note times in test results document

**Target Performance:**
```
Voice capture:     ~5s
Transcription:     <3s
Code generation:   <15s
Validation:        <1s
Storage:           <1s
────────────────────────
Total:            <25s ✅
```

### Accuracy Tests

Track these metrics:

1. **Voice recognition accuracy**
   - Commands tested: 10
   - Correctly transcribed: X
   - Accuracy: (X/10) * 100%
   - Target: >85%

2. **Code quality**
   - Scripts generated: 10
   - Compiles/validates: X
   - Runs without errors: Y
   - Target: >80%

## Error Handling Tests

### Test Case: Unclear Voice Command
**Steps:**
1. Press ENTER
2. Mumble or speak very quietly
3. Observe behavior

**Expected:**
- "Could not understand audio" message
- Returns to listening state
- No crash

### Test Case: LM Studio Offline
**Steps:**
1. Stop LM Studio server
2. Try to generate code

**Expected:**
- "LM Studio not available" error
- Helpful error message
- No crash

### Test Case: Invalid Code Generated
**Steps:**
1. (This should be rare, but test if it happens)

**Expected:**
- Validation catches syntax errors
- Warning displayed
- Code still saved (user can fix manually)

## User Experience Tests

### Ease of Use
- [ ] Setup process is straightforward
- [ ] Error messages are helpful
- [ ] Progress is clearly indicated
- [ ] Results are easy to find

### Feedback Quality
- [ ] Clear indication of each step
- [ ] Appropriate use of emojis/icons
- [ ] Color coding works (if terminal supports it)
- [ ] Timing information provided

## Success Criteria Summary

For prototype to be considered **successful**, it must achieve:

### Functional Requirements
- ✅ Voice input works 90%+ of the time
- ✅ Voice recognition accuracy >85%
- ✅ Code compiles/runs successfully >80%
- ✅ Files saved in correct location 100%

### Performance Requirements
- ✅ Total time <30 seconds (average)
- ✅ Voice recognition <3 seconds
- ✅ Code generation <15 seconds

### User Experience Requirements
- ✅ Clear feedback at each step
- ✅ Helpful error messages
- ✅ No confusing prompts
- ✅ Easy recovery from errors

## Test Results Template

Use this template to document test results:

```markdown
# Test Results - Einstein AI Coding Agent Prototype

**Date:** 2026-04-19
**Tester:** [Your Name]
**Environment:** macOS 14.0 / Python 3.11

## Automated Tests
- [ ] All automated tests passed

## Integration Tests

### Test Case 1: Simple Python Script
- [ ] Passed
- Time: ____ seconds
- Notes: ___________

### Test Case 2: Web Scraper
- [ ] Passed
- Time: ____ seconds
- Notes: ___________

### Test Case 3: JavaScript Function
- [ ] Passed
- Time: ____ seconds
- Notes: ___________

### Test Case 4: Bash Script
- [ ] Passed
- Time: ____ seconds
- Notes: ___________

## Performance Metrics
- Average total time: ____ seconds
- Voice recognition accuracy: ____%
- Code quality (runs without errors): ____%

## Issues Found
1. ___________
2. ___________

## Recommendations
1. ___________
2. ___________

## Overall Assessment
- [ ] Prototype is ready for demo
- [ ] Needs minor fixes before demo
- [ ] Needs significant work

**Summary:** ___________
```

## Next Steps After Testing

1. **Document Results**
   - Fill in test results template
   - Note any issues or bugs
   - Measure all performance metrics

2. **Record Demo Video**
   - Show successful end-to-end flow
   - Demonstrate multiple languages
   - Highlight key features

3. **Prepare Presentation**
   - Show test results
   - Demo video
   - Performance metrics
   - Lessons learned

4. **Decide on Next Phase**
   - If successful → Proceed to full implementation
   - If issues → Iterate on prototype

---

**Ready to test?**

```bash
# Run all tests
python3 tests/test_basic.py

# Start manual testing
python3 main.py
```

Good luck! 🚀
