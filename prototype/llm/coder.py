#!/usr/bin/env python3
"""
LLM Integration Module - Generates code using Qwen Coder 32B via LM Studio
"""

import requests
import json
import re
from typing import Dict, Optional


class CodeGenerator:
    """Generates code using LM Studio API"""
    
    def __init__(self, api_url: str = "http://localhost:1234/v1/chat/completions"):
        """
        Initialize code generator
        
        Args:
            api_url: LM Studio API endpoint
        """
        self.api_url = api_url
        self.model = "qwen-coder-32b"  # Adjust based on loaded model
        
    def generate(self, task: str, language: str = "python") -> Dict[str, str]:
        """
        Generate code for the given task
        
        Args:
            task: Description of what the code should do
            language: Programming language (python, javascript, bash, etc.)
            
        Returns:
            Dict with 'code', 'filename', and 'language' keys
        """
        print(f"🤖 Generating {language} code for: {task}")
        
        # Build system prompt
        system_prompt = self._build_system_prompt(language)
        
        # Build user prompt
        user_prompt = self._build_user_prompt(task, language)
        
        # Call LM Studio
        try:
            code = self._call_llm(system_prompt, user_prompt)
            
            # Clean up code (remove markdown if present)
            code = self._clean_code(code)
            
            # Generate filename
            filename = self._generate_filename(task, language)
            
            print(f"✅ Generated {len(code)} characters of code")
            
            return {
                'code': code,
                'filename': filename,
                'language': language
            }
            
        except Exception as e:
            print(f"❌ Code generation failed: {e}")
            raise
    
    def _build_system_prompt(self, language: str) -> str:
        """Build system prompt for the LLM"""
        return f"""You are an expert {language} developer with 10+ years of experience.

Your task is to generate clean, production-ready code that:
- Follows best practices and style guides
- Includes comprehensive error handling
- Has clear, helpful comments
- Is immediately runnable without modifications
- Uses type hints (where applicable)
- Handles edge cases

Generate ONLY the code - no explanations, no markdown formatting, no preamble.
The code should be complete and ready to save to a file."""
    
    def _build_user_prompt(self, task: str, language: str) -> str:
        """Build user prompt for the LLM"""
        return f"""Write a {language} script that: {task}

Requirements:
- Complete, working code only
- Include all necessary imports
- Add docstrings/comments
- Handle errors gracefully
- Make it production-ready

Code:"""
    
    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """
        Call LM Studio API
        
        Returns:
            Generated code as string
        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,  # Lower = more consistent
            "max_tokens": 2000,
            "stream": False
        }
        
        response = requests.post(
            self.api_url,
            json=payload,
            timeout=30  # 30 second timeout
        )
        
        if response.status_code != 200:
            raise Exception(f"LM Studio API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        if 'choices' not in data or len(data['choices']) == 0:
            raise Exception("No response from LLM")
        
        return data['choices'][0]['message']['content']
    
    def _clean_code(self, code: str) -> str:
        """
        Clean up generated code
        - Remove markdown code blocks
        - Strip extra whitespace
        """
        # Remove markdown code blocks
        pattern = r'```(?:\w+)?\s*\n(.*?)\n```'
        match = re.search(pattern, code, re.DOTALL)
        
        if match:
            code = match.group(1)
        
        # Strip leading/trailing whitespace
        code = code.strip()
        
        return code
    
    def _generate_filename(self, task: str, language: str) -> str:
        """
        Generate appropriate filename from task description
        
        Args:
            task: Task description
            language: Programming language
            
        Returns:
            Filename (e.g., "scrape_hackernews.py")
        """
        # Extension mapping
        ext_map = {
            'python': 'py',
            'javascript': 'js',
            'typescript': 'ts',
            'bash': 'sh',
            'shell': 'sh',
            'java': 'java',
            'go': 'go',
            'rust': 'rs'
        }
        
        extension = ext_map.get(language.lower(), 'txt')
        
        # Extract key words from task
        # Remove common words
        stop_words = {'a', 'an', 'the', 'to', 'for', 'of', 'in', 'on', 'at', 'by', 'with'}
        words = [w for w in task.lower().split() if w not in stop_words]
        
        # Take first 3-4 meaningful words
        name_words = words[:4] if len(words) >= 4 else words
        
        # Create filename
        filename = '_'.join(name_words) + '.' + extension
        
        # Clean up special characters
        filename = re.sub(r'[^a-z0-9_.]', '', filename)
        
        return filename
    
    def test_connection(self) -> bool:
        """
        Test if LM Studio is accessible
        
        Returns:
            bool: True if connection successful
        """
        try:
            # Try a simple request
            response = requests.get(
                self.api_url.replace('/v1/chat/completions', '/v1/models'),
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ LM Studio connected: {self.api_url}")
                return True
            else:
                print(f"⚠️  LM Studio responded but with status {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to LM Studio at {self.api_url}")
            print("   Make sure LM Studio is running with a model loaded")
            return False
            
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False


def main():
    """Test the code generator"""
    print("Code Generator Test")
    print("=" * 50)
    
    generator = CodeGenerator()
    
    # Test connection
    if not generator.test_connection():
        print("\n❌ LM Studio not available!")
        print("\nTo fix:")
        print("1. Open LM Studio")
        print("2. Load Qwen Coder 32B model")
        print("3. Start the server on port 1234")
        return
    
    # Test code generation
    test_cases = [
        ("print hello world", "python"),
        ("validate email address", "javascript"),
        ("backup files to zip", "bash")
    ]
    
    for task, lang in test_cases:
        print(f"\n{'='*50}")
        print(f"Test: {task} ({lang})")
        print('='*50)
        
        try:
            result = generator.generate(task, lang)
            print(f"\nFilename: {result['filename']}")
            print(f"\nGenerated code ({len(result['code'])} chars):")
            print('-'*50)
            print(result['code'][:500])  # First 500 chars
            if len(result['code']) > 500:
                print(f"\n... ({len(result['code']) - 500} more characters)")
            print('-'*50)
            
        except Exception as e:
            print(f"❌ Failed: {e}")


if __name__ == "__main__":
    main()
