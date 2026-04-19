#!/usr/bin/env python3
"""
Einstein AI Coding Agent - Prototype MVP
Voice → Code Pipeline

Main orchestrator that connects all modules:
1. Voice input (listener.py)
2. LLM code generation (coder.py)
3. Code execution (runner.py)
4. Storage (manager.py)
"""

import sys
import os
from pathlib import Path
import time

# Add module paths
sys.path.insert(0, str(Path(__file__).parent))

from voice.listener import VoiceListener
from llm.coder import CodeGenerator
from executor.runner import CodeExecutor
from storage.manager import StorageManager


class EinsteinCodingAgent:
    """Main AI Coding Agent orchestrator"""
    
    def __init__(self):
        """Initialize all components"""
        print("🤖 Initializing Einstein AI Coding Agent...")
        
        self.voice_listener = VoiceListener()
        self.code_generator = CodeGenerator()
        self.code_executor = CodeExecutor()
        self.storage_manager = StorageManager()
        
        self.stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0
        }
    
    def run(self):
        """Main execution loop"""
        
        # Display banner
        self._display_banner()
        
        # Verify components
        if not self._verify_setup():
            print("\n❌ Setup incomplete. Please fix the issues above.")
            return
        
        print("\n✅ All systems ready!")
        print("\n" + "="*60)
        print("Ready to generate code from voice commands!")
        print("="*60)
        
        # Main loop
        while True:
            try:
                self._process_request()
                
            except KeyboardInterrupt:
                self._shutdown()
                break
                
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                print("Continuing...")
    
    def _display_banner(self):
        """Display startup banner"""
        banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🤖 EINSTEIN AI CODING AGENT - PROTOTYPE v0.1.0      ║
