import pygame
import math

# Initialize Pygame
pygame.init()

# ==================== GAME CONSTANTS ====================

# Window Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Game Object Parameters
BALL_RADIUS = 10
BALL_SPEED = 5
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
BRICK_ROWS = 6
BRICK_COLS = 10

# Color Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)

# Brick Colors
BRICK_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

# ==================== GAME OBJECTS ====================


class Brick:
    """Represents a brick in the game"""

    def __init__(self, x, y, color):
        """Initialize brick object"""
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color
        self.is_hit = False

    def draw(self, screen):
        """Draw the brick on canvas with border"""
        if not self.is_hit:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)  # Border

    def check_collision(self, ball):
        """Check if the ball collides with the brick"""
        if not self.is_hit and self.rect.colliderect(ball.rect):
            return True
        return False

    def destroy(self):
        """Handle brick destruction when hit"""
        self.is_hit = True


class Paddle:
    """Represents the player's paddle"""

    def __init__(self, x, y):
        """Initialize paddle object"""
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = WHITE

    def draw(self, screen):
        """Draw the paddle on canvas with border"""
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Border

    def move(self, mouse_x):
        """Update paddle position based on mouse X coordinate, centering paddle to mouse position"""
        self.rect.centerx = mouse_x
        # Keep paddle within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH


class Ball:
    """Represents the ball in the game"""

    def __init__(self, x, y):
        """Initialize ball object"""
        self.rect = pygame.Rect(
            x - BALL_RADIUS, y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2
        )
        self.speed_x = BALL_SPEED
        self.speed_y = BALL_SPEED
        self.color = WHITE

    def draw(self, screen):
        """Draw the ball on canvas"""
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)
        pygame.draw.circle(screen, BLACK, self.rect.center, BALL_RADIUS, 2)  # Border

    def move(self):
        """Update ball position"""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def bounce_x(self):
        """Reverse horizontal direction"""
        self.speed_x = -self.speed_x

    def bounce_y(self):
        """Reverse vertical direction"""
        self.speed_y = -self.speed_y

    def check_wall_collision(self):
        """Check collision with walls and bounce accordingly"""
        # Left and right walls
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.bounce_x()

        # Top wall
        if self.rect.top <= 0:
            self.bounce_y()

        # Bottom wall (game over condition)
        return self.rect.bottom >= WINDOW_HEIGHT

    def check_paddle_collision(self, paddle):
        """Check collision with paddle and bounce accordingly"""
        if self.rect.colliderect(paddle.rect) and self.speed_y > 0:
            self.bounce_y()
            # Add some angle based on where the ball hits the paddle
            hit_pos = (self.rect.centerx - paddle.rect.centerx) / (PADDLE_WIDTH / 2)
            self.speed_x = BALL_SPEED * hit_pos


# ==================== GAME INITIALIZATION ====================


def create_bricks():
    """Create the grid of bricks"""
    bricks = []
    brick_start_x = (WINDOW_WIDTH - (BRICK_COLS * BRICK_WIDTH)) // 2
    brick_start_y = 50

    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = brick_start_x + col * BRICK_WIDTH
            y = brick_start_y + row * BRICK_HEIGHT
            color = BRICK_COLORS[row % len(BRICK_COLORS)]
            brick = Brick(x, y, color)
            bricks.append(brick)

    return bricks


# ==================== MAIN GAME LOOP ====================


def main():
    """Main game function"""
    # Set up the display
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Brick Breaker Game")
    clock = pygame.time.Clock()

    # Create game objects
    paddle = Paddle(WINDOW_WIDTH // 2 - PADDLE_WIDTH // 2, WINDOW_HEIGHT - 50)
    ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    bricks = create_bricks()

    # Game state variables
    running = True
    game_over = False
    game_won = False

    # Main game loop
    while running:
        clock.tick(FPS)

        # ==================== EVENT HANDLING ====================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                # Handle mouse movement to control paddle
                mouse_x = event.pos[0]
                paddle.move(mouse_x)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (game_over or game_won):
                    # Restart game
                    paddle = Paddle(
                        WINDOW_WIDTH // 2 - PADDLE_WIDTH // 2, WINDOW_HEIGHT - 50
                    )
                    ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
                    bricks = create_bricks()
                    game_over = False
                    game_won = False

        # ==================== GAME LOGIC ====================
        if not game_over and not game_won:
            # Move ball
            ball.move()

            # Check wall collisions
            if ball.check_wall_collision():
                game_over = True

            # Check paddle collision
            ball.check_paddle_collision(paddle)

            # Check brick collisions
            for brick in bricks:
                if brick.check_collision(ball):
                    brick.destroy()
                    ball.bounce_y()
                    break

            # Check win condition
            if all(brick.is_hit for brick in bricks):
                game_won = True

        # ==================== SCREEN RENDERING ====================
        # Clear screen background
        screen.fill(BLACK)

        # Draw game objects
        if not game_over and not game_won:
            # Draw bricks
            for brick in bricks:
                brick.draw(screen)

            # Draw paddle
            paddle.draw(screen)

            # Draw ball
            ball.draw(screen)

        # Draw game status messages
        font = pygame.font.Font(None, 74)
        if game_over:
            text = font.render("GAME OVER", True, RED)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(text, text_rect)

            restart_text = pygame.font.Font(None, 36).render(
                "Press R to Restart", True, WHITE
            )
            restart_rect = restart_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
            )
            screen.blit(restart_text, restart_rect)

        elif game_won:
            text = font.render("YOU WIN!", True, GREEN)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(text, text_rect)

            restart_text = pygame.font.Font(None, 36).render(
                "Press R to Restart", True, WHITE
            )
            restart_rect = restart_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
            )
            screen.blit(restart_text, restart_rect)

        # Update screen display
        pygame.display.flip()

    pygame.quit()


# ==================== PROGRAM ENTRY POINT ====================

if __name__ == "__main__":
    main()
