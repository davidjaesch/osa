#!/usr/bin/env python3
"""
Setup script for OSA game.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False

def main():
    """Main setup function."""
    print("Setting up OSA game...")
    
    # Check if we're in the right directory
    if not os.path.exists("requirements.txt"):
        print("Error: requirements.txt not found. Please run this script from the game directory.")
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    print("\nSetup complete!")
    print("To run the game: python main.py")
    print("To run tests: python test_main.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)