# OSA - Temporary Platform Creator

A simple 2D platformer game where players can create temporary platforms to overcome impassable areas and solve environmental puzzles.

## Features

- **Temporary Platform Creation**: Click anywhere to create platforms that help you navigate the world
- **Platform Timer System**: Platforms automatically disappear after 5 seconds with visual countdown
- **Platform Limit Management**: Maximum of 3 active platforms at any time
- **Physics-Based Movement**: Player character with gravity, jumping, and collision detection

## Requirements

- Python 3.6+
- pygame 2.5.2

## Installation

1. Clone the repository
2. Run the setup script:
   ```bash
   python setup.py
   ```

## How to Play

1. Start the game:
   ```bash
   python main.py
   ```

2. **Controls**:
   - **Movement**: Arrow keys or WASD
   - **Jump**: Spacebar, Up arrow, or W key
   - **Create Platform**: Left mouse click

3. **Gameplay**:
   - Click anywhere on the screen to create a temporary platform
   - Use platforms to reach higher areas or cross gaps
   - Platforms turn from green to yellow to red as they expire
   - You can have a maximum of 3 platforms active at once
   - Platforms last for 5 seconds before disappearing

## Testing

Run the test suite to verify all features work correctly:

```bash
python test_main.py
```

## Acceptance Criteria

✅ **The player can create a temporary platform at a valid location**
- Click anywhere on screen to create platforms
- Platforms won't overlap with player or existing platforms
- Platforms are automatically positioned within screen bounds

✅ **The platform disappears after a certain amount of time**
- Each platform lasts exactly 5 seconds
- Visual timer shows remaining time with color changes
- Expired platforms are automatically removed

✅ **The player cannot create more than a certain number of platforms at once**
- Maximum of 3 active platforms enforced
- Attempt to create more platforms will fail
- UI shows current platform count

## Architecture

The game is built with a modular design:

- `TemporaryPlatform`: Handles platform creation, timing, and expiration
- `Player`: Manages player movement, physics, and collision detection  
- `Game`: Main game loop, event handling, and platform management
- Comprehensive test suite validates all acceptance criteria