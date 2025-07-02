#!/usr/bin/env python3
"""
OSA Game - Temporary Platform Creation Feature
A simple 2D platformer where players can create temporary platforms.
"""

import pygame
import sys
import time
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Game settings
PLATFORM_DURATION = 5.0  # Platform lasts 5 seconds
MAX_PLATFORMS = 3  # Maximum number of active platforms
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLAYER_SIZE = 30
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5


class TemporaryPlatform:
    """Represents a temporary platform that disappears after a certain time."""
    
    def __init__(self, x: int, y: int, duration: float = PLATFORM_DURATION):
        self.x = x
        self.y = y
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT
        self.creation_time = time.time()
        self.duration = duration
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def is_expired(self) -> bool:
        """Check if the platform has expired."""
        return time.time() - self.creation_time > self.duration
    
    def get_remaining_time(self) -> float:
        """Get the remaining time before the platform expires."""
        return max(0, self.duration - (time.time() - self.creation_time))
    
    def draw(self, screen: pygame.Surface):
        """Draw the platform with visual indication of remaining time."""
        remaining_ratio = self.get_remaining_time() / self.duration
        
        # Change color based on remaining time
        if remaining_ratio > 0.5:
            color = GREEN
        elif remaining_ratio > 0.2:
            color = YELLOW
        else:
            color = RED
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Draw a timer bar
        bar_width = int(self.width * remaining_ratio)
        if bar_width > 0:
            timer_rect = pygame.Rect(self.x, self.y - 5, bar_width, 3)
            pygame.draw.rect(screen, WHITE, timer_rect)


class Player:
    """Represents the player character."""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self, platforms: List[TemporaryPlatform]):
        """Update player position and handle collisions."""
        # Apply gravity
        if not self.on_ground:
            self.vel_y += GRAVITY
        
        # Update horizontal position
        self.x += self.vel_x
        self.rect.x = self.x
        
        # Update vertical position
        self.y += self.vel_y
        self.rect.y = self.y
        
        # Ground collision (simple floor)
        self.on_ground = False
        if self.y + self.height >= SCREEN_HEIGHT - 50:
            self.y = SCREEN_HEIGHT - 50 - self.height
            self.vel_y = 0
            self.on_ground = True
            self.rect.y = self.y
        
        # Platform collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Landing on top of platform
                if self.vel_y > 0 and self.y < platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    self.rect.y = self.y
        
        # Keep player on screen
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        self.rect.x = self.x
    
    def jump(self):
        """Make the player jump if on ground."""
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
    
    def move_left(self):
        """Move player left."""
        self.vel_x = -PLAYER_SPEED
    
    def move_right(self):
        """Move player right."""
        self.vel_x = PLAYER_SPEED
    
    def stop_horizontal(self):
        """Stop horizontal movement."""
        self.vel_x = 0
    
    def draw(self, screen: pygame.Surface):
        """Draw the player."""
        pygame.draw.rect(screen, BLUE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)


class Game:
    """Main game class that handles the game loop and platform management."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("OSA - Temporary Platform Creator")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize player
        self.player = Player(100, SCREEN_HEIGHT - 100)
        
        # Platform management
        self.platforms: List[TemporaryPlatform] = []
        
        # Font for UI
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def create_platform(self, mouse_pos: Tuple[int, int]) -> bool:
        """Create a platform at the mouse position if valid."""
        x, y = mouse_pos
        
        # Check if we're at the platform limit
        if len(self.platforms) >= MAX_PLATFORMS:
            return False
        
        # Validate position (not too close to player, within screen bounds)
        platform_x = x - PLATFORM_WIDTH // 2
        platform_y = y - PLATFORM_HEIGHT // 2
        
        # Keep platform within screen bounds
        platform_x = max(0, min(platform_x, SCREEN_WIDTH - PLATFORM_WIDTH))
        platform_y = max(0, min(platform_y, SCREEN_HEIGHT - PLATFORM_HEIGHT - 50))
        
        # Check if position is valid (not overlapping with player or other platforms)
        new_platform_rect = pygame.Rect(platform_x, platform_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        
        # Don't create platform too close to player
        if new_platform_rect.colliderect(self.player.rect):
            return False
        
        # Don't create platform overlapping with existing platforms
        for platform in self.platforms:
            if new_platform_rect.colliderect(platform.rect):
                return False
        
        # Create the platform
        new_platform = TemporaryPlatform(platform_x, platform_y)
        self.platforms.append(new_platform)
        return True
    
    def update_platforms(self):
        """Update platforms and remove expired ones."""
        self.platforms = [p for p in self.platforms if not p.is_expired()]
    
    def handle_events(self):
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.create_platform(event.pos)
        
        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        else:
            self.player.stop_horizontal()
        
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.jump()
    
    def draw_ui(self):
        """Draw the user interface."""
        # Platform count
        platform_text = self.font.render(f"Platforms: {len(self.platforms)}/{MAX_PLATFORMS}", True, WHITE)
        self.screen.blit(platform_text, (10, 10))
        
        # Instructions
        instructions = [
            "Click to create platforms",
            "Arrow keys/WASD to move",
            "Space to jump"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(text, (10, 50 + i * 25))
        
        # Platform timer info
        if self.platforms:
            timer_text = self.small_font.render("Platform timers:", True, WHITE)
            self.screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))
            
            for i, platform in enumerate(self.platforms):
                remaining = platform.get_remaining_time()
                timer_info = self.small_font.render(f"Platform {i+1}: {remaining:.1f}s", True, WHITE)
                self.screen.blit(timer_info, (SCREEN_WIDTH - 200, 35 + i * 20))
    
    def draw_ground(self):
        """Draw the ground level."""
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
        pygame.draw.rect(self.screen, GRAY, ground_rect)
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            
            # Update game state
            self.update_platforms()
            self.player.update(self.platforms)
            
            # Draw everything
            self.screen.fill(BLACK)
            self.draw_ground()
            
            # Draw platforms
            for platform in self.platforms:
                platform.draw(self.screen)
            
            # Draw player
            self.player.draw(self.screen)
            
            # Draw UI
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point of the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()