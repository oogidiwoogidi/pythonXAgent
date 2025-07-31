"""
Game Configuration Constants

This module contains all the configuration constants used throughout the game.
Centralizing constants makes the game easier to maintain and modify.
"""

# === Window Configuration ===
WINDOW_WIDTH = 700  # Set to requested size
WINDOW_HEIGHT = 500  # Set to requested size
WINDOW_TITLE = "2D Platform Shooter"
FPS = 60
FULLSCREEN_ENABLED = False  # Default to windowed mode

# === Player Configuration ===
PLAYER_SIZE = 40
PLAYER_COLOR = (0, 0, 0)  # Black
PLAYER_SPEED = 5
PLAYER_MAX_HEALTH = 100

# === Player 2 Configuration ===
PLAYER2_SIZE = 40
PLAYER2_COLOR = (0, 128, 255)  # Blue
PLAYER2_SPEED = 5
PLAYER2_MAX_HEALTH = 100

# === Enemy Configuration ===
ENEMY_SIZE = 40
ENEMY_COLOR = (255, 0, 0)  # Red
ENEMY_MAX_HEALTH = 100
ENEMY_JUMP_STRENGTH = 15

# === Bullet Configuration ===
BULLET_WIDTH = 8
BULLET_HEIGHT = 4
BULLET_COLOR = (255, 0, 0)  # Red
BULLET_SPEED = 7

PLAYER_BULLET_WIDTH = 8
PLAYER_BULLET_HEIGHT = 4
PLAYER_BULLET_COLOR = (0, 0, 255)  # Blue
PLAYER_BULLET_SPEED = 10

PLAYER2_BULLET_WIDTH = 8
PLAYER2_BULLET_HEIGHT = 4
PLAYER2_BULLET_COLOR = (0, 255, 255)  # Cyan
PLAYER2_BULLET_SPEED = 10

# === Physics Configuration ===
GRAVITY = 1
JUMP_STRENGTH = 15

# === Platform Configuration ===
PLATFORM_COLOR = (128, 128, 128)  # Grey
PLATFORM_MIN_WIDTH = 80
PLATFORM_MAX_WIDTH = 160
PLATFORM_HEIGHT = 20
PLATFORM_COUNT = 12
BLOCK_SIZE = 40

# === Combat Configuration ===
KNOCKBACK_DISTANCE = 5
KNOCKBACK_VERTICAL = 12
KNOCKBACK_DURATION = 12

PLAYER_BULLET_DAMAGE = PLAYER_MAX_HEALTH // 30
ENEMY_BULLET_DAMAGE = PLAYER_MAX_HEALTH // 30
PLAYER2_BULLET_DAMAGE = PLAYER2_MAX_HEALTH // 30

# === Weapon Configuration ===
WEAPON_RIFLE = "rifle"
RIFLE_COOLDOWN_FRAMES = 6
MAGAZINE_SIZE = 15
RELOAD_FRAMES = 180

# === Difficulty Configuration ===
DIFFICULTY_LEVELS = {
    "Easy": {
        "enemy_speed": 2,
        "bullet_speed": 5,
        "interval_min": 80,
        "interval_max": 160,
        "enemy_jump_interval": 120,
    },
    "Medium": {
        "enemy_speed": 4,
        "bullet_speed": 7,
        "interval_min": 40,
        "interval_max": 120,
        "enemy_jump_interval": 80,
    },
    "Hard": {
        "enemy_speed": 6,
        "bullet_speed": 10,
        "interval_min": 20,
        "interval_max": 60,
        "enemy_jump_interval": 40,
    },
    "Master": {
        "enemy_speed": 9,
        "bullet_speed": 15,
        "interval_min": 10,
        "interval_max": 30,
        "enemy_jump_interval": 20,
    },
}

# === UI Configuration ===
UI_FONT_SIZE = 24
UI_BUTTON_FONT_SIZE = 32
UI_LABEL_FONT_SIZE = 20
UI_RELOAD_FONT_SIZE = 28

# === Colors ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (180, 180, 180)
ORANGE = (255, 140, 0)
GOLD = (255, 215, 0)
DARK_RED = (200, 0, 0)
LIGHT_GREEN = (0, 200, 0)

# === Sound Effects ===
# Gunshot sounds removed
