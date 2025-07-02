#!/usr/bin/env python3
"""
Tests for the OSA temporary platform creation feature.
"""

import unittest
import time
import sys
import os

# Add the current directory to the path to import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import TemporaryPlatform, Player, Game, PLATFORM_DURATION, MAX_PLATFORMS, SCREEN_WIDTH, SCREEN_HEIGHT


class TestTemporaryPlatform(unittest.TestCase):
    """Test cases for the TemporaryPlatform class."""
    
    def test_platform_creation(self):
        """Test that a platform is created with correct properties."""
        platform = TemporaryPlatform(100, 200)
        self.assertEqual(platform.x, 100)
        self.assertEqual(platform.y, 200)
        self.assertEqual(platform.width, 100)  # PLATFORM_WIDTH
        self.assertEqual(platform.height, 20)  # PLATFORM_HEIGHT
        self.assertFalse(platform.is_expired())
    
    def test_platform_expiration(self):
        """Test that a platform expires after the specified duration."""
        # Create a platform with a very short duration for testing
        platform = TemporaryPlatform(100, 200, duration=0.1)
        self.assertFalse(platform.is_expired())
        
        # Wait for the platform to expire
        time.sleep(0.15)
        self.assertTrue(platform.is_expired())
    
    def test_remaining_time(self):
        """Test that remaining time calculation works correctly."""
        platform = TemporaryPlatform(100, 200, duration=1.0)
        initial_time = platform.get_remaining_time()
        self.assertAlmostEqual(initial_time, 1.0, delta=0.1)
        
        # Wait a bit and check again
        time.sleep(0.1)
        remaining_time = platform.get_remaining_time()
        self.assertLess(remaining_time, initial_time)
        self.assertGreater(remaining_time, 0.8)


class TestPlayer(unittest.TestCase):
    """Test cases for the Player class."""
    
    def test_player_creation(self):
        """Test that a player is created with correct properties."""
        player = Player(100, 200)
        self.assertEqual(player.x, 100)
        self.assertEqual(player.y, 200)
        self.assertEqual(player.vel_x, 0)
        self.assertEqual(player.vel_y, 0)
        self.assertFalse(player.on_ground)
    
    def test_player_movement(self):
        """Test player movement functions."""
        player = Player(100, 200)
        
        # Test horizontal movement
        player.move_left()
        self.assertEqual(player.vel_x, -5)  # PLAYER_SPEED
        
        player.move_right()
        self.assertEqual(player.vel_x, 5)
        
        player.stop_horizontal()
        self.assertEqual(player.vel_x, 0)


class TestGame(unittest.TestCase):
    """Test cases for the Game class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # We can't fully initialize pygame in tests, so we'll test the logic parts
        self.game = Game()
    
    def test_platform_creation_limit(self):
        """Test that the game respects the maximum platform limit."""
        # Clear any existing platforms
        self.game.platforms = []
        
        # Create platforms up to the limit
        for i in range(MAX_PLATFORMS):
            result = self.game.create_platform((100 + i * 150, 300))
            self.assertTrue(result)
        
        self.assertEqual(len(self.game.platforms), MAX_PLATFORMS)
        
        # Try to create one more platform - should fail
        result = self.game.create_platform((100, 400))
        self.assertFalse(result)
        self.assertEqual(len(self.game.platforms), MAX_PLATFORMS)
    
    def test_platform_position_validation(self):
        """Test that platforms are created at valid positions."""
        self.game.platforms = []
        
        # Test valid position
        result = self.game.create_platform((200, 300))
        self.assertTrue(result)
        self.assertEqual(len(self.game.platforms), 1)
        
        # Test position too close to existing platform (should fail)
        result = self.game.create_platform((210, 310))  # Very close to the first platform
        self.assertFalse(result)
        self.assertEqual(len(self.game.platforms), 1)
    
    def test_platform_cleanup(self):
        """Test that expired platforms are removed."""
        self.game.platforms = []
        
        # Create a platform with very short duration
        platform = TemporaryPlatform(100, 200, duration=0.1)
        self.game.platforms.append(platform)
        self.assertEqual(len(self.game.platforms), 1)
        
        # Wait for expiration
        time.sleep(0.15)
        
        # Update platforms (this should remove expired ones)
        self.game.update_platforms()
        self.assertEqual(len(self.game.platforms), 0)
    
    def test_platform_bounds_validation(self):
        """Test that platforms are kept within screen bounds."""
        self.game.platforms = []
        
        # Test position outside screen bounds
        result = self.game.create_platform((-50, 300))  # Outside left edge
        if result:  # If platform was created, it should be adjusted to valid bounds
            platform = self.game.platforms[-1]
            self.assertGreaterEqual(platform.x, 0)
        
        # Test position beyond right edge
        result = self.game.create_platform((SCREEN_WIDTH + 50, 300))
        if result:
            platform = self.game.platforms[-1]
            self.assertLessEqual(platform.x + platform.width, SCREEN_WIDTH)


class TestAcceptanceCriteria(unittest.TestCase):
    """Test cases that verify the acceptance criteria are met."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()
    
    def test_player_can_create_platform_at_valid_location(self):
        """Acceptance Criteria: The player can create a temporary platform at a valid location."""
        self.game.platforms = []
        
        # Test creating a platform at a valid location
        valid_position = (300, 400)
        result = self.game.create_platform(valid_position)
        
        self.assertTrue(result, "Player should be able to create a platform at a valid location")
        self.assertEqual(len(self.game.platforms), 1, "One platform should be created")
        
        platform = self.game.platforms[0]
        self.assertIsInstance(platform, TemporaryPlatform, "Created object should be a TemporaryPlatform")
    
    def test_platform_disappears_after_time(self):
        """Acceptance Criteria: The platform disappears after a certain amount of time."""
        self.game.platforms = []
        
        # Create a platform with short duration for testing
        platform = TemporaryPlatform(100, 200, duration=0.1)
        self.game.platforms.append(platform)
        
        # Initially, platform should not be expired
        self.assertFalse(platform.is_expired(), "Platform should not be expired immediately after creation")
        
        # Wait for expiration
        time.sleep(0.15)
        
        # Platform should now be expired
        self.assertTrue(platform.is_expired(), "Platform should be expired after duration")
        
        # Update platforms to remove expired ones
        self.game.update_platforms()
        self.assertEqual(len(self.game.platforms), 0, "Expired platform should be removed from game")
    
    def test_platform_limit_enforced(self):
        """Acceptance Criteria: The player cannot create more than a certain number of platforms at once."""
        self.game.platforms = []
        
        # Create platforms up to the maximum limit
        platforms_created = 0
        for i in range(MAX_PLATFORMS + 2):  # Try to create more than the limit
            result = self.game.create_platform((100 + i * 120, 300))
            if result:
                platforms_created += 1
        
        self.assertEqual(platforms_created, MAX_PLATFORMS, 
                        f"Should only be able to create {MAX_PLATFORMS} platforms")
        self.assertEqual(len(self.game.platforms), MAX_PLATFORMS, 
                        f"Game should have exactly {MAX_PLATFORMS} active platforms")
        
        # Try to create one more - should fail
        result = self.game.create_platform((500, 400))
        self.assertFalse(result, "Creating platform beyond limit should fail")
        self.assertEqual(len(self.game.platforms), MAX_PLATFORMS, 
                        "Platform count should remain at maximum after failed creation")


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)