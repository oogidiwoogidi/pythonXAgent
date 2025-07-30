import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set the window size
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("White Background Window")

# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Define player square properties
PLAYER_SIZE = 40
player_x = WINDOW_WIDTH // 2 - PLAYER_SIZE // 2
player_y = WINDOW_HEIGHT // 2 - PLAYER_SIZE // 2
PLAYER_COLOR = (0, 0, 0)
PLAYER_SPEED = 5

# Define enemy square properties
ENEMY_SIZE = 40
enemy_x = WINDOW_WIDTH // 4 - ENEMY_SIZE // 2
enemy_y = WINDOW_HEIGHT // 2 - ENEMY_SIZE // 2
ENEMY_COLOR = (255, 0, 0)

# Define bullet properties
BULLET_WIDTH = 8
BULLET_HEIGHT = 4
BULLET_COLOR = (255, 0, 0)
BULLET_SPEED = 7
bullets = []
bullet_timer = 0
bullet_interval = random.randint(40, 120)  # Frames between shots

# Define player bullet properties
PLAYER_BULLET_WIDTH = 8
PLAYER_BULLET_HEIGHT = 4
PLAYER_BULLET_COLOR = (0, 0, 255)
PLAYER_BULLET_SPEED = 10
player_bullets = []

# Define player 2 bullet properties
PLAYER2_BULLET_WIDTH = 8
PLAYER2_BULLET_HEIGHT = 4
PLAYER2_BULLET_COLOR = (0, 255, 255)
PLAYER2_BULLET_SPEED = 10
player2_bullets = []

# Gravity and jumping properties
GRAVITY = 1
JUMP_STRENGTH = 15
player_velocity_y = 0
is_jumping = False

# Enemy gravity properties
enemy_velocity_y = 0
enemy_is_jumping = False  # For future extension if needed

# Define platform properties
PLATFORM_COLOR = (128, 128, 128)
PLATFORMS = [
    pygame.Rect(120, 320, 120, 20),
    pygame.Rect(300, 250, 150, 20),
    pygame.Rect(480, 180, 100, 20),
    pygame.Rect(50, 120, 80, 20),
]

# Health properties
PLAYER_MAX_HEALTH = 100
ENEMY_MAX_HEALTH = 100
player_health = PLAYER_MAX_HEALTH
enemy_health = ENEMY_MAX_HEALTH

# Two player mode flag
two_player_mode = False

# Player 2 properties
PLAYER2_SIZE = 40
PLAYER2_COLOR = (0, 128, 255)
PLAYER2_SPEED = 5
PLAYER2_MAX_HEALTH = 100

player2_x = 3 * WINDOW_WIDTH // 4 - PLAYER2_SIZE // 2
player2_y = WINDOW_HEIGHT // 2 - PLAYER2_SIZE // 2
player2_velocity_y = 0
player2_is_jumping = False
player2_health = PLAYER2_MAX_HEALTH
player2_bullets = []

# Add facing direction for both players
player_facing_right = True
player2_facing_right = True

# Difficulty settings for single player mode
DIFFICULTY_LEVELS = {
    "Easy": {
        "enemy_speed": 2,
        "bullet_speed": 5,
        "interval_min": 80,
        "interval_max": 160,
    },
    "Medium": {
        "enemy_speed": 4,
        "bullet_speed": 7,
        "interval_min": 40,
        "interval_max": 120,
    },
    "Hard": {
        "enemy_speed": 6,
        "bullet_speed": 10,
        "interval_min": 20,
        "interval_max": 60,
    },
}
difficulty = "Medium"  # Default

# Add flags to track if explosion has already occurred
player_exploded = False
enemy_exploded = False
player2_exploded = False


def get_health_color(health, max_health):
    """Return the color based on health percentage."""
    percent = health / max_health
    if percent > 0.7:
        return (0, 200, 0)  # Green
    elif percent > 0.4:
        return (255, 215, 0)  # Yellow
    elif percent > 0.15:
        return (255, 140, 0)  # Orange
    else:
        return (200, 0, 0)  # Red


