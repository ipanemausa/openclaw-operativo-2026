import os
import sys
import json
import subprocess
from pathlib import Path

def clone_repo(repo='DeepSeek-AI/DeepSeek-Model', branch='main'):
    token = os.getenv('DEEPSEEK_GITHUB_TOKEN')
    if not token:
        return {'status': 'error', 'message': 'Missing DEEPSEEK_GITHUB_TOKEN environment variable'}
    auth_repo = f'https://{token}@github.com/{repo}.git'
    target_dir = Path(__file__).resolve().parent.parent / 'repos' / repo.split('/')[-1]
    if target_dir.exists():
        try:
            subprocess.check_call(['git', '-C', str(target_dir), 'pull', 'origin', branch])
        except subprocess.CalledProcessError as e:
            return {'status': 'error', 'message': f'Git pull failed: {e}'}
    else:
        try:
            subprocess.check_call(['git', 'clone', '-b', branch, auth_repo, str(target_dir)])
        except subprocess.CalledProcessError as e:
            return {'status': 'error', 'message': f'Git clone failed: {e}'}
    # Build step if present
    build_success = False
    build_msg = 'No build step detected'
    if (target_dir / 'setup.py').exists():
        try:
            subprocess.check_call([sys.executable, 'setup.py', 'install'], cwd=str(target_dir))
            build_success = True
            build_msg = 'setup.py install completed'
        except subprocess.CalledProcessError as e:
            build_msg = f'setup.py failed: {e}'
    elif (target_dir / 'Makefile').exists():
        try:
            subprocess.check_call(['make'], cwd=str(target_dir))
            build_success = True
            build_msg = 'make completed'
        except subprocess.CalledProcessError as e:
            build_msg = f'make failed: {e}'
    return {'status': 'ok', 'repoPath': str(target_dir), 'build': build_success, 'message': build_msg}

if __name__ == '__main__':
    repo = os.getenv('DEEPSEEK_GIT_REPO', 'DeepSeek-AI/DeepSeek-Model')
    branch = os.getenv('DEEPSEEK_GIT_BRANCH', 'main')
    result = clone_repo(repo, branch)
    print(json.dumps(result))
