import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Bird properties
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
BIRD_X = 60
GRAVITY = 0.5
FLAP_STRENGTH = -8

# Pipe properties
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 3

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)


class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = int(self.y)

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(
            self.x,
            self.height + PIPE_GAP,
            PIPE_WIDTH,
            SCREEN_HEIGHT - self.height - PIPE_GAP,
        )

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.top_rect)
        pygame.draw.rect(surface, GREEN, self.bottom_rect)

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0


def draw_text(surface, text, x, y):
    img = font.render(text, True, BLACK)
    surface.blit(img, (x, y))


def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + 100)]
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                if event.key == pygame.K_r and game_over:
                    main()

        if not game_over:
            bird.update()
            if pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe(SCREEN_WIDTH))

            for pipe in pipes:
                pipe.update()
                if pipe.off_screen():
                    pipes.remove(pipe)
                if pipe.x + PIPE_WIDTH < bird.x and not hasattr(pipe, "scored"):
                    score += 1
                    pipe.scored = True

            # Collision detection
            for pipe in pipes:
                if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(
                    pipe.bottom_rect
                ):
                    game_over = True

            if bird.y < 0 or bird.y + BIRD_HEIGHT > SCREEN_HEIGHT:
                game_over = True

        # Draw everything
        screen.fill(WHITE)
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)
        draw_text(screen, f"Score: {score}", 10, 10)
        if game_over:
            draw_text(
                screen, "Game Over! Press R to Restart", 20, SCREEN_HEIGHT // 2 - 40
            )
        pygame.display.flip()


if __name__ == "__main__":
    main()
