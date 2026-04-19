#!/usr/bin/env python3
"""Save code to file with Git tracking"""

import os
from datetime import datetime

def save_code(code, task_description):
    """Save code to ~/ai-projects/ with Git commit"""
    
    # Generate project name
    project_name = task_description.lower()[:30].replace(' ', '-')
    project_dir = os.path.expanduser(f"~/ai-projects/{project_name}")
    
    # Create directory
    os.makedirs(project_dir, exist_ok=True)
    
    # Save code
    code_file = os.path.join(project_dir, "script.py")
    with open(code_file, 'w') as f:
        f.write(code)
    
    print(f"💾 Saved to: {code_file}")
    
    # Git init + commit
    os.chdir(project_dir)
    
    if not os.path.exists('.git'):
        os.system('git init > /dev/null 2>&1')
    
    os.system('git add script.py > /dev/null 2>&1')
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Generated: {task_description} ({timestamp})"
    os.system(f'git commit -m "{commit_msg}" > /dev/null 2>&1')
    
    print("✅ Git commit done!")
    
    return code_file

if __name__ == "__main__":
    test_code = 'print("test")'
    path = save_code(test_code, "test script")
    print(f"Saved to: {path}")
