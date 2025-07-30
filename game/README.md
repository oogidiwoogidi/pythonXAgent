# Game Collection

A collection of games built with Pygame including a 2D platform shooter and Flappy Bird clone.

## Games Included

### 2D Platform Shooter

A multiplayer 2D platform shooter game featuring weapon systems, gravity physics, and multiple difficulty levels.

### Flappy Bird

A classic Flappy Bird clone with simple controls and addictive gameplay.

## Features

- **Single Player Mode**: Fight against AI enemy with configurable difficulty
- **Two Player Mode**: Local multiplayer combat
- **Weapon System**: Switch between rifle and shotgun with different mechanics
- **Physics Engine**: Gravity, jumping, and platform collision detection
- **Dynamic Platforms**: Randomly generated platform layouts
- **Health System**: Visual health bars with color-coded status
- **Knockback Effects**: Visual feedback for damage and impacts

## Game Controls

### Flappy Bird

- **Spacebar**: Flap wings to fly upward
- **R**: Restart game (when game over)

### 2D Platform Shooter

#### Single Player Mode

- **WASD**: Move player
- **Space**: Jump
- **Mouse Click**: Shoot (direction based on mouse position)
- **1/2**: Switch weapons (Rifle/Shotgun)

#### Two Player Mode

- **Player 1**:

  - **WASD**: Move
  - **Space**: Jump
  - **E**: Shoot
  - **1/2**: Switch weapons

- **Player 2**:
  - **Arrow Keys**: Move
  - **Up Arrow**: Jump
  - **Numpad 0**: Shoot
  - **Numpad 1/2**: Switch weapons

#### General (2D Platform Shooter)

- **R**: Restart game
- **ESC**: Exit/Cancel

## Quick Start

### Option 1: Game Launcher (Recommended)

Run the launcher to choose which game to play:

```bash
python launcher.py
```

### Option 2: Run Individual Games

Run the 2D Platform Shooter:

```bash
python main.py
```

Run Flappy Bird:

```bash
python flappy_bird.py
```

## Installation

1. Ensure Python 3.7+ is installed
2. Install required dependencies:
   ```bash
   pip install pygame
   ```
3. Run the game launcher:
   ```bash
   python launcher.py
   ```
   Or run individual games:
   ```bash
   python main.py          # 2D Platform Shooter
   python flappy_bird.py   # Flappy Bird
   ```

## Game Structure

```
game/
├── launcher.py          # Game launcher (choose which game to play)
├── main.py              # 2D Platform Shooter entry point
├── flappy_bird.py       # Flappy Bird game
├── src/
│   ├── config.py        # Game configuration constants
│   ├── entities.py      # Player, Enemy, and Bullet classes
│   ├── game_engine.py   # Main game loop and logic
│   ├── menus.py         # Menu system and UI
│   └── utils.py         # Utility functions
├── assets/              # Game assets (empty for now)
├── docs/                # Documentation
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Difficulty Levels

- **Easy**: Slow enemies, easy shooting patterns
- **Medium**: Balanced gameplay (default)
- **Hard**: Fast enemies, challenging combat
- **Master**: Expert level difficulty

## Weapons

### Rifle

- Fast firing rate
- Single projectile per shot
- 15 round magazine
- Good for precise targeting

### Shotgun

- Slow firing rate
- Multiple projectiles per shot (spread pattern)
- 2 round magazine
- Effective at close range (5 block radius)

## Development

The game is modular and extensible. Key components:

- **Config**: Centralized configuration management
- **Entities**: Object-oriented entity system
- **Game Engine**: Main game loop and state management
- **Menus**: User interface and menu system
- **Utils**: Reusable utility functions

## Future Enhancements

- Sound effects and background music
- Animated sprites and visual effects
- Additional weapon types
- Power-ups and collectibles
- Network multiplayer support
- Level editor and custom maps
