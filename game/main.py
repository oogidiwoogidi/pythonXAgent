"""
2D Platform Shooter Game - Main Entry Point

A multiplayer 2D platform shooter game with weapon system,
gravity physics, and multiple difficulty levels.
"""

import pygame
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from game_engine import GameEngine


def main():
    """Main entry point for the game."""
    try:
        # Initialize the game engine
        game = GameEngine()

        # Start the game loop
        game.run()

    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
