#!/usr/bin/env python3
"""Execute Python code in subprocess"""

import subprocess
import tempfile
import os

def execute_code(code, timeout=10):
    """Execute Python code and return output"""
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        print("⚙️ Executing...")
        
        result = subprocess.run(
            ['python3', temp_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            print("✅ Success!")
            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        else:
            print(f"❌ Failed (exit {result.returncode})")
            return {
                'success': False,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    finally:
        os.unlink(temp_file)

if __name__ == "__main__":
    test = 'print("Hello!")'
    result = execute_code(test)
    print(f"Result: {result}")
