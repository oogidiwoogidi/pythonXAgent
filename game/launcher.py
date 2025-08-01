#!/usr/bin/env python3
"""
2D Platform Shooter Launcher

Simple launcher for the 2D Platform Shooter game.
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
pygame.display.set_caption("2D Platform Shooter")

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


def run_game():
    """Run the platform shooter game."""
    try:
        # Get the directory of this launcher script
        launcher_dir = os.path.dirname(os.path.abspath(__file__))
        game_path = os.path.join(launcher_dir, "main.py")

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
    pygame.display.set_caption("2D Platform Shooter")

    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # Check button clicks
                if start_button.collidepoint(mouse_pos):
                    run_game()
                elif quit_button.collidepoint(mouse_pos):
                    running = False

        # Clear screen
        screen.fill(WHITE)

        # Draw title
        title_text = font_title.render("2D Platform Shooter", True, BLACK)
        title_x = (SCREEN_WIDTH - title_text.get_width()) // 2
        screen.blit(title_text, (title_x, 50))

        # Draw subtitle
        subtitle_text = font_button.render("Fast-paced action platformer", True, GRAY)
        subtitle_x = (SCREEN_WIDTH - subtitle_text.get_width()) // 2
        screen.blit(subtitle_text, (subtitle_x, 100))

        # Draw buttons
        button_width = 200
        button_height = 50
        button_x = (SCREEN_WIDTH - button_width) // 2

        start_button = draw_button(
            screen, "Start Game", button_x, 180, button_width, button_height
        )

        quit_button = draw_button(
            screen, "Quit", button_x, 250, button_width, button_height, GRAY
        )

        # Draw instructions
        instructions = [
            "Controls:",
            "• WASD keys to move",
            "• Space to jump",
            "• Mouse to aim and shoot",
            "• 1/2 keys to switch weapons",
        ]

        for i, instruction in enumerate(instructions):
            color = BLACK if i == 0 else GRAY
            text = (
                font_button.render(instruction, True, color)
                if i == 0
                else pygame.font.SysFont(None, 24).render(instruction, True, color)
            )
            screen.blit(text, (20, 320 + i * 25))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
