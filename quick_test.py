#!/usr/bin/env python3
"""
Quick game test - runs the game for a few seconds to ensure it starts correctly.
"""

import os
import sys
import threading
import time

# Set SDL to use dummy video driver for headless testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import Game

def test_game_startup():
    """Test that the game starts and runs without crashing."""
    try:
        print("Starting game test...")
        game = Game()
        
        # Simulate a few game loop iterations
        for i in range(10):
            # Simulate game updates
            game.update_platforms()
            game.player.update(game.platforms)
            
            # Test platform creation
            if i == 2:
                game.create_platform((300, 400))
            if i == 4:
                game.create_platform((500, 300))
                
            time.sleep(0.01)  # Small delay to simulate real game timing
        
        print("✅ Game startup test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Game startup test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_game_startup()
    if success:
        print("\n🎮 Game is ready to run!")
        print("Run 'python main.py' to start the game with display.")
    else:
        print("\n❌ Game startup test failed.")
        sys.exit(1)