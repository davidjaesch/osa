#!/usr/bin/env python3
"""
Validation script to test the game functionality without requiring a display.
"""

import os
import sys
import time

# Set SDL to use dummy video driver for headless testing
os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import Game, TemporaryPlatform, Player, MAX_PLATFORMS, PLATFORM_DURATION

def test_game_initialization():
    """Test that the game initializes correctly."""
    print("Testing game initialization...")
    try:
        game = Game()
        print("✅ Game initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Game initialization failed: {e}")
        return False

def test_platform_creation_and_management():
    """Test platform creation and management functionality."""
    print("\nTesting platform creation and management...")
    
    try:
        game = Game()
        
        # Test creating platforms up to limit
        print(f"Testing platform creation limit ({MAX_PLATFORMS} max)...")
        for i in range(MAX_PLATFORMS):
            result = game.create_platform((100 + i * 150, 300))
            if not result:
                print(f"❌ Failed to create platform {i+1}")
                return False
        
        print(f"✅ Successfully created {MAX_PLATFORMS} platforms")
        
        # Test that creating beyond limit fails
        result = game.create_platform((700, 300))
        if result:
            print("❌ Should not be able to create platform beyond limit")
            return False
        
        print("✅ Correctly prevented creation beyond limit")
        
        # Test platform expiration
        print("Testing platform expiration...")
        initial_count = len(game.platforms)
        
        # Add a platform with very short duration
        short_platform = TemporaryPlatform(500, 400, duration=0.1)
        game.platforms.append(short_platform)
        expected_count = initial_count + 1
        
        # Verify platform was added
        if len(game.platforms) != expected_count:
            print("❌ Platform was not added correctly")
            return False
        
        time.sleep(0.15)  # Wait for expiration
        game.update_platforms()  # Clean up expired platforms
        
        if len(game.platforms) == initial_count:
            print("✅ Platform expired and was removed correctly")
        else:
            print(f"❌ Platform should have expired. Expected {initial_count}, got {len(game.platforms)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Platform management test failed: {e}")
        return False

def test_player_functionality():
    """Test player functionality."""
    print("\nTesting player functionality...")
    
    try:
        game = Game()
        player = game.player
        
        # Test initial state
        if player.vel_x != 0 or player.vel_y != 0:
            print("❌ Player should start with zero velocity")
            return False
        
        # Test movement
        player.move_left()
        if player.vel_x >= 0:
            print("❌ Player should move left with negative velocity")
            return False
        
        player.move_right()
        if player.vel_x <= 0:
            print("❌ Player should move right with positive velocity")
            return False
        
        player.stop_horizontal()
        if player.vel_x != 0:
            print("❌ Player should stop horizontal movement")
            return False
        
        print("✅ Player movement controls work correctly")
        return True
        
    except Exception as e:
        print(f"❌ Player functionality test failed: {e}")
        return False

def test_acceptance_criteria():
    """Test all acceptance criteria."""
    print("\nTesting acceptance criteria...")
    
    try:
        game = Game()
        
        # Criteria 1: Player can create a temporary platform at a valid location
        print("1. Testing platform creation at valid location...")
        result = game.create_platform((300, 400))
        if not result or len(game.platforms) == 0:
            print("❌ Failed to create platform at valid location")
            return False
        print("✅ Platform created at valid location")
        
        # Criteria 2: Platform disappears after a certain amount of time
        print("2. Testing platform expiration...")
        test_platform = TemporaryPlatform(100, 200, duration=0.1)
        if test_platform.is_expired():
            print("❌ Platform should not be expired immediately")
            return False
        
        time.sleep(0.15)
        if not test_platform.is_expired():
            print("❌ Platform should be expired after duration")
            return False
        print("✅ Platform expires after specified time")
        
        # Criteria 3: Player cannot create more than certain number of platforms
        print("3. Testing platform limit enforcement...")
        game.platforms = []  # Clear platforms
        
        # Create platforms up to limit
        created_count = 0
        for i in range(MAX_PLATFORMS + 2):  # Try to create more than limit
            if game.create_platform((100 + i * 120, 300)):
                created_count += 1
        
        if created_count != MAX_PLATFORMS:
            print(f"❌ Should create exactly {MAX_PLATFORMS} platforms, created {created_count}")
            return False
        
        print(f"✅ Platform limit enforced correctly ({MAX_PLATFORMS} max)")
        
        return True
        
    except Exception as e:
        print(f"❌ Acceptance criteria test failed: {e}")
        return False

def main():
    """Run all validation tests."""
    print("OSA Game Validation")
    print("=" * 50)
    
    tests = [
        test_game_initialization,
        test_platform_creation_and_management,
        test_player_functionality,
        test_acceptance_criteria
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"\n❌ Test failed: {test.__name__}")
    
    print("\n" + "=" * 50)
    print(f"Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All validation tests passed! The game is ready to use.")
        print("\nTo run the game with display: python main.py")
        print("To run unit tests: python test_main.py")
        return True
    else:
        print("❌ Some validation tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)