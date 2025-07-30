import pygame
import random
import os

# === Initialization ===
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 900, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("White Background Window")
clock = pygame.time.Clock()

# === Constants ===
PLAYER_SIZE = 40
PLAYER_COLOR = (0, 0, 0)
PLAYER_SPEED = 5

ENEMY_SIZE = 40
ENEMY_COLOR = (255, 0, 0)

BULLET_WIDTH = 8
BULLET_HEIGHT = 4
BULLET_COLOR = (255, 0, 0)
BULLET_SPEED = 7

PLAYER_BULLET_WIDTH = 8
PLAYER_BULLET_HEIGHT = 4
PLAYER_BULLET_COLOR = (0, 0, 255)
PLAYER_BULLET_SPEED = 10

PLAYER2_BULLET_WIDTH = 8
PLAYER2_BULLET_HEIGHT = 4
PLAYER2_BULLET_COLOR = (0, 255, 255)
PLAYER2_BULLET_SPEED = 10

GRAVITY = 1
JUMP_STRENGTH = 15

PLATFORM_COLOR = (128, 128, 128)
PLATFORM_MIN_WIDTH = 80
PLATFORM_MAX_WIDTH = 160
PLATFORM_HEIGHT = 20
PLATFORM_COUNT = 12

KNOCKBACK_DISTANCE = 5
KNOCKBACK_VERTICAL = 12
KNOCKBACK_DURATION = 12

PLAYER_MAX_HEALTH = 100
ENEMY_MAX_HEALTH = 100
PLAYER2_MAX_HEALTH = 100

PLAYER_BULLET_DAMAGE = PLAYER_MAX_HEALTH // 30
ENEMY_BULLET_DAMAGE = PLAYER_MAX_HEALTH // 30
PLAYER2_BULLET_DAMAGE = PLAYER2_MAX_HEALTH // 30

PLAYER2_SIZE = 40
PLAYER2_COLOR = (0, 128, 255)
PLAYER2_SPEED = 5

BLOCK_SIZE = 40

WEAPON_RIFLE = "rifle"
WEAPON_SHOTGUN = "shotgun"

RIFLE_COOLDOWN_FRAMES = 6
SHOTGUN_COOLDOWN_FRAMES = 18
SHOTGUN_MAGAZINE_SIZE = 2
SHOTGUN_BULLETS_PER_SHOT = 12

MAGAZINE_SIZE = 15
RELOAD_FRAMES = 180

DIFFICULTY_LEVELS = {
    "Easy": {"enemy_speed": 2, "bullet_speed": 5, "interval_min": 80, "interval_max": 160},
    "Medium": {"enemy_speed": 4, "bullet_speed": 7, "interval_min": 40, "interval_max": 120},
    "Hard": {"enemy_speed": 6, "bullet_speed": 10, "interval_min": 20, "interval_max": 60},
    "Master": {"enemy_speed": 9, "bullet_speed": 15, "interval_min": 10, "interval_max": 30},
}

# === Game State Variables ===
player_x = WINDOW_WIDTH // 2 - PLAYER_SIZE // 2
player_y = WINDOW_HEIGHT // 2 - PLAYER_SIZE // 2
player_velocity_y = 0
is_jumping = False
player_health = PLAYER_MAX_HEALTH
player_facing_right = True

enemy_x = WINDOW_WIDTH // 4 - ENEMY_SIZE // 2
enemy_y = WINDOW_HEIGHT // 2 - ENEMY_SIZE // 2
enemy_velocity_y = 0
enemy_is_jumping = False
enemy_health = ENEMY_MAX_HEALTH

player2_x = 3 * WINDOW_WIDTH // 4 - PLAYER2_SIZE // 2
player2_y = WINDOW_HEIGHT // 2 - PLAYER2_SIZE // 2
player2_velocity_y = 0
player2_is_jumping = False
player2_health = PLAYER2_MAX_HEALTH
player2_facing_right = True

bullets = []
player_bullets = []
player2_bullets = []

PLATFORMS = []

player_knockback_timer = 0
player_knockback_dx = 0
player_knockback_dy = 0

enemy_knockback_timer = 0
enemy_knockback_dx = 0
enemy_knockback_dy = 0

player2_knockback_timer = 0
player2_knockback_dx = 0
player2_knockback_dy = 0

two_player_mode = False
difficulty = "Medium"

player_exploded = False
enemy_exploded = False
player2_exploded = False

ENEMY_JUMP_STRENGTH = 15
enemy_jump_timer = 0
enemy_jump_interval = 120

bullet_timer = 0
bullet_interval = random.randint(40, 120)

player_magazine = MAGAZINE_SIZE
player_reloading = False
player_reload_timer = 0

player2_magazine = MAGAZINE_SIZE
player2_reloading = False
player2_reload_timer = 0

player_weapon = WEAPON_RIFLE
player2_weapon = WEAPON_RIFLE

player_rifle_cooldown = 0
player2_rifle_cooldown = 0
player_shotgun_cooldown = 0
player2_shotgun_cooldown = 0

font = pygame.font.SysFont(None, 24)

# === Utility Functions ===

def get_health_color(health, max_health):
    """Return the color based on health percentage."""
    percent = health / max_health
    if percent > 0.7:
        return (0, 200, 0)
    elif percent > 0.4:
        return (255, 215, 0)
    elif percent > 0.15:
        return (255, 140, 0)
    else:
        return (200, 0, 0)

