import pygame

# Initialize Pygame
pygame.init()

# Set the window size
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("White Background Window")

# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Main loop to run the game
running = True
while running:
    clock.tick(60)  # Limit the frame rate to 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    pygame.display.flip()

pygame.quit()
