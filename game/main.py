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
        # Pre-initialize mixer for better sound compatibility
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.init()

        try:
            pygame.mixer.init()
            # Set mixer channels for sound effects
            pygame.mixer.set_num_channels(8)
        except Exception as mixer_error:
            print(f"Failed to initialize mixer: {mixer_error}")

        # Load background music
        music_path = r"C:\Users\Elyas\Downloads\Dark Tension Suspense Cinematic NoCopyright Background Music 1 Hour by Soundridemusic.mp3"
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)  # Loop forever
                print("Background music started.")
            except Exception as music_error:
                print(f"Failed to play music: {music_error}")
        else:
            print(f"Background music file not found: {music_path}")

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
    sys.exit()
