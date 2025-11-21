"""
Quick launch script for the Movie Sentiment Analytics Platform
Run this script to start the application with one command
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if requirements are installed"""
    try:
        import streamlit
        import pymongo
        import torch
        import transformers
        return True
    except ImportError:
        return False

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def check_env_file():
    """Check if .env file exists"""
    env_path = Path(".env")
    if not env_path.exists():
        print("Creating .env file from template...")
        example_path = Path(".env.example")
        if example_path.exists():
            import shutil
            shutil.copy(example_path, env_path)
            print("✓ .env file created. Please configure if needed.")
        else:
            print("⚠ .env.example not found. Continuing with defaults.")

def main():
    """Main launch function"""
    print("=" * 60)
    print("Movie Sentiment Analytics Platform")
    print("Quick Launch Script")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("\n⚠ Required packages not installed.")
        response = input("Install now? (y/n): ")
        if response.lower() == 'y':
            install_requirements()
        else:
            print("Please run: pip install -r requirements.txt")
            sys.exit(1)
    
    # Check .env file
    check_env_file()
    
    # Run test
    print("\nRunning system check...")
    test_result = subprocess.run([sys.executable, "test_system.py"])
    
    if test_result.returncode != 0:
        print("\n⚠ System check found issues.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Launch Streamlit
    print("\n" + "=" * 60)
    print("Launching application...")
    print("The app will open in your browser automatically.")
    print("Press Ctrl+C to stop the server.")
    print("=" * 60 + "\n")
    
    try:
        subprocess.run(["streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\nApplication stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