def set_player_positions():
    """Set player spawn positions for both modes."""
    global player_x, player_y, player2_x, player2_y
    player_y = WINDOW_HEIGHT // 2 - PLAYER_SIZE // 2
    player2_y = WINDOW_HEIGHT // 2 - PLAYER2_SIZE // 2
    if two_player_mode:
        player_x = WINDOW_WIDTH // 8 - PLAYER_SIZE // 2
        player2_x = 7 * WINDOW_WIDTH // 8 - PLAYER2_SIZE // 2
    else:
        player_x = WINDOW_WIDTH // 2 - PLAYER_SIZE // 2
        player2_x = 3 * WINDOW_WIDTH // 4 - PLAYER2_SIZE // 2

def reset_game():
    """Reset all game variables to their initial state."""
    global player_x, player_y, player_velocity_y, is_jumping, player_health
    global enemy_x, enemy_y, enemy_velocity_y, enemy_is_jumping, enemy_health
    global bullets, player_bullets, bullet_timer, bullet_interval
    global player2_x, player2_y, player2_velocity_y, player2_is_jumping, player2_health, player2_bullets
    global PLATFORMS
    global player_magazine, player_reloading, player_reload_timer
    global player2_magazine, player2_reloading, player2_reload_timer
    global player_weapon, player2_weapon
    global player_rifle_cooldown, player2_rifle_cooldown, player_shotgun_cooldown, player2_shotgun_cooldown
    player_weapon = WEAPON_RIFLE
    player2_weapon = WEAPON_RIFLE
    PLATFORMS = generate_random_platforms()
    set_player_positions()
    player_velocity_y = 0
    is_jumping = False
    player_health = PLAYER_MAX_HEALTH
    enemy_x = WINDOW_WIDTH // 4 - ENEMY_SIZE // 2
    enemy_y = WINDOW_HEIGHT // 2 - ENEMY_SIZE // 2
    enemy_velocity_y = 0
    enemy_is_jumping = False
    enemy_health = ENEMY_MAX_HEALTH
    bullets = []
    player_bullets = []
    bullet_timer = 0
    bullet_interval = random.randint(40, 120)
    player2_velocity_y = 0
    player2_is_jumping = False
    player2_health = PLAYER2_MAX_HEALTH
    player2_bullets = []
    player_magazine = MAGAZINE_SIZE
    player_reloading = False
    player_reload_timer = 0
    player2_magazine = MAGAZINE_SIZE
    player2_reloading = False
    player2_reload_timer = 0
    player_rifle_cooldown = 0
    player2_rifle_cooldown = 0
    player_shotgun_cooldown = 0
    player2_shotgun_cooldown = 0

def draw_button(surface, text, x, y, width, height):
    """Draw a button and return its rect."""
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, (220, 220, 220), button_rect)
    pygame.draw.rect(surface, (0, 0, 0), button_rect, 2)
    font_btn = pygame.font.SysFont(None, 32)
    text_surface = font_btn.render(text, True, (0, 0, 0))
    text_x = x + (width - text_surface.get_width()) // 2
    text_y = y + (height - text_surface.get_height()) // 2
    surface.blit(text_surface, (text_x, text_y))
    return button_rect

