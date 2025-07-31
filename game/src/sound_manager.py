"""
Sound Manager

Handles loading and playing sound effects for the game.
"""

import pygame
import os


class SoundManager:
    def __init__(self, assets_path):
        self.assets_path = assets_path
        self.sounds = {}
        self._load_sounds()

    def _load_sounds(self):
        # Add your .wav files to the assets folder
        sound_files = {
            "jump": "jump.wav",
            "shoot": "shoot.wav",
            "damage": "damage.wav",
            "game_over": "game_over.wav",
        }
        for key, filename in sound_files.items():
            path = os.path.join(self.assets_path, filename)
            if os.path.exists(path):
                self.sounds[key] = pygame.mixer.Sound(path)
            else:
                self.sounds[key] = None  # Placeholder if file is missing

    def play(self, sound_key):
        sound = self.sounds.get(sound_key)
        if sound:
            sound.play()


# Usage:
# sound_manager = SoundManager(os.path.join(os.path.dirname(__file__), '../assets'))
# sound_manager.play('jump')
