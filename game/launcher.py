#!/usr/bin/env python3
"""
Game Launcher

A simple launcher to select and run different games.
"""

import pygame
import sys
import os
import subprocess

# Initialize Pygame for the launcher
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
LIGHT_BLUE = (100, 150, 250)
GRAY = (128, 128, 128)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Launcher")

clock = pygame.time.Clock()
font_title = pygame.font.SysFont(None, 48)
font_button = pygame.font.SysFont(None, 32)


def draw_button(surface, text, x, y, width, height, color=LIGHT_BLUE):
    """Draw a button and return its rectangle for collision detection."""
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, button_rect)
    pygame.draw.rect(surface, BLACK, button_rect, 2)

    text_surface = font_button.render(text, True, BLACK)
    text_x = x + (width - text_surface.get_width()) // 2
    text_y = y + (height - text_surface.get_height()) // 2
    surface.blit(text_surface, (text_x, text_y))

    return button_rect


def run_game(game_script):
    """Run a game script."""
    try:
        # Get the directory of this launcher script
        launcher_dir = os.path.dirname(os.path.abspath(__file__))
        game_path = os.path.join(launcher_dir, game_script)

        if os.path.exists(game_path):
            # Close the launcher
            pygame.quit()

            # Run the game
            subprocess.run([sys.executable, game_path])

            # Restart the launcher after the game closes
            main()
        else:
            print(f"Game not found: {game_path}")
    except Exception as e:
        print(f"Error running game: {e}")


def main():
    """Main launcher loop."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Launcher")

    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # Check button clicks
                if shooter_button.collidepoint(mouse_pos):
                    run_game("main.py")
                elif flappy_button.collidepoint(mouse_pos):
                    run_game("flappy_bird.py")
                elif quit_button.collidepoint(mouse_pos):
                    running = False

        # Clear screen
        screen.fill(WHITE)

        # Draw title
        title_text = font_title.render("Game Launcher", True, BLACK)
        title_x = (SCREEN_WIDTH - title_text.get_width()) // 2
        screen.blit(title_text, (title_x, 50))

        # Draw subtitle
        subtitle_text = font_button.render("Choose a game to play:", True, GRAY)
        subtitle_x = (SCREEN_WIDTH - subtitle_text.get_width()) // 2
        screen.blit(subtitle_text, (subtitle_x, 100))

        # Draw buttons
        button_width = 200
        button_height = 50
        button_x = (SCREEN_WIDTH - button_width) // 2

        shooter_button = draw_button(
            screen, "2D Platform Shooter", button_x, 150, button_width, button_height
        )

        flappy_button = draw_button(
            screen, "Flappy Bird", button_x, 220, button_width, button_height
        )

        quit_button = draw_button(
            screen, "Quit", button_x, 290, button_width, button_height, GRAY
        )

        # Draw instructions
        instructions = [
            "Controls:",
            "• Platform Shooter: WASD + Space + Mouse",
            "• Flappy Bird: Spacebar to flap",
        ]

        for i, instruction in enumerate(instructions):
            color = BLACK if i == 0 else GRAY
            text = (
                font_button.render(instruction, True, color)
                if i == 0
                else pygame.font.SysFont(None, 24).render(instruction, True, color)
            )
            screen.blit(text, (20, 350 + i * 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
