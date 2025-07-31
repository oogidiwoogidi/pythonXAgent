# Game Collection - AI Coding Instructions

## Project Architecture

This is a modular Pygame game collection featuring two games: a 2D platform shooter and Flappy Bird. The project uses a centralized configuration system and entity-based architecture.

### Core Components

- **Main Entry Points**: `main.py` (platform shooter), `flappy_bird.py` (standalone), `launcher.py` (game selector)
- **Game Engine**: `src/game_engine.py` - main game loop, collision detection, rendering pipeline
- **Entity System**: `src/entities.py` - Player, Enemy, Bullet classes with physics and AI
- **Configuration**: `src/config.py` - centralized constants for all gameplay parameters
- **UI Framework**: `src/menus.py` + `src/utils.py` - modal menus and rendering utilities

### Critical Architecture Patterns

#### Configuration System (`src/config.py`)

All game constants are centralized in `config.py`. When modifying gameplay:

- Update `DIFFICULTY_LEVELS` dict for AI behavior (enemy_speed, bullet_speed, intervals)
- Modify weapon configs (`RIFLE_COOLDOWN_FRAMES`, `SHOTGUN_MAGAZINE_SIZE`, etc.)
- Adjust physics constants (`GRAVITY`, `JUMP_STRENGTH`, `KNOCKBACK_DISTANCE`)

#### Entity System (`src/entities.py`)

All entities inherit from `Entity` base class with `x, y, size, color, velocity_y`. Key patterns:

- Player weapon switching uses `switch_weapon(key)` with pygame key constants
- Knockback system overrides normal movement for `knockback_timer` frames
- Collision detection relies on `update_rect()` to sync pygame.Rect with x/y positions

#### Game Engine Flow (`src/game_engine.py`)

1. Menu → Game Mode Selection → Difficulty (if single player)
2. Entity initialization with platform generation
3. Main game loop: events → entity updates → collision detection → rendering
4. Game over detection → menu restart cycle

## Development Workflows

### Running Games

```bash
python launcher.py      # Recommended: Interactive game selector
python main.py          # Direct: 2D platform shooter
python flappy_bird.py   # Direct: Flappy Bird
```

### Dependency Management

```bash
pip install pygame>=2.0.0  # Only runtime dependency required
```

### Adding New Weapons

1. Add constants to `config.py`: `WEAPON_NAME`, `WEAPON_NAME_COOLDOWN_FRAMES`, `WEAPON_NAME_DAMAGE`
2. Extend `Player.shoot()` in `entities.py` with new weapon case
3. Update `Player.switch_weapon()` to handle new weapon key binding
4. Modify collision detection in `GameEngine._handle_collisions()` for weapon-specific behavior

### Modifying AI Behavior

Edit `DIFFICULTY_LEVELS` in `config.py`:

- `enemy_speed`: Movement speed toward player
- `bullet_speed`: Projectile velocity
- `interval_min/max`: Enemy shooting frequency range
- `enemy_jump_interval`: AI jumping behavior timing

### Import Patterns

- Main game files use `sys.path.append(os.path.join(os.path.dirname(__file__), "src"))` to import from `src/`
- All `src/` modules import from `config` for constants: `from config import *`
- Utility functions imported explicitly: `from utils import draw_health_bar, generate_random_platforms`

### Collision System

- Uses pygame.Rect for all collision detection in `GameEngine._handle_collisions()`
- Shotgun weapons have range-based damage (5 block radius check): `abs(bullet.x - target.x) <= 5 * BLOCK_SIZE`
- Knockback applies temporary movement override with visual shake effects for `KNOCKBACK_DURATION` frames

### UI Rendering Order

1. Clear screen (WHITE background)
2. Draw platforms (PLATFORM_COLOR)
3. Draw entities (players, enemies, bullets)
4. Draw death effects (X marks, explosion pieces)
5. Draw UI overlays (health bars, weapon info)

### Platform Generation (`utils.generate_random_platforms()`)

- Ensures minimum 2-block vertical separation between platforms
- Handles overlap detection with fallback generation
- Uses attempt limiting (`max_attempts = PLATFORM_COUNT * 30`) to prevent infinite loops

## Integration Points

### Launcher Integration

- Uses `subprocess.run([sys.executable, game_path])` to execute individual games
- Restarts launcher after game completion with recursive `main()` call
- Handles Python path resolution for cross-platform compatibility

### Menu System (`src/menus.py`)

- Modal menu pattern: blocking loops until user selection
- Mouse-based UI with button collision detection using `pygame.Rect.collidepoint()`
- State flow: Start → Difficulty (single player) → Game → Game Over → Restart cycle

### Physics Integration

- Gravity applied uniformly to all entities with `velocity_y += GRAVITY`
- Platform collision uses temporary rectangle projection: `temp_rect = pygame.Rect(self.x, new_y, self.size, self.size)`
- Knockback overrides normal movement for fixed duration frames with shake effects

### Control Schemes

**Single Player (mouse aiming)**: WASD movement, Space jump, Mouse click shoot, 1/2 weapon switch
**Two Player**: Player 1 (WASD + Space + E), Player 2 (Arrow keys + Up + Numpad 0)
**AI Enemy**: Configurable via difficulty levels, automatic shooting and movement

When extending this codebase, maintain the centralized config pattern, entity-based collision system, and modular menu architecture.
