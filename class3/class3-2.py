import pygame

# Initialize Pygame
pygame.init()

# Set window size
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("White Background Window")

clock = pygame.time.Clock()  # Create a clock to control the frame rate
while True:  # (infinite loop to run the game)
    clock.tick(60)  # Set frame rate to 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Fill background with white
    screen.fill((255, 255, 255))

    pygame.display.flip()