# Set player spawn positions for both modes
def set_player_positions():
    global player_x, player_y, player2_x, player2_y
    player_y = WINDOW_HEIGHT // 2 - PLAYER_SIZE // 2
    player2_y = WINDOW_HEIGHT // 2 - PLAYER2_SIZE // 2
    if two_player_mode:
        player_x = WINDOW_WIDTH // 8 - PLAYER_SIZE // 2  # Left side
        player2_x = 7 * WINDOW_WIDTH // 8 - PLAYER2_SIZE // 2  # Right side
    else:
        player_x = WINDOW_WIDTH // 2 - PLAYER_SIZE // 2
        player2_x = 3 * WINDOW_WIDTH // 4 - PLAYER2_SIZE // 2


def reset_game():
    """Reset all game variables to their initial state."""
    global player_x, player_y, player_velocity_y, is_jumping, player_health
    global enemy_x, enemy_y, enemy_velocity_y, enemy_is_jumping, enemy_health
    global bullets, player_bullets, bullet_timer, bullet_interval
    global player2_x, player2_y, player2_velocity_y, player2_is_jumping, player2_health, player2_bullets

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


# Set up font for displaying coordinates
font = pygame.font.SysFont(None, 24)

# Show start menu with 2 Player button
show_start_menu = True
difficulty_select = False
while show_start_menu:
    screen.fill((255, 255, 255))  # White background
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
                two_player_mode = False
                difficulty_select = True
                show_start_menu = False
            if two_player_button_rect.collidepoint(mouse_pos):
                two_player_mode = True
                set_player_positions()
                show_start_menu = False

