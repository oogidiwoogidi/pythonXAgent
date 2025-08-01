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
        # Look for sound files in the assets/sounds folder
        sounds_path = os.path.join(self.assets_path, "sounds")
        sound_files = {
            "jump": "jump.wav",
            "shoot": "shoot.mp3",
            "damage": "damage.wav",
            "game_over": "game_over.wav",
        }
        for key, filename in sound_files.items():
            path = os.path.join(sounds_path, filename)
            if os.path.exists(path):
                self.sounds[key] = pygame.mixer.Sound(path)
                # Set much quieter volume for gunshot sound
                if key == "shoot":
                    self.sounds[key].set_volume(
                        0.2
                    )  # 20% volume for very quiet gunshots
                print(f"Loaded sound: {key} from {path}")
            else:
                self.sounds[key] = None  # Placeholder if file is missing
                print(f"Sound file not found: {path}")

    def play(self, sound_key, volume=None):
        sound = self.sounds.get(sound_key)
        if sound:
            if volume is not None:
                sound.set_volume(volume)
            sound.play()


# Usage:
# sound_manager = SoundManager(os.path.join(os.path.dirname(__file__), '../assets'))
# sound_manager.play('jump')
