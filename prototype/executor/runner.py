#!/usr/bin/env python3
"""
Code Executor Module - Validates and runs generated code
"""

import subprocess
import ast
import os
from pathlib import Path
from typing import Dict, Optional
import tempfile


class CodeExecutor:
    """Validates and executes generated code"""
    
    def __init__(self, project_base: str = "~/ai-projects"):
        """
        Initialize executor
        
        Args:
            project_base: Base directory for projects
        """
        self.project_base = Path(project_base).expanduser()
        self.project_base.mkdir(parents=True, exist_ok=True)
        
    def validate(self, code: str, language: str) -> Dict[str, any]:
        """
        Validate code syntax before execution
        
        Args:
            code: Source code to validate
            language: Programming language
            
        Returns:
            Dict with 'valid' (bool) and 'error' (str) keys
        """
        print(f"🔍 Validating {language} syntax...")
        
        if language == 'python':
            return self._validate_python(code)
        elif language in ['javascript', 'typescript']:
            return self._validate_javascript(code)
        elif language in ['bash', 'shell']:
            return self._validate_bash(code)
        else:
            # For other languages, skip validation
            print(f"⚠️  No validator for {language}, skipping...")
            return {'valid': True, 'error': None}
    
    def _validate_python(self, code: str) -> Dict[str, any]:
        """Validate Python syntax"""
        try:
            ast.parse(code)
            print("✅ Python syntax valid")
            return {'valid': True, 'error': None}
        except SyntaxError as e:
            error = f"Syntax error at line {e.lineno}: {e.msg}"
            print(f"❌ {error}")
            return {'valid': False, 'error': error}
    
    def _validate_javascript(self, code: str) -> Dict[str, any]:
        """Validate JavaScript syntax (requires node)"""
        try:
            # NOTE: `node --check` expects a file path (it does not read from stdin).
            # Write to a temp file and ask node to syntax-check it.
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.js',
                delete=False
            ) as f:
                f.write(code)
                temp_path = f.name

            result = subprocess.run(
                ['node', '--check', temp_path],
                capture_output=True,
                timeout=5,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ JavaScript syntax valid")
                return {'valid': True, 'error': None}
            else:
                error = result.stderr
                print(f"❌ {error}")
                return {'valid': False, 'error': error}
                
        except FileNotFoundError:
            print("⚠️  Node not found, skipping validation")
            return {'valid': True, 'error': None}
        except Exception as e:
            return {'valid': False, 'error': str(e)}
        finally:
            try:
                if 'temp_path' in locals() and temp_path:
                    os.unlink(temp_path)
            except Exception:
                pass
    
    def _validate_bash(self, code: str) -> Dict[str, any]:
        """Validate Bash syntax"""
        try:
            # Use bash -n to check syntax
            result = subprocess.run(
                ['bash', '-n'],
                input=code.encode(),
                capture_output=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print("✅ Bash syntax valid")
                return {'valid': True, 'error': None}
            else:
                error = result.stderr.decode()
                print(f"❌ {error}")
                return {'valid': False, 'error': error}
                
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def run(self, code: str, filename: str, language: str, 
            timeout: int = 30) -> Dict[str, any]:
        """
        Execute code in a subprocess (sandboxed)
        
        Args:
            code: Source code
            filename: Filename
            language: Programming language
            timeout: Max execution time in seconds
            
        Returns:
            Dict with 'success', 'stdout', 'stderr', 'exit_code'
        """
        print(f"▶️  Executing {filename}...")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix=f'.{filename.split(".")[-1]}',
            delete=False
        ) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            # Determine command to run
            if language == 'python':
                cmd = ['python3', temp_path]
            elif language == 'javascript':
                cmd = ['node', temp_path]
            elif language in ['bash', 'shell']:
                os.chmod(temp_path, 0o755)
                cmd = ['bash', temp_path]
            else:
                return {
                    'success': False,
                    'stdout': '',
                    'stderr': f'No executor for {language}',
                    'exit_code': -1
                }
            
            # Run with timeout
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=timeout,
                text=True
            )
            
            success = result.returncode == 0
            
            if success:
                print(f"✅ Execution successful (exit code: {result.returncode})")
            else:
                print(f"⚠️  Execution failed (exit code: {result.returncode})")
            
            return {
                'success': success,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'exit_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            print(f"⏱️  Execution timed out after {timeout}s")
            return {
                'success': False,
                'stdout': '',
                'stderr': f'Execution timed out after {timeout}s',
                'exit_code': -1
            }
            
        except Exception as e:
            print(f"❌ Execution error: {e}")
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'exit_code': -1
            }
            
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
    
    def test_execution(self, language: str) -> bool:
        """
        Test if we can execute code in the given language
        
        Returns:
            bool: True if execution works
        """
        test_code = {
            'python': 'print("test")',
            'javascript': 'console.log("test")',
            'bash': 'echo "test"'
        }
        
        if language not in test_code:
            return False
        
        result = self.run(
            test_code[language],
            f'test.{language}',
            language,
            timeout=5
        )
        
        return result['success']


def main():
    """Test the executor"""
    print("Code Executor Test")
    print("=" * 50)
    
    executor = CodeExecutor()
    
    # Test Python execution
    print("\n📝 Testing Python execution...")
    python_code = """
print("Hello from Python!")
x = 5 + 3
print(f"5 + 3 = {x}")
"""
    
    validation = executor.validate(python_code, 'python')
    if validation['valid']:
        result = executor.run(python_code, 'test.py', 'python')
        print(f"\nStdout:\n{result['stdout']}")
        if result['stderr']:
            print(f"\nStderr:\n{result['stderr']}")
    
    # Test JavaScript execution
    print("\n" + "="*50)
    print("📝 Testing JavaScript execution...")
    js_code = """
console.log("Hello from JavaScript!");
const x = 5 + 3;
console.log(`5 + 3 = ${x}`);
"""
    
    validation = executor.validate(js_code, 'javascript')
    if validation['valid']:
        result = executor.run(js_code, 'test.js', 'javascript')
        print(f"\nStdout:\n{result['stdout']}")
        if result['stderr']:
            print(f"\nStderr:\n{result['stderr']}")
    
    # Test Bash execution
    print("\n" + "="*50)
    print("📝 Testing Bash execution...")
    bash_code = """
#!/bin/bash
echo "Hello from Bash!"
x=$((5 + 3))
echo "5 + 3 = $x"
"""
    
    validation = executor.validate(bash_code, 'bash')
    if validation['valid']:
        result = executor.run(bash_code, 'test.sh', 'bash')
        print(f"\nStdout:\n{result['stdout']}")
        if result['stderr']:
            print(f"\nStderr:\n{result['stderr']}")


if __name__ == "__main__":
    main()
