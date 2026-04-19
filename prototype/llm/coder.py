#!/usr/bin/env python3
"""Code generator using Ollama Qwen Coder 32B"""

import requests
import json
import re

def generate_code(task_description):
    """Generate Python code from task description"""
    
    url = "http://localhost:11434/api/generate"
    
    prompt = f"""You are a Python expert. Generate clean, working code for:

Task: {task_description}

Requirements:
- Complete, executable Python code
- Include comments
- Just code, no explanations
- Wrap in ```python ... ```

Generate:"""
    
    payload = {
        "model": "qwen2.5-coder:32b",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        print("🧠 Generating code...")
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        code = result.get("response", "")
        
        # Extract code from markdown
        code_match = re.search(r'```python\n(.*?)\n```', code, re.DOTALL)
        if code_match:
            clean_code = code_match.group(1)
        else:
            clean_code = code
        
        print("✅ Code generated!")
        return clean_code.strip()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    code = generate_code("print hello world")
    print(f"Generated:\n{code}")
