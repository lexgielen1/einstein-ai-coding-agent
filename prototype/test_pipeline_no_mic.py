#!/usr/bin/env python3
"""Test pipeline without microphone (text input)"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from llm.coder import generate_code
from executor.runner import execute_code
from storage.manager import save_code

def test_pipeline(command):
    """Test without voice input"""
    
    print("=" * 60)
    print(f"🧪 Testing: {command}")
    print("=" * 60)
    
    # Generate code
    print("\n1️⃣ Generating code...")
    code = generate_code(command)
    
    if not code:
        print("❌ Code generation failed")
        return False
    
    print(f"\n📄 Generated Code:\n{'-'*60}\n{code}\n{'-'*60}")
    
    # Save code
    print("\n2️⃣ Saving code...")
    file_path = save_code(code, command)
    
    # Execute code
    print("\n3️⃣ Executing code...")
    result = execute_code(code)
    
    print(f"\n📊 Result:")
    print(f"Success: {result.get('success', False)}")
    
    if result.get('stdout'):
        print(f"Output: {result['stdout']}")
    
    if result.get('stderr'):
        print(f"Errors: {result['stderr']}")
    
    success = result.get('success', False)
    
    print(f"\n{'✅ TEST PASSED' if success else '❌ TEST FAILED'}")
    print(f"Code saved to: {file_path}")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    # Test cases
    tests = [
        "print hello world",
        "create a function to add two numbers",
        "write a script to get current date and time"
    ]
    
    results = []
    
    for test in tests:
        success = test_pipeline(test)
        results.append((test, success))
        print("\n\n")
    
    # Summary
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test}")
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} passed ({passed*100//total}%)")
    print("=" * 60)
