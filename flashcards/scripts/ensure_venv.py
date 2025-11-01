#!/usr/bin/env python3
"""
Ensures virtual environment is set up and runs scripts with dependencies available.
This wrapper handles venv creation and dependency installation automatically.
"""

import os
import sys
import subprocess
from pathlib import Path

def ensure_venv():
    """Ensure virtual environment exists and dependencies are installed."""
    skill_dir = Path(__file__).parent.parent
    venv_dir = skill_dir / "venv"
    requirements_file = skill_dir / "requirements.txt"

    # Check if we're already in a venv
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        return True

    # Create venv if it doesn't exist
    if not venv_dir.exists():
        print("Creating virtual environment...", file=sys.stderr)
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

    # Determine python executable in venv
    if sys.platform == "win32":
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:
        venv_python = venv_dir / "bin" / "python"

    # Check if dependencies are installed
    try:
        result = subprocess.run(
            [str(venv_python), "-c", "import reportlab"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise ImportError
    except (subprocess.CalledProcessError, ImportError):
        print("Installing dependencies...", file=sys.stderr)
        subprocess.run(
            [str(venv_python), "-m", "pip", "install", "-q", "-r", str(requirements_file)],
            check=True
        )

    return venv_python

if __name__ == "__main__":
    # This script can be used as a wrapper
    if len(sys.argv) < 2:
        print("Usage: ensure_venv.py <script.py> [args...]", file=sys.stderr)
        sys.exit(1)

    venv_python = ensure_venv()

    # Re-run with the venv python if needed
    if not (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
        script_to_run = sys.argv[1]
        script_args = sys.argv[2:]
        os.execv(str(venv_python), [str(venv_python), script_to_run] + script_args)