# Difficulty selection menu (only for single player)
while difficulty_select:
    screen.fill((255, 255, 255))  # White background
    easy_rect = draw_button(
        screen, "Easy", (WINDOW_WIDTH - 340) // 2, WINDOW_HEIGHT // 2 - 20, 100, 32
    )
    medium_rect = draw_button(
        screen, "Medium", (WINDOW_WIDTH - 100) // 2, WINDOW_HEIGHT // 2 - 20, 100, 32
    )
    hard_rect = draw_button(
        screen, "Hard", (WINDOW_WIDTH + 140) // 2, WINDOW_HEIGHT // 2 - 20, 100, 32
    )
    font_diff = pygame.font.SysFont(None, 20)
    diff_text = font_diff.render(f"Select Difficulty", True, (0, 0, 0))
    screen.blit(
        diff_text,
        ((WINDOW_WIDTH - diff_text.get_width()) // 2, WINDOW_HEIGHT // 2 - 60),
    )
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if easy_rect.collidepoint(mouse_pos):
                difficulty = "Easy"
                set_player_positions()
                difficulty_select = False
            if medium_rect.collidepoint(mouse_pos):
                difficulty = "Medium"
                set_player_positions()
                difficulty_select = False
            if hard_rect.collidepoint(mouse_pos):
                difficulty = "Hard"
                set_player_positions()
                difficulty_select = False


def apply_gravity_and_platforms(x, y, size, velocity_y):
    """Apply gravity and handle collision with platforms, including ceiling collision with blocks."""
    next_y = y + velocity_y
    rect = pygame.Rect(x, next_y, size, size)
    landed = False
    for platform in PLATFORMS:
        platform_rect = pygame.Rect(
            platform.x, platform.y, platform.width, platform.height
        )
        # Landing on top of platform
        if (
            rect.colliderect(platform_rect)
            and velocity_y > 0
            and y + size <= platform.y + 5
        ):
            next_y = platform.y - size
            velocity_y = 0
            landed = True
            break
        # Hitting block from below
        if (
            rect.colliderect(platform_rect)
            and velocity_y < 0
            and y >= platform.y + platform.height - 5
        ):
            next_y = platform.y + platform.height
            velocity_y = 0
            break
    # Ground collision
    if next_y >= WINDOW_HEIGHT - size:
        next_y = WINDOW_HEIGHT - size
        velocity_y = 0
        landed = True
    # Ceiling collision
    if next_y < 0:
        next_y = 0
        velocity_y = 0
    return next_y, velocity_y, landed


def draw_health_bar(surface, x, y, health, max_health, back_color=(200, 200, 200)):
    """Draw a health bar at the given position with dynamic color."""
    bar_width = 100
    bar_height = 12
    pygame.draw.rect(surface, back_color, (x, y, bar_width, bar_height))
    health_width = int(bar_width * (health / max_health))
    bar_color = get_health_color(health, max_health)
    pygame.draw.rect(surface, bar_color, (x, y, health_width, bar_height))
    pygame.draw.rect(surface, (0, 0, 0), (x, y, bar_width, bar_height), 2)


def draw_x_above(surface, x, y, size):
    """Draw an X above the given square."""
    font_x = pygame.font.SysFont(None, size)
    x_surface = font_x.render("X", True, (200, 0, 0))
    surface.blit(x_surface, (x + size // 2 - x_surface.get_width() // 2, y - size // 2))


def draw_labeled_health_bar(
    surface, x, y, health, max_health, label, back_color=(200, 200, 200)
):
    """Draw a labeled health bar at the given position with dynamic color."""
    bar_width = 100
    bar_height = 12
    font_label = pygame.font.SysFont(None, 20)
    label_surface = font_label.render(label, True, (0, 0, 0))
    surface.blit(label_surface, (x, y - 18))
    pygame.draw.rect(surface, back_color, (x, y, bar_width, bar_height))
    health_width = int(bar_width * (health / max_health))
    bar_color = get_health_color(health, max_health)
    pygame.draw.rect(surface, bar_color, (x, y, health_width, bar_height))
    pygame.draw.rect(surface, (0, 0, 0), (x, y, bar_width, bar_height), 2)


def break_into_pieces(x, y, size, color):
    """Animate the character breaking into pieces at (x, y)."""
    pieces = []
    piece_size = size // 8
    for _ in range(16):
        px = x + random.randint(0, size - piece_size)
        py = y + random.randint(0, size - piece_size)
        dx = random.randint(-7, 7)
        dy = random.randint(-7, 7)
        pieces.append(
            {"rect": pygame.Rect(px, py, piece_size, piece_size), "dx": dx, "dy": dy}
        )
    for _ in range(18):  # Number of animation frames
        screen.fill((255, 255, 255))
        # Draw platforms
        for platform in PLATFORMS:
            pygame.draw.rect(screen, PLATFORM_COLOR, platform)
        # Draw all pieces
        for piece in pieces:
            pygame.draw.rect(screen, color, piece["rect"])
            piece["rect"].x += piece["dx"]
            piece["rect"].y += piece["dy"]
        pygame.display.flip()
        pygame.time.delay(35)


def draw_crown(surface, x, y):
    """Draw a simple crown above the given (x, y) position."""
    crown_color = (255, 215, 0)
    crown_width = 40
    crown_height = 20
    base_rect = pygame.Rect(x, y, crown_width, crown_height // 2)
    pygame.draw.rect(surface, crown_color, base_rect)
    # Draw three triangles for crown points
    pygame.draw.polygon(surface, crown_color, [(x, y), (x + 10, y - 20), (x + 20, y)])
    pygame.draw.polygon(
        surface, crown_color, [(x + 10, y), (x + 20, y - 20), (x + 30, y)]
    )
    pygame.draw.polygon(
        surface, crown_color, [(x + 20, y), (x + 30, y - 20), (x + 40, y)]
    )


def show_game_over(winner_title):
    """Display the game over screen with the winner and a crown, and a restart button."""
    screen.fill((255, 255, 255))  # White background
    font_title = pygame.font.SysFont(None, 60)
    font_winner = pygame.font.SysFont(None, 48)
    game_over_text = font_title.render("Game Over", True, (0, 0, 0))
    winner_text = font_winner.render(winner_title, True, (0, 0, 0))
    # Center texts
    game_over_x = (WINDOW_WIDTH - game_over_text.get_width()) // 2
    winner_x = (WINDOW_WIDTH - winner_text.get_width()) // 2
    winner_y = WINDOW_HEIGHT // 2
    screen.blit(game_over_text, (game_over_x, WINDOW_HEIGHT // 2 - 100))
    screen.blit(winner_text, (winner_x, winner_y))
    # Draw crown above winner name
    draw_crown(screen, winner_x + winner_text.get_width() // 2 - 20, winner_y - 40)
    # Draw restart button
    restart_rect = draw_button(
        screen, "Restart", (WINDOW_WIDTH - 160) // 2, WINDOW_HEIGHT // 2 + 80, 160, 40
    )
    pygame.display.flip()
    waiting = True
    restart_clicked = False
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_rect.collidepoint(mouse_pos):
                        restart_clicked = True
                        waiting = False
                elif event.type == pygame.KEYDOWN:
                    waiting = False
    return restart_clicked


# Main loop to run the game
while True:
    # Main game loop
    running = True
    game_over = False
    winner_title = ""
    # Reset explosion flags
    player_exploded = False
    enemy_exploded = False
    player2_exploded = False

    # Show start menu with 2 Player button
    show_start_menu = True
    difficulty_select = False
    while show_start_menu:
        screen.fill((255, 255, 255))  # White background
        start_button_rect = draw_button(
            screen, "Start", (WINDOW_WIDTH - 160) // 2, WINDOW_HEIGHT // 2 - 60, 160, 40
        )
        two_player_button_rect = draw_button(
            screen,
            "2 Player",
            (WINDOW_WIDTH - 160) // 2,
            WINDOW_HEIGHT // 2 + 10,
            160,
            40,
        )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    two_player_mode = False
                    difficulty_select = True
                    show_start_menu = False
                if two_player_button_rect.collidepoint(mouse_pos):
                    two_player_mode = True
                    set_player_positions()
                    show_start_menu = False

    # Difficulty selection menu (only for single player)
    while difficulty_select:
        screen.fill((255, 255, 255))  # White background
        easy_rect = draw_button(
            screen, "Easy", (WINDOW_WIDTH - 340) // 2, WINDOW_HEIGHT // 2 - 20, 100, 32
        )
        medium_rect = draw_button(
            screen,
            "Medium",
            (WINDOW_WIDTH - 100) // 2,
            WINDOW_HEIGHT // 2 - 20,
            100,
            32,
        )
        hard_rect = draw_button(
            screen, "Hard", (WINDOW_WIDTH + 140) // 2, WINDOW_HEIGHT // 2 - 20, 100, 32
        )
        font_diff = pygame.font.SysFont(None, 20)
        diff_text = font_diff.render(f"Select Difficulty", True, (0, 0, 0))
        screen.blit(
            diff_text,
            ((WINDOW_WIDTH - diff_text.get_width()) // 2, WINDOW_HEIGHT // 2 - 60),
        )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if easy_rect.collidepoint(mouse_pos):
                    difficulty = "Easy"
                    set_player_positions()
                    difficulty_select = False
                if medium_rect.collidepoint(mouse_pos):
                    difficulty = "Medium"
                    set_player_positions()
                    difficulty_select = False
                if hard_rect.collidepoint(mouse_pos):
                    difficulty = "Hard"
                    set_player_positions()
                    difficulty_select = False

    while running:
        clock.tick(60)  # Limit the frame rate to 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Player 1 controls
            if player_health > 0 and (not two_player_mode or player2_health > 0):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not is_jumping:
                        player_velocity_y = -JUMP_STRENGTH
                        is_jumping = True
                    # Player 1 shoot with 'E' in 2 player mode
                    if two_player_mode and event.key == pygame.K_e:
                        direction = 1 if player_facing_right else -1
                        player_bullets.append(
                            {
                                "x": player_x + PLAYER_SIZE // 2,
                                "y": player_y + PLAYER_SIZE // 2,
                                "dx": direction * PLAYER_BULLET_SPEED,
                            }
                        )
                    # Player 2 shoot with Numpad 0 in 2 player mode
                    if two_player_mode and event.key == pygame.K_KP0:
                        direction2 = 1 if player2_facing_right else -1
                        player2_bullets.append(
                            {
                                "x": player2_x + PLAYER2_SIZE // 2,
                                "y": player2_y + PLAYER2_SIZE // 2,
                                "dx": direction2 * PLAYER2_BULLET_SPEED,
                            }
                        )
                # Player 1 shoot with mouse in single player mode only
                if not two_player_mode and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        direction = 1 if mouse_x > player_x else -1
                        player_bullets.append(
                            {
                                "x": player_x + PLAYER_SIZE // 2,
                                "y": player_y + PLAYER_SIZE // 2,
                                "dx": direction * PLAYER_BULLET_SPEED,
                            }
                        )

        # Player 1 movement
        keys = pygame.key.get_pressed()
        prev_player_x = player_x
        prev_player_y = player_y
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

        # Prevent player and NPC from overlapping in single player mode
        if not two_player_mode:
            player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
            enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE)
            if player_rect.colliderect(enemy_rect):
                # Revert player movement if collision detected
                player_x = prev_player_x
                player_y = prev_player_y

        # 2 Player controls and physics
        if two_player_mode:
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

        # Skip enemy movement, gravity, and shooting in 2 player mode
        if not two_player_mode:
            # Apply gravity and platform collision to enemy
            enemy_y, enemy_velocity_y, enemy_landed = apply_gravity_and_platforms(
                enemy_x, enemy_y, ENEMY_SIZE, enemy_velocity_y
            )
            if not enemy_landed:
                enemy_velocity_y += GRAVITY

            # Constrain enemy horizontally
            enemy_x = max(0, min(enemy_x, WINDOW_WIDTH - ENEMY_SIZE))

            # Enemy movement (simple horizontal patrol)
            prev_enemy_x = enemy_x
            prev_enemy_y = enemy_y
            enemy_speed = DIFFICULTY_LEVELS[difficulty]["enemy_speed"]
            if player_x > enemy_x:
                enemy_x += enemy_speed
            elif player_x < enemy_x:
                enemy_x -= enemy_speed
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

        # Check for collisions between enemy bullets and player
        player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
        for bullet in bullets:
            bullet_rect = pygame.Rect(
                bullet["x"], bullet["y"], BULLET_WIDTH, BULLET_HEIGHT
            )
            if bullet_rect.colliderect(player_rect):
                player_health = max(0, player_health - 10)
                bullets.remove(bullet)

        # Check for collisions between player bullets and enemy
        if not two_player_mode:
            enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE)
            for bullet in player_bullets:
                bullet_rect = pygame.Rect(
                    bullet["x"], bullet["y"], PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT
                )
                if bullet_rect.colliderect(enemy_rect):
                    enemy_health = max(0, enemy_health - 10)
                    player_bullets.remove(bullet)

        # Check for collisions between player 2 bullets and enemy
        if not two_player_mode:
            enemy_rect = pygame.Rect(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE)
            for bullet in player2_bullets:
                bullet_rect = pygame.Rect(
                    bullet["x"],
                    bullet["y"],
                    PLAYER2_BULLET_WIDTH,
                    PLAYER2_BULLET_HEIGHT,
                )
                if bullet_rect.colliderect(enemy_rect):
                    enemy_health = max(0, enemy_health - 10)
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
                # Reset all game state and return to start menu
                break
            else:
                running = False
                continue

        pygame.display.flip()

    if not running:
        break

pygame.quit()
