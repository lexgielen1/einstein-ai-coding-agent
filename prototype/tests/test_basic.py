#!/usr/bin/env python3
"""
Basic integration tests for Einstein AI Coding Agent
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from llm.coder import CodeGenerator
from executor.runner import CodeExecutor
from storage.manager import StorageManager


def test_code_generator():
    """Test code generation"""
    print("\n" + "="*60)
    print("TEST: Code Generator")
    print("="*60)
    
    generator = CodeGenerator()
    
    # Test connection
    if not generator.test_connection():
        print("❌ FAILED: LM Studio not available")
        return False
    
    # Generate simple code
    try:
        result = generator.generate("print hello world", "python")
        
        if 'code' not in result or 'filename' not in result:
            print("❌ FAILED: Invalid result structure")
            return False
        
        if len(result['code']) < 10:
            print("❌ FAILED: Code too short")
            return False
        
        print("✅ PASSED: Code generation works")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_code_executor():
    """Test code execution"""
    print("\n" + "="*60)
    print("TEST: Code Executor")
    print("="*60)
    
    executor = CodeExecutor()
    
    # Test Python
    python_code = 'print("test")'
    result = executor.run(python_code, "test.py", "python")
    
    if not result['success']:
        print(f"❌ FAILED: Python execution failed - {result['stderr']}")
        return False
    
    if "test" not in result['stdout']:
        print("❌ FAILED: Python output incorrect")
        return False
    
    print("✅ PASSED: Code execution works")
    return True


def test_storage_manager():
    """Test storage manager"""
    print("\n" + "="*60)
    print("TEST: Storage Manager")
    print("="*60)
    
    manager = StorageManager()
    
    # Save test file
    try:
        result = manager.save(
            code='print("test")',
            filename="test_storage.py",
            language="python",
            task="test storage"
        )
        
        if 'filepath' not in result:
            print("❌ FAILED: No filepath in result")
            return False
        
        filepath = Path(result['filepath'])
        if not filepath.exists():
            print(f"❌ FAILED: File not created at {filepath}")
            return False
        
        print(f"✅ PASSED: Storage works (created {filepath})")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("EINSTEIN AI CODING AGENT - PROTOTYPE TESTS")
    print("="*70)
    
    tests = [
        ("Code Generator", test_code_generator),
        ("Code Executor", test_code_executor),
        ("Storage Manager", test_storage_manager)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ TEST CRASHED: {name} - {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