║                                                          ║
║     Voice → Code in <30 seconds                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def _verify_setup(self) -> bool:
        """Verify all components are working"""
        
        print("\n🔍 Verifying setup...")
        all_ok = True
        
        # Check microphone
        print("\n1. Checking microphone...")
        if self.voice_listener.test_microphone():
            print("   ✅ Microphone ready")
        else:
            print("   ❌ No microphone found")
            all_ok = False
        
        # Check LM Studio
        print("\n2. Checking LM Studio connection...")
        if self.code_generator.test_connection():
            print("   ✅ LM Studio connected")
        else:
            print("   ❌ LM Studio not available")
            print("   ℹ️  Start LM Studio and load Qwen Coder 32B on port 1234")
            all_ok = False
        
        # Check executor
        print("\n3. Checking code execution capabilities...")
        for lang in ['python', 'javascript', 'bash']:
            if self.code_executor.test_execution(lang):
                print(f"   ✅ {lang.capitalize()} execution ready")
            else:
                print(f"   ⚠️  {lang.capitalize()} execution not available")
        
        # Check storage
        print("\n4. Checking storage...")
        projects_dir = Path("~/ai-projects").expanduser()
        if projects_dir.exists():
            print(f"   ✅ Projects directory: {projects_dir}")
        else:
            projects_dir.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Created projects directory: {projects_dir}")
        
        return all_ok
    
    def _process_request(self):
        """Process a single voice → code request"""
        
        self.stats['total_requests'] += 1
        start_time = time.time()
        
        print("\n" + "="*60)
        print(f"Request #{self.stats['total_requests']}")
        print("="*60)
        
        # Step 1: Get voice command
        command = self.voice_listener.listen()
        
        if not command:
            print("\n⚠️  No command received. Try again.")
            self.stats['failed'] += 1
            return
        
        print(f"\n📝 Command: '{command}'")
        
        # Step 2: Determine language and task
        # Simple parsing - extract language if mentioned
        language = self._detect_language(command)
        task = command
        
        print(f"🎯 Language: {language}")
        print(f"🎯 Task: {task}")
        
        # Step 3: Generate code
        try:
            print(f"\n{'─'*60}")
            print("⚙️  GENERATING CODE...")
            print('─'*60)
            
            result = self.code_generator.generate(task, language)
            
            code = result['code']
            filename = result['filename']
            
            print(f"\n✅ Generated {filename} ({len(code)} characters)")
            
            # Preview code
            print(f"\n📄 Code preview:")
            print('─'*60)
            lines = code.split('\n')
            preview_lines = min(20, len(lines))
            print('\n'.join(lines[:preview_lines]))
            if len(lines) > preview_lines:
                print(f"\n... ({len(lines) - preview_lines} more lines)")
            print('─'*60)
            
        except Exception as e:
            print(f"\n❌ Code generation failed: {e}")
            self.stats['failed'] += 1
            return
        
        # Step 4: Validate code
        print(f"\n{'─'*60}")
        print("🔍 VALIDATING CODE...")
        print('─'*60)
        
        validation = self.code_executor.validate(code, language)
        
        if not validation['valid']:
            print(f"\n⚠️  Validation failed: {validation['error']}")
            print("⚠️  Saving anyway (you can fix it manually)")
        
        # Step 5: Save to file
        print(f"\n{'─'*60}")
        print("💾 SAVING TO FILE...")
        print('─'*60)
        
        try:
            save_result = self.storage_manager.save(
                code=code,
                filename=filename,
                language=language,
                task=task
            )
            
            filepath = save_result['filepath']
            project_dir = save_result['project_dir']
            
            print(f"\n✅ Project created: {project_dir}")
            print(f"✅ Main file: {filepath}")
            
        except Exception as e:
            print(f"\n❌ Failed to save: {e}")
            self.stats['failed'] += 1
            return
        
        # Step 6: Optionally test execution (for simple scripts)
        if self._should_auto_execute(code, language):
            print(f"\n{'─'*60}")
            print("▶️  TESTING EXECUTION...")
            print('─'*60)
            
            exec_result = self.code_executor.run(code, filename, language)
            
            if exec_result['success']:
                print("\n✅ Code executed successfully!")
                if exec_result['stdout']:
                    print(f"\nOutput:\n{exec_result['stdout']}")
            else:
                print(f"\n⚠️  Execution failed (exit code: {exec_result['exit_code']})")
                if exec_result['stderr']:
                    print(f"\nError:\n{exec_result['stderr']}")
        
        # Step 7: Summary
        elapsed = time.time() - start_time
        
        print(f"\n{'='*60}")
        print("✅ SUCCESS!")
        print('='*60)
        print(f"📁 Project: {project_dir}")
        print(f"📄 File: {filename}")
        print(f"⏱️  Time: {elapsed:.1f} seconds")
        print('='*60)
        
        self.stats['successful'] += 1
    
    def _detect_language(self, command: str) -> str:
        """
        Detect programming language from command
        
        Args:
            command: Voice command text
            
        Returns:
            Detected language (default: python)
        """
        command_lower = command.lower()
        
        if 'python' in command_lower:
            return 'python'
        elif 'javascript' in command_lower or 'js' in command_lower:
            return 'javascript'
        elif 'typescript' in command_lower or 'ts' in command_lower:
            return 'typescript'
        elif 'bash' in command_lower or 'shell' in command_lower:
            return 'bash'
        elif 'java' in command_lower:
            return 'java'
        elif 'go' in command_lower or 'golang' in command_lower:
            return 'go'
        else:
            # Default to Python
            return 'python'
    
    def _should_auto_execute(self, code: str, language: str) -> bool:
        """
        Determine if code should be auto-executed
        Only for simple, safe scripts
        
        Returns:
            bool: True if safe to auto-execute
        """
        # Don't auto-execute shell scripts (could be dangerous)
        if language in ['bash', 'shell']:
            return False
        
        # Don't auto-execute if code is too long (likely complex)
        if len(code) > 1000:
            return False
        
        # Don't auto-execute if it has certain keywords
        dangerous_keywords = ['os.system', 'subprocess', 'eval', 'exec', 'rm ', 'delete']
        code_lower = code.lower()
        
        for keyword in dangerous_keywords:
            if keyword in code_lower:
                return False
        
        # Otherwise, it's probably safe
        return True
    
    def _shutdown(self):
        """Clean shutdown"""
        print("\n\n" + "="*60)
        print("📊 SESSION STATISTICS")
        print("="*60)
        print(f"Total requests: {self.stats['total_requests']}")
        print(f"Successful: {self.stats['successful']}")
        print(f"Failed: {self.stats['failed']}")
        
        if self.stats['total_requests'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_requests']) * 100
            print(f"Success rate: {success_rate:.1f}%")
        
        print("="*60)
        print("\n👋 Thank you for using Einstein AI Coding Agent!")
        print("   Your projects are saved in ~/ai-projects/\n")


def main():
    """Entry point"""
    agent = EinsteinCodingAgent()
    agent.run()


if __name__ == "__main__":
    main()