def show_start_and_difficulty_menu():
    """Show the start menu and difficulty selection. Returns (two_player_mode, difficulty)."""
    while True:
        screen.fill((255, 255, 255))
        start_button_rect = draw_button(
            screen, "Start", (WINDOW_WIDTH - 160) // 2, WINDOW_HEIGHT // 2 - 60, 160, 40
        )
        two_player_button_rect = draw_button(
            screen, "2 Player", (WINDOW_WIDTH - 160) // 2, WINDOW_HEIGHT // 2 + 10, 160, 40
        )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    while True:
                        screen.fill((255, 255, 255))
                        easy_rect = draw_button(
                            screen, "Easy", (WINDOW_WIDTH - 440) // 2, WINDOW_HEIGHT // 2 - 20, 100, 32
                        )
                        medium_rect = draw_button(
                            screen, "Medium", (WINDOW_WIDTH - 120) // 2, WINDOW_HEIGHT // 2 - 20, 100, 32
                        )
                        hard_rect = draw_button(
                            screen, "Hard", (WINDOW_WIDTH + 200) // 2, WINDOW_HEIGHT // 2 - 20, 100, 32
                        )
                        master_rect = draw_button(
                            screen, "Master", (WINDOW_WIDTH + 520) // 2, WINDOW_HEIGHT // 2 - 20, 100, 32
                        )
                        font_diff = pygame.font.SysFont(None, 20)
                        diff_text = font_diff.render("Select Difficulty", True, (0, 0, 0))
                        screen.blit(
                            diff_text,
                            ((WINDOW_WIDTH - diff_text.get_width()) // 2, WINDOW_HEIGHT // 2 - 60),
                        )
                        pygame.display.flip()
                        for event2 in pygame.event.get():
                            if event2.type == pygame.QUIT:
                                pygame.quit()
                                exit()
                            if event2.type == pygame.MOUSEBUTTONDOWN and event2.button == 1:
                                mouse_pos2 = pygame.mouse.get_pos()
                                if easy_rect.collidepoint(mouse_pos2):
                                    return False, "Easy"
                                if medium_rect.collidepoint(mouse_pos2):
                                    return False, "Medium"
                                if hard_rect.collidepoint(mouse_pos2):
                                    return False, "Hard"
                                if master_rect.collidepoint(mouse_pos2):
                                    return False, "Master"
                if two_player_button_rect.collidepoint(mouse_pos):
                    return True, None

def apply_gravity_and_platforms(x, y, size, velocity_y):
    """
    Apply gravity and handle platform collisions for a square entity.

    Args:
        x (int): The x-coordinate of the entity.
        y (int): The y-coordinate of the entity.
        size (int): The size of the entity.
        velocity_y (int): The vertical velocity.

    Returns:
        tuple: (new_y, new_velocity_y, landed)
    """
    landed = False
    new_y = y + velocity_y
    entity_rect = pygame.Rect(x, new_y, size, size)
    for platform in PLATFORMS:
        if entity_rect.colliderect(platform) and velocity_y >= 0:
            new_y = platform.top - size
            velocity_y = 0
            landed = True
            break
    if new_y + size >= WINDOW_HEIGHT:
        new_y = WINDOW_HEIGHT - size
        velocity_y = 0
        landed = True
    return new_y, velocity_y, landed

def draw_health_bar(surface, x, y, health, max_health):
    """Draw a health bar at the specified position."""
    bar_width = 100
    bar_height = 12
    health_ratio = max(0, health) / max_health
    color = get_health_color(health, max_health)
    pygame.draw.rect(surface, (180, 180, 180), (x, y, bar_width, bar_height))
    pygame.draw.rect(surface, color, (x, y, int(bar_width * health_ratio), bar_height))
    pygame.draw.rect(surface, (0, 0, 0), (x, y, bar_width, bar_height), 2)

def draw_labeled_health_bar(surface, x, y, health, max_health, label):
    """Draw a labeled health bar."""
    draw_health_bar(surface, x, y, health, max_health)
    font_label = pygame.font.SysFont(None, 20)
    text = f"{label}: {health}/{max_health}"
    text_surface = font_label.render(text, True, (0, 0, 0))
    surface.blit(text_surface, (x, y - 18))

def draw_x_above(surface, x, y, size):
    """Draw a red 'X' above the entity to indicate defeat."""
    center_x = x + size // 2
    top_y = y - 18
    font_x = pygame.font.SysFont(None, 32)
    x_surface = font_x.render("X", True, (200, 0, 0))
    surface.blit(x_surface, (center_x - x_surface.get_width() // 2, top_y))

def break_into_pieces(x, y, size, color):
    """Display a simple explosion effect by breaking the entity into pieces."""
    for _ in range(12):
        piece_x = x + random.randint(0, size)
        piece_y = y + random.randint(0, size)
        piece_size = random.randint(4, 10)
        pygame.draw.rect(screen, color, (piece_x, piece_y, piece_size, piece_size))

def show_game_over(winner_title):
    """Display the game over screen and handle restart."""
    font_over = pygame.font.SysFont(None, 48)
    font_btn = pygame.font.SysFont(None, 32)
    while True:
        screen.fill((255, 255, 255))
        over_text = font_over.render(
            f"Game Over! Winner: {winner_title}", True, (0, 0, 0)
        )
        screen.blit(
            over_text,
            ((WINDOW_WIDTH - over_text.get_width()) // 2, WINDOW_HEIGHT // 2 - 80),
        )
        restart_rect = draw_button(
            screen, "Restart", (WINDOW_WIDTH - 160) // 2, WINDOW_HEIGHT // 2, 160, 40
        )
        quit_rect = draw_button(
            screen, "Quit", (WINDOW_WIDTH - 160) // 2, WINDOW_HEIGHT // 2 + 60, 160, 40
        )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse_pos):
                    return True
                if quit_rect.collidepoint(mouse_pos):
                    return False

def generate_random_platforms():
    """
    Generate a list of random platforms for the map, ensuring no overlap and at least 2 blocks vertical separation.

    Returns:
        list: List of pygame.Rect objects representing platforms.
    """
    platforms = []
    attempts = 0
    min_vertical_gap = 2 * BLOCK_SIZE
    max_attempts = PLATFORM_COUNT * 30
    while len(platforms) < PLATFORM_COUNT and attempts < max_attempts:
        width = random.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH)
        x = random.randint(0, WINDOW_WIDTH - width)
        y = random.randint(80, WINDOW_HEIGHT - 120)
        new_platform = pygame.Rect(x, y, width, PLATFORM_HEIGHT)
        if all(
            not new_platform.colliderect(existing)
            and abs(new_platform.top - existing.top) >= min_vertical_gap
            for existing in platforms
        ):
            platforms.append(new_platform)
        attempts += 1
    while len(platforms) < PLATFORM_COUNT:
        width = random.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH)
        x = random.randint(0, WINDOW_WIDTH - width)
        y = WINDOW_HEIGHT - PLATFORM_HEIGHT - 10
        new_platform = pygame.Rect(x, y, width, PLATFORM_HEIGHT)
        if all(
            not new_platform.colliderect(existing)
            and abs(new_platform.top - existing.top) >= min_vertical_gap
            for existing in platforms
        ):
            platforms.append(new_platform)
    return platforms

# === Main Game Loop ===
while True:
    running = True
    game_over = False
    winner_title = ""
    player_exploded = False
    enemy_exploded = False
    player2_exploded = False

    reset_game()
    set_player_positions()

    while running:
        clock.tick(60)
        # --- Reload logic ---
        if player_reloading:
            player_reload_timer += 1
            if player_reload_timer >= RELOAD_FRAMES:
                if player_weapon == WEAPON_SHOTGUN:
                    player_magazine = SHOTGUN_MAGAZINE_SIZE
                else:
                    player_magazine = MAGAZINE_SIZE
                player_reloading = False
                player_reload_timer = 0

        if two_player_mode and player2_reloading:
            player2_reload_timer += 1
            if player2_reload_timer >= RELOAD_FRAMES:
                if player2_weapon == WEAPON_SHOTGUN:
                    player2_magazine = SHOTGUN_MAGAZINE_SIZE
                else:
                    player2_magazine = MAGAZINE_SIZE
                player2_reloading = False
                player2_reload_timer = 0

        # --- Cooldown logic ---
        if player_rifle_cooldown > 0:
            player_rifle_cooldown -= 1
        if player_shotgun_cooldown > 0:
            player_shotgun_cooldown -= 1
        if two_player_mode:
            if player2_rifle_cooldown > 0:
                player2_rifle_cooldown -= 1
            if player2_shotgun_cooldown > 0:
                player2_shotgun_cooldown -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_weapon = WEAPON_RIFLE
                    player_magazine = MAGAZINE_SIZE
                if event.key == pygame.K_2:
                    player_weapon = WEAPON_SHOTGUN
                    player_magazine = SHOTGUN_MAGAZINE_SIZE
                if two_player_mode:
                    if event.key == pygame.K_KP1:
                        player2_weapon = WEAPON_RIFLE
                        player2_magazine = MAGAZINE_SIZE
                    if event.key == pygame.K_KP2:
                        player2_weapon = WEAPON_SHOTGUN
                        player2_magazine = SHOTGUN_MAGAZINE_SIZE
            # Player 1 controls
            if player_health > 0 and (not two_player_mode or player2_health > 0):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not is_jumping:
                        player_velocity_y = -JUMP_STRENGTH
                        is_jumping = True
                    # Player 1 shoot with 'E' in 2 player mode
                    if two_player_mode and event.key == pygame.K_e:
                        if player_weapon == WEAPON_RIFLE:
                            if (
                                not player_reloading
                                and player_magazine > 0
                                and player_rifle_cooldown == 0
                            ):
                                direction = 1 if player_facing_right else -1
                                player_bullets.append(
                                    {
                                        "x": player_x + PLAYER_SIZE // 2,
                                        "y": player_y + PLAYER_SIZE // 2,
                                        "dx": direction * PLAYER_BULLET_SPEED,
                                    }
                                )
                                player_magazine -= 1
                                player_rifle_cooldown = RIFLE_COOLDOWN_FRAMES
                                if player_magazine == 0:
                                    player_reloading = True
                                    player_reload_timer = 0
                        elif player_weapon == WEAPON_SHOTGUN:
                            if (
                                not player_reloading
                                and player_magazine > 0
                                and player_shotgun_cooldown == 0
                            ):
                                direction = 1 if player_facing_right else -1
                                # Shotgun fires 10 bullets in a wide spread
                                for spread in range(-9, 10, 2):
                                    player_bullets.append(
                                        {
                                            "x": player_x + PLAYER_SIZE // 2,
                                            "y": player_y + PLAYER_SIZE // 2 + spread,
                                            "dx": direction * PLAYER_BULLET_SPEED,
                                            "shotgun": True,
                                        }
                                    )
                                player_magazine -= 1
                                player_shotgun_cooldown = SHOTGUN_COOLDOWN_FRAMES
                                if player_magazine == 0:
                                    player_reloading = True
                                    player_reload_timer = 0
                    # Player 2 shoot with Numpad 0 in 2 player mode
                    if two_player_mode and event.key == pygame.K_KP0:
                        if player2_weapon == WEAPON_RIFLE:
                            if (
                                not player2_reloading
                                and player2_magazine > 0
                                and player2_rifle_cooldown == 0
                            ):
                                direction2 = 1 if player2_facing_right else -1
                                player2_bullets.append(
                                    {
                                        "x": player2_x + PLAYER2_SIZE // 2,
                                        "y": player2_y + PLAYER2_SIZE // 2,
                                        "dx": direction2 * PLAYER2_BULLET_SPEED,
                                    }
                                )
                                player2_magazine -= 1
                                player2_rifle_cooldown = RIFLE_COOLDOWN_FRAMES
                                if player2_magazine == 0:
                                    player2_reloading = True
                                    player2_reload_timer = 0
                        elif player2_weapon == WEAPON_SHOTGUN:
                            if (
                                not player2_reloading
                                and player2_magazine > 0
                                and player2_shotgun_cooldown == 0
                            ):
                                direction2 = 1 if player2_facing_right else -1
                                for spread in range(-9, 10, 2):
                                    player2_bullets.append(
                                        {
                                            "x": player2_x + PLAYER2_SIZE // 2,
                                            "y": player2_y + PLAYER2_SIZE // 2 + spread,
                                            "dx": direction2 * PLAYER2_BULLET_SPEED,
                                            "shotgun": True,
                                        }
                                    )
                                player2_magazine -= 1
                                player2_shotgun_cooldown = SHOTGUN_COOLDOWN_FRAMES
                                if player2_magazine == 0:
                                    player2_reloading = True
                                    player2_reload_timer = 0
                # Player 1 shoot with mouse in single player mode only
                if not two_player_mode and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if player_weapon == WEAPON_RIFLE:
                            if (
                                not player_reloading
                                and player_magazine > 0
                                and player_rifle_cooldown == 0
                            ):
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                direction = 1 if mouse_x > player_x else -1
                                player_bullets.append(
                                    {
                                        "x": player_x + PLAYER_SIZE // 2,
                                        "y": player_y + PLAYER_SIZE // 2,
                                        "dx": direction * PLAYER_BULLET_SPEED,
                                    }
                                )
                                player_magazine -= 1
                                player_rifle_cooldown = RIFLE_COOLDOWN_FRAMES
                                if player_magazine == 0:
                                    player_reloading = True
                                    player_reload_timer = 0
                        elif player_weapon == WEAPON_SHOTGUN:
                            if (
                                not player_reloading
                                and player_magazine > 0
                                and player_shotgun_cooldown == 0
                            ):
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                direction = 1 if mouse_x > player_x else -1
                                for spread in range(-9, 10, 2):
                                    player_bullets.append(
                                        {
                                            "x": player_x + PLAYER_SIZE // 2,
                                            "y": player_y + PLAYER_SIZE // 2 + spread,
                                            "dx": direction * PLAYER_BULLET_SPEED,
                                            "shotgun": True,
                                        }
                                    )
                                player_magazine -= 1
                                player_shotgun_cooldown = SHOTGUN_COOLDOWN_FRAMES
                                if player_magazine == 0:
                                    player_reloading = True
                                    player_reload_timer = 0

        # Store previous positions for collision revert
        prev_player_x = player_x
        prev_player_y = player_y
        prev_enemy_x = enemy_x
        prev_enemy_y = enemy_y
        prev_player2_x = player2_x
        prev_player2_y = player2_y

        # --- Knockback and shake logic ---
        # Player knockback
        if player_knockback_timer > 0:
            # Apply horizontal and vertical knockback
            player_x += player_knockback_dx
            player_y += player_knockback_dy
            # Apply gravity to vertical knockback
            player_knockback_dy += GRAVITY
            # Shake effect
            player_x += random.randint(-2, 2)
            player_y += random.randint(-2, 2)
            # Constrain within window
            player_x = max(0, min(player_x, WINDOW_WIDTH - PLAYER_SIZE))
            player_y = max(0, min(player_y, WINDOW_HEIGHT - PLAYER_SIZE))
            player_knockback_timer -= 1

        # Enemy knockback
        if enemy_knockback_timer > 0:
            enemy_x += enemy_knockback_dx
            enemy_y += enemy_knockback_dy
            enemy_knockback_dy += GRAVITY
            enemy_x += random.randint(-2, 2)
            enemy_y += random.randint(-2, 2)
            enemy_x = max(0, min(enemy_x, WINDOW_WIDTH - ENEMY_SIZE))
            enemy_y = max(0, min(enemy_y, WINDOW_HEIGHT - ENEMY_SIZE))
            enemy_knockback_timer -= 1

        # Player 2 knockback
        if player2_knockback_timer > 0:
            player2_x += player2_knockback_dx
            player2_y += player2_knockback_dy
            player2_knockback_dy += GRAVITY
            player2_x += random.randint(-2, 2)
            player2_y += random.randint(-2, 2)
            player2_x = max(0, min(player2_x, WINDOW_WIDTH - PLAYER2_SIZE))
            player2_y = max(0, min(player2_y, WINDOW_HEIGHT - PLAYER2_SIZE))
            player2_knockback_timer -= 1

        # --- Movement only if not in knockback ---
        if player_knockback_timer == 0:
            # Player 1 movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player_y -= PLAYER_SPEED
            if keys[pygame.K_s]:
                player_y += PLAYER_SPEED
            if keys[pygame.K_a]:
                player_x -= PLAYER_SPEED
                player_facing_right = False
            if keys[pygame.K_d]:
                player_x += PLAYER_SPEED
                player_facing_right = True

        if two_player_mode and player2_knockback_timer == 0:
            # 2 Player controls and physics
            # Arrow keys for movement
            if keys[pygame.K_UP] and not player2_is_jumping:
                player2_velocity_y = -JUMP_STRENGTH
                player2_is_jumping = True
            if keys[pygame.K_LEFT]:
                player2_x -= PLAYER2_SPEED
                player2_facing_right = False
            if keys[pygame.K_RIGHT]:
                player2_x += PLAYER2_SPEED
                player2_facing_right = True
            if keys[pygame.K_DOWN]:
                player2_y += PLAYER2_SPEED

            # Gravity and platform collision for player 2
            player2_y, player2_velocity_y, player2_landed = apply_gravity_and_platforms(
                player2_x, player2_y, PLAYER2_SIZE, player2_velocity_y
            )
            if player2_landed:
                player2_is_jumping = False
            else:
                player2_velocity_y += GRAVITY

            player2_x = max(0, min(player2_x, WINDOW_WIDTH - PLAYER2_SIZE))

        # Apply gravity and platform collision to player
        player_y, player_velocity_y, player_landed = apply_gravity_and_platforms(
            player_x, player_y, PLAYER_SIZE, player_velocity_y
        )
        if player_landed:
            is_jumping = False
        else:
            player_velocity_y += GRAVITY

        # Constrain player horizontally
        player_x = max(0, min(player_x, WINDOW_WIDTH - PLAYER_SIZE))

        # Constrain enemy horizontally
        enemy_x = max(0, min(enemy_x, WINDOW_WIDTH - ENEMY_SIZE))

        # Remove collision revert logic so player and NPC/player2 can pass through each other
        # Prevent player and NPC from overlapping in both modes
        # player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
        # enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE)
        # if player_rect.colliderect(enemy_rect):
        #     player_x = prev_player_x
        #     player_y = prev_player_y
        #     enemy_x = prev_enemy_x
        #     enemy_y = prev_enemy_y

        # Prevent player 1 and player 2 from overlapping in two player mode
        # if two_player_mode:
        #     player2_rect = pygame.Rect(player2_x, player2_y, PLAYER2_SIZE, PLAYER2_SIZE)
        #     if player_rect.colliderect(player2_rect):
        #         player_x = prev_player_x
        #         player_y = prev_player_y
        #         player2_x = prev_player2_x
        #         player2_y = prev_player2_y

        # Skip enemy movement, gravity, and shooting in 2 player mode
        if not two_player_mode:
            # Set NPC jump interval based on difficulty (lower interval = more jumps)
            if difficulty == "Easy":
                enemy_jump_interval = 120
            elif difficulty == "Medium":
                enemy_jump_interval = 80
            elif difficulty == "Hard":
                enemy_jump_interval = 40
            elif difficulty == "Master":
                enemy_jump_interval = 20

            # Apply gravity and platform collision to enemy
            enemy_y, enemy_velocity_y, enemy_landed = apply_gravity_and_platforms(
                enemy_x, enemy_y, ENEMY_SIZE, enemy_velocity_y
            )
            if not enemy_landed:
                enemy_velocity_y += GRAVITY

            # NPC random jump logic
            enemy_jump_timer += 1
            if enemy_landed and enemy_jump_timer >= enemy_jump_interval:
                if random.random() < 0.7:  # 70% chance to jump when interval reached
                    enemy_velocity_y = -ENEMY_JUMP_STRENGTH
                enemy_jump_timer = 0

            # Enemy movement (simple horizontal patrol with distance check)
            prev_enemy_x = enemy_x
            prev_enemy_y = enemy_y
            enemy_speed = DIFFICULTY_LEVELS[difficulty]["enemy_speed"]
            distance_x = abs(player_x - enemy_x)
            if distance_x > 8 * BLOCK_SIZE:
                if player_x > enemy_x:
                    enemy_x += enemy_speed
                elif player_x < enemy_x:
                    enemy_x -= enemy_speed
            # If within 8 blocks, NPC does not move horizontally
            enemy_x = max(0, min(enemy_x, WINDOW_WIDTH - ENEMY_SIZE))
            # Prevent NPC and player from overlapping after enemy moves
            player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
            enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE)
            if player_rect.colliderect(enemy_rect):
                enemy_x = prev_enemy_x
                enemy_y = prev_enemy_y

            # Enemy gun shooting logic (disable if either is dead)
            if player_health > 0 and enemy_health > 0:
                bullet_timer += 1
                interval_min = DIFFICULTY_LEVELS[difficulty]["interval_min"]
                interval_max = DIFFICULTY_LEVELS[difficulty]["interval_max"]
                if bullet_timer >= random.randint(interval_min, interval_max):
                    bullet_timer = 0
                    # Shoot bullet towards player
                    direction = 1 if player_x > enemy_x else -1
                    bullets.append(
                        {
                            "x": enemy_x + ENEMY_SIZE // 2,
                            "y": enemy_y + ENEMY_SIZE // 2,
                            "dx": direction
                            * DIFFICULTY_LEVELS[difficulty]["bullet_speed"],
                        }
                    )

        # Update enemy bullet positions
        for bullet in bullets:
            bullet["x"] += bullet["dx"]

        # Remove enemy bullets that go off screen
        bullets = [b for b in bullets if 0 <= b["x"] <= WINDOW_WIDTH]

        # Update player bullet positions
        for bullet in player_bullets:
            bullet["x"] += bullet["dx"]

        # Remove player bullets that go off screen
        player_bullets = [b for b in player_bullets if 0 <= b["x"] <= WINDOW_WIDTH]

        # Update player 2 bullet positions
        for bullet in player2_bullets:
            bullet["x"] += bullet["dx"]

        # Remove player 2 bullets that go off screen
        player2_bullets = [b for b in player2_bullets if 0 <= b["x"] <= WINDOW_WIDTH]

        # --- Bullet collision and knockback trigger ---
        # Check for collisions between enemy bullets and player
        player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
        for bullet in bullets:
            bullet_rect = pygame.Rect(
                bullet["x"], bullet["y"], BULLET_WIDTH, BULLET_HEIGHT
            )
            if bullet_rect.colliderect(player_rect):
                player_health = max(0, player_health - ENEMY_BULLET_DAMAGE)
                player_knockback_dx = (
                    KNOCKBACK_DISTANCE if bullet["dx"] > 0 else -KNOCKBACK_DISTANCE
                )
                player_knockback_dy = -KNOCKBACK_VERTICAL
                player_knockback_timer = KNOCKBACK_DURATION
                bullets.remove(bullet)

        # Check for collisions between player bullets and enemy (single player mode)
        if not two_player_mode:
            enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE)
            for bullet in player_bullets[:]:
                bullet_rect = pygame.Rect(
                    bullet["x"], bullet["y"], PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT
                )
                # Shotgun: only hit if within 5 blocks horizontally
                if bullet_rect.colliderect(enemy_rect):
                    if bullet.get("shotgun"):
                        if abs((bullet["x"] - enemy_x)) <= 5 * BLOCK_SIZE:
                            enemy_health = max(0, enemy_health - PLAYER_BULLET_DAMAGE)
                            enemy_knockback_dx = (
                                KNOCKBACK_DISTANCE
                                if bullet["dx"] > 0
                                else -KNOCKBACK_DISTANCE
                            )
                            enemy_knockback_dy = -KNOCKBACK_VERTICAL
                            enemy_knockback_timer = KNOCKBACK_DURATION
                            player_bullets.remove(bullet)
                        else:
                            continue
                    else:
                        enemy_health = max(0, enemy_health - PLAYER_BULLET_DAMAGE)
                        enemy_knockback_dx = (
                            KNOCKBACK_DISTANCE
                            if bullet["dx"] > 0
                            else -KNOCKBACK_DISTANCE
                        )
                        enemy_knockback_dy = -KNOCKBACK_VERTICAL
                        enemy_knockback_timer = KNOCKBACK_DURATION
                        player_bullets.remove(bullet)

        # Check for collisions between player 2 bullets and enemy (single player mode)
        if not two_player_mode:
            enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE)
            for bullet in player2_bullets[:]:
                bullet_rect = pygame.Rect(
                    bullet["x"],
                    bullet["y"],
                    PLAYER2_BULLET_WIDTH,
                    PLAYER2_BULLET_HEIGHT,
                )
                if bullet_rect.colliderect(enemy_rect):
                    if bullet.get("shotgun"):
                        if abs((bullet["x"] - enemy_x)) <= 5 * BLOCK_SIZE:
                            enemy_health = max(0, enemy_health - PLAYER2_BULLET_DAMAGE)
                            enemy_knockback_dx = (
                                KNOCKBACK_DISTANCE
                                if bullet["dx"] > 0
                                else -KNOCKBACK_DISTANCE
                            )
                            enemy_knockback_dy = -KNOCKBACK_VERTICAL
                            enemy_knockback_timer = KNOCKBACK_DURATION
                            player2_bullets.remove(bullet)
                        else:
                            continue
                    else:
                        enemy_health = max(0, enemy_health - PLAYER2_BULLET_DAMAGE)
                        enemy_knockback_dx = (
                            KNOCKBACK_DISTANCE
                            if bullet["dx"] > 0
                            else -KNOCKBACK_DISTANCE
                        )
                        enemy_knockback_dy = -KNOCKBACK_VERTICAL
                        enemy_knockback_timer = KNOCKBACK_DURATION
                        player2_bullets.remove(bullet)

        # Check for collisions between player bullets and player 2 (2 player mode)
        if two_player_mode:
            player2_rect = pygame.Rect(player2_x, player2_y, PLAYER2_SIZE, PLAYER2_SIZE)
            for bullet in player_bullets[:]:
                bullet_rect = pygame.Rect(
                    bullet["x"], bullet["y"], PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT
                )
                if bullet_rect.colliderect(player2_rect):
                    if bullet.get("shotgun"):
                        if abs((bullet["x"] - player2_x)) <= 5 * BLOCK_SIZE:
                            player2_health = max(
                                0, player2_health - PLAYER_BULLET_DAMAGE
                            )
                            player2_knockback_dx = (
                                KNOCKBACK_DISTANCE
                                if bullet["dx"] > 0
                                else -KNOCKBACK_DISTANCE
                            )
                            player2_knockback_dy = -KNOCKBACK_VERTICAL
                            player2_knockback_timer = KNOCKBACK_DURATION
                            player_bullets.remove(bullet)
                        else:
                            continue
                    else:
                        player2_health = max(0, player2_health - PLAYER_BULLET_DAMAGE)
                        player2_knockback_dx = (
                            KNOCKBACK_DISTANCE
                            if bullet["dx"] > 0
                            else -KNOCKBACK_DISTANCE
                        )
                        player2_knockback_dy = -KNOCKBACK_VERTICAL
                        player2_knockback_timer = KNOCKBACK_DURATION
                        player_bullets.remove(bullet)

        # Check for collisions between player 2 bullets and player 1 (2 player mode)
        if two_player_mode:
            player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
            for bullet in player2_bullets[:]:
                bullet_rect = pygame.Rect(
                    bullet["x"],
                    bullet["y"],
                    PLAYER2_BULLET_WIDTH,
                    PLAYER2_BULLET_HEIGHT,
                )
                if bullet_rect.colliderect(player_rect):
                    if bullet.get("shotgun"):
                        if abs((bullet["x"] - player_x)) <= 5 * BLOCK_SIZE:
                            player_health = max(
                                0, player_health - PLAYER2_BULLET_DAMAGE
                            )
                            player_knockback_dx = (
                                KNOCKBACK_DISTANCE
                                if bullet["dx"] > 0
                                else -KNOCKBACK_DISTANCE
                            )
                            player_knockback_dy = -KNOCKBACK_VERTICAL
                            player_knockback_timer = KNOCKBACK_DURATION
                            player2_bullets.remove(bullet)
                        else:
                            continue
                    else:
                        player_health = max(0, player_health - PLAYER2_BULLET_DAMAGE)
                        player_knockback_dx = (
                            KNOCKBACK_DISTANCE
                            if bullet["dx"] > 0
                            else -KNOCKBACK_DISTANCE
                        )
                        player_knockback_dy = -KNOCKBACK_VERTICAL
                        player_knockback_timer = KNOCKBACK_DURATION
                        player2_bullets.remove(bullet)

        # Fill the background with white
        screen.fill((255, 255, 255))

        # Draw platforms
        for platform in PLATFORMS:
            pygame.draw.rect(screen, PLATFORM_COLOR, platform)

        # Draw the player square (black)
        pygame.draw.rect(
            screen, PLAYER_COLOR, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
        )

        # Draw the enemy square (red) and health bar only if not in 2 player mode
        if not two_player_mode:
            pygame.draw.rect(
                screen, ENEMY_COLOR, (enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE)
            )
            draw_health_bar(
                screen, WINDOW_WIDTH - 110, 10, enemy_health, ENEMY_MAX_HEALTH
            )
            if enemy_health <= 0:
                draw_x_above(screen, enemy_x, enemy_y, ENEMY_SIZE)

        # Draw enemy bullets
        for bullet in bullets:
            pygame.draw.rect(
                screen,
                BULLET_COLOR,
                (bullet["x"], bullet["y"], BULLET_WIDTH, BULLET_HEIGHT),
            )

        # Draw player bullets
        for bullet in player_bullets:
            pygame.draw.rect(
                screen,
                PLAYER_BULLET_COLOR,
                (bullet["x"], bullet["y"], PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT),
            )

        # Draw player 2 bullets
        for bullet in player2_bullets:
            pygame.draw.rect(
                screen,
                PLAYER2_BULLET_COLOR,
                (bullet["x"], bullet["y"], PLAYER2_BULLET_WIDTH, PLAYER2_BULLET_HEIGHT),
            )

        # Draw health bars with dynamic color and labels
        if two_player_mode:
            draw_labeled_health_bar(
                screen, 10, 10, player_health, PLAYER_MAX_HEALTH, "Player 1"
            )
            draw_labeled_health_bar(
                screen,
                WINDOW_WIDTH - 110,
                10,
                player2_health,
                PLAYER2_MAX_HEALTH,
                "Player 2",
            )
        else:
            draw_labeled_health_bar(
                screen, 10, 10, player_health, PLAYER_MAX_HEALTH, "Player"
            )
            draw_labeled_health_bar(
                screen, WINDOW_WIDTH - 110, 10, enemy_health, ENEMY_MAX_HEALTH, "NPC"
            )

        # Draw X above head if dead and break into pieces only once
        if player_health <= 0 and not player_exploded:
            break_into_pieces(player_x, player_y, PLAYER_SIZE, PLAYER_COLOR)
            player_exploded = True
        if not two_player_mode and enemy_health <= 0 and not enemy_exploded:
            break_into_pieces(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_COLOR)
            enemy_exploded = True
        if two_player_mode and player2_health <= 0 and not player2_exploded:
            break_into_pieces(player2_x, player2_y, PLAYER2_SIZE, PLAYER2_COLOR)
            player2_exploded = True

        # Draw X above head if dead
        if player_health <= 0:
            draw_x_above(screen, player_x, player_y, PLAYER_SIZE)
        if not two_player_mode and enemy_health <= 0:
            draw_x_above(screen, enemy_x, enemy_y, ENEMY_SIZE)
        if two_player_mode and player2_health <= 0:
            draw_x_above(screen, player2_x, player2_y, PLAYER2_SIZE)

        # Draw the second player in 2 player mode
        if two_player_mode:
            pygame.draw.rect(
                screen,
                PLAYER2_COLOR,
                (player2_x, player2_y, PLAYER2_SIZE, PLAYER2_SIZE),
            )
            # Remove duplicate health bar for Player 1
            # draw_health_bar(screen, 10, 30, player2_health, PLAYER2_MAX_HEALTH)
            if player2_health <= 0:
                draw_x_above(screen, player2_x, player2_y, PLAYER2_SIZE)

        # Draw reloading message, magazine count, and weapon type
        font_reload = pygame.font.SysFont(None, 28)
        weapon_text = font_reload.render(
            f"Weapon: {'Rifle' if player_weapon == WEAPON_RIFLE else 'Shotgun'}",
            True,
            (0, 0, 0),
        )
        screen.blit(weapon_text, (player_x, player_y - 60))
        if player_reloading:
            reload_text = font_reload.render("Reloading...", True, (200, 0, 0))
            screen.blit(reload_text, (player_x, player_y - 32))
        else:
            mag_text = font_reload.render(f"Ammo: {player_magazine}", True, (0, 0, 0))
            screen.blit(mag_text, (player_x, player_y - 32))

        if two_player_mode:
            weapon_text2 = font_reload.render(
                f"Weapon: {'Rifle' if player2_weapon == WEAPON_RIFLE else 'Shotgun'}",
                True,
                (0, 0, 0),
            )
            screen.blit(weapon_text2, (player2_x, player2_y - 60))
            if player2_reloading:
                reload_text2 = font_reload.render("Reloading...", True, (200, 0, 0))
                screen.blit(reload_text2, (player2_x, player2_y - 32))
            else:
                mag_text2 = font_reload.render(
                    f"Ammo: {player2_magazine}", True, (0, 0, 0)
                )
                screen.blit(mag_text2, (player2_x, player2_y - 32))

        # Check for game over condition and set winner
        if not game_over:
            if player_health <= 0:
                game_over = True
                if two_player_mode:
                    winner_title = "Player 2"
                else:
                    winner_title = "NPC"
            elif not two_player_mode and enemy_health <= 0:
                game_over = True
                winner_title = "Player"
            elif two_player_mode and player2_health <= 0:
                game_over = True
                winner_title = "Player 1"

        # If game over, show game over screen and handle restart
        if game_over:
            restart_clicked = show_game_over(winner_title)
            if restart_clicked:
                # Reset all game state and return to battle directly
                break
            else:
                running = False
                continue

        pygame.display.flip()
    if not running:
        break

pygame.quit()