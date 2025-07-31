"""
Sprite System - Advanced Graphics Mod Pack

This module provides a sprite management system that can use either
actual image files or procedurally generated sprites for enhanced visuals.
"""

import pygame
import math
import os
from config import *


class SpriteManager:
    """Manages all sprites and textures for the game."""

    def __init__(self):
        self.sprites = {}
        self.animations = {}
        self.generated_sprites = {}
        self._generate_default_sprites()

    def _generate_default_sprites(self):
        """Generate default sprites procedurally when image files aren't available."""

        # Player sprite (ninja-like character)
        self.generated_sprites["player"] = self._create_player_sprite(
            PLAYER_SIZE, PLAYER_COLOR
        )
        self.generated_sprites["player2"] = self._create_player_sprite(
            PLAYER2_SIZE, PLAYER2_COLOR
        )

        # Enemy sprite (robot-like)
        self.generated_sprites["enemy"] = self._create_enemy_sprite(
            ENEMY_SIZE, ENEMY_COLOR
        )

        # Weapon sprites
        self.generated_sprites["rifle"] = self._create_rifle_sprite()
        self.generated_sprites["pistol"] = self._create_pistol_sprite()

        # Bullet sprites
        self.generated_sprites["bullet"] = self._create_bullet_sprite(
            BULLET_WIDTH, BULLET_HEIGHT, BULLET_COLOR
        )
        self.generated_sprites["player_bullet"] = self._create_bullet_sprite(
            PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT, PLAYER_BULLET_COLOR
        )
        self.generated_sprites["player2_bullet"] = self._create_bullet_sprite(
            PLAYER2_BULLET_WIDTH, PLAYER2_BULLET_HEIGHT, PLAYER2_BULLET_COLOR
        )

        # Platform textures
        self.generated_sprites["platform"] = self._create_platform_texture(
            PLATFORM_MIN_WIDTH, PLATFORM_HEIGHT
        )

        # UI elements
        self.generated_sprites["crosshair"] = self._create_crosshair()

    def _create_player_sprite(self, size, color):
        """Create a ninja-like player sprite."""
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        # Body (main rectangle with rounded corners effect)
        body_rect = pygame.Rect(size // 4, size // 3, size // 2, size // 2)
        pygame.draw.rect(surf, color, body_rect)
        pygame.draw.rect(surf, (255, 255, 255), body_rect, 2)

        # Head
        head_radius = size // 6
        pygame.draw.circle(surf, color, (size // 2, size // 4), head_radius)
        pygame.draw.circle(
            surf, (255, 255, 255), (size // 2, size // 4), head_radius, 2
        )

        # Eyes
        eye_size = 2
        pygame.draw.circle(
            surf, (255, 255, 255), (size // 2 - 3, size // 4 - 2), eye_size
        )
        pygame.draw.circle(
            surf, (255, 255, 255), (size // 2 + 3, size // 4 - 2), eye_size
        )

        # Arms
        arm_width = size // 8
        arm_height = size // 3
        # Left arm
        pygame.draw.rect(
            surf, color, (size // 4 - arm_width, size // 3, arm_width, arm_height)
        )
        # Right arm
        pygame.draw.rect(surf, color, (3 * size // 4, size // 3, arm_width, arm_height))

        # Legs
        leg_width = size // 10
        leg_height = size // 4
        # Left leg
        pygame.draw.rect(
            surf,
            color,
            (size // 2 - leg_width - 2, 3 * size // 4, leg_width, leg_height),
        )
        # Right leg
        pygame.draw.rect(
            surf, color, (size // 2 + 2, 3 * size // 4, leg_width, leg_height)
        )

        return surf

    def _create_enemy_sprite(self, size, color):
        """Create a robot-like enemy sprite."""
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        # Body (angular robot design)
        body_rect = pygame.Rect(size // 4, size // 3, size // 2, size // 2)
        pygame.draw.rect(surf, color, body_rect)
        pygame.draw.rect(surf, (100, 100, 100), body_rect, 2)

        # Head (square)
        head_size = size // 3
        head_rect = pygame.Rect(
            size // 2 - head_size // 2, size // 8, head_size, head_size
        )
        pygame.draw.rect(surf, color, head_rect)
        pygame.draw.rect(surf, (100, 100, 100), head_rect, 2)

        # Eyes (glowing red)
        eye_size = 3
        pygame.draw.circle(surf, (255, 0, 0), (size // 2 - 4, size // 4), eye_size)
        pygame.draw.circle(surf, (255, 0, 0), (size // 2 + 4, size // 4), eye_size)

        # Antenna
        pygame.draw.line(
            surf, (100, 100, 100), (size // 2, size // 8), (size // 2, size // 16), 2
        )
        pygame.draw.circle(surf, (255, 0, 0), (size // 2, size // 16), 2)

        # Arms (mechanical)
        arm_width = size // 6
        arm_height = size // 3
        # Left arm
        arm_rect1 = pygame.Rect(size // 4 - arm_width, size // 3, arm_width, arm_height)
        pygame.draw.rect(surf, color, arm_rect1)
        pygame.draw.rect(surf, (100, 100, 100), arm_rect1, 1)
        # Right arm
        arm_rect2 = pygame.Rect(3 * size // 4, size // 3, arm_width, arm_height)
        pygame.draw.rect(surf, color, arm_rect2)
        pygame.draw.rect(surf, (100, 100, 100), arm_rect2, 1)

        return surf

    def _create_rifle_sprite(self):
        """Create a rifle weapon sprite."""
        surf = pygame.Surface((30, 8), pygame.SRCALPHA)

        # Barrel
        pygame.draw.rect(surf, (60, 60, 60), (0, 2, 25, 4))

        # Stock
        pygame.draw.rect(surf, (80, 60, 40), (20, 0, 10, 8))

        # Trigger guard
        pygame.draw.rect(surf, (60, 60, 60), (15, 3, 8, 2))

        return surf

    def _create_pistol_sprite(self):
        """Create a pistol weapon sprite."""
        surf = pygame.Surface((20, 12), pygame.SRCALPHA)

        # Barrel
        pygame.draw.rect(surf, (60, 60, 60), (0, 4, 15, 4))

        # Handle
        pygame.draw.rect(surf, (80, 60, 40), (10, 5, 6, 7))

        # Trigger
        pygame.draw.rect(surf, (60, 60, 60), (12, 8, 2, 2))

        return surf

    def _create_bullet_sprite(self, width, height, color):
        """Create an enhanced bullet sprite."""
        surf = pygame.Surface((width + 4, height + 2), pygame.SRCALPHA)

        # Main bullet body
        bullet_rect = pygame.Rect(2, 1, width, height)
        pygame.draw.rect(surf, color, bullet_rect)

        # Bullet tip (pointed)
        tip_points = [
            (width + 2, height // 2 + 1),
            (width + 4, height // 2 + 1),
            (width + 3, 1),
            (width + 3, height + 1),
        ]
        pygame.draw.polygon(surf, color, tip_points)

        # Bullet glow
        glow_surf = pygame.Surface((width + 6, height + 4), pygame.SRCALPHA)
        glow_color = (*color[:3], 100)
        pygame.draw.rect(glow_surf, glow_color, (0, 0, width + 6, height + 4))

        final_surf = pygame.Surface((width + 6, height + 4), pygame.SRCALPHA)
        final_surf.blit(glow_surf, (0, 0))
        final_surf.blit(surf, (1, 1))

        return final_surf

    def _create_platform_texture(self, width, height):
        """Create a textured platform sprite."""
        surf = pygame.Surface((width, height), pygame.SRCALPHA)

        # Base platform color
        pygame.draw.rect(surf, PLATFORM_COLOR, (0, 0, width, height))

        # Add texture lines
        for i in range(0, width, 8):
            pygame.draw.line(surf, (100, 100, 100), (i, 0), (i, height))

        for i in range(0, height, 4):
            pygame.draw.line(surf, (100, 100, 100), (0, i), (width, i))

        # Border
        pygame.draw.rect(surf, (80, 80, 80), (0, 0, width, height), 2)

        # Highlight on top
        pygame.draw.line(surf, (180, 180, 180), (0, 1), (width, 1), 1)

        return surf

    def _create_crosshair(self):
        """Create a crosshair sprite for aiming."""
        surf = pygame.Surface((20, 20), pygame.SRCALPHA)

        center = 10
        # Horizontal line
        pygame.draw.line(
            surf, (255, 255, 255), (center - 8, center), (center - 3, center), 2
        )
        pygame.draw.line(
            surf, (255, 255, 255), (center + 3, center), (center + 8, center), 2
        )

        # Vertical line
        pygame.draw.line(
            surf, (255, 255, 255), (center, center - 8), (center, center - 3), 2
        )
        pygame.draw.line(
            surf, (255, 255, 255), (center, center + 3), (center, center + 8), 2
        )

        # Center dot
        pygame.draw.circle(surf, (255, 0, 0), (center, center), 1)

        return surf

    def get_sprite(self, name):
        """Get a sprite by name."""
        if name in self.sprites:
            return self.sprites[name]
        elif name in self.generated_sprites:
            return self.generated_sprites[name]
        else:
            # Return a default colored rectangle if sprite not found
            return pygame.Surface((20, 20))

    def load_sprite(self, name, file_path):
        """Load a sprite from file."""
        try:
            sprite = pygame.image.load(file_path).convert_alpha()
            self.sprites[name] = sprite
            return sprite
        except pygame.error:
            print(f"Could not load sprite: {file_path}")
            return self.get_sprite(name)  # Return generated sprite as fallback

    def scale_sprite(self, sprite, width, height):
        """Scale a sprite to specified dimensions."""
        return pygame.transform.scale(sprite, (width, height))

    def rotate_sprite(self, sprite, angle):
        """Rotate a sprite by specified angle."""
        return pygame.transform.rotate(sprite, angle)


class AnimationManager:
    """Manages sprite animations."""

    def __init__(self):
        self.animations = {}
        self.animation_states = {}

    def create_animation(self, name, frames, frame_duration):
        """Create an animation from a list of frames."""
        self.animations[name] = {
            "frames": frames,
            "frame_duration": frame_duration,
            "total_frames": len(frames),
        }

    def start_animation(self, entity_id, animation_name):
        """Start an animation for an entity."""
        if animation_name in self.animations:
            self.animation_states[entity_id] = {
                "animation": animation_name,
                "current_frame": 0,
                "frame_timer": 0,
            }

    def update_animations(self):
        """Update all active animations."""
        for entity_id, state in self.animation_states.items():
            animation = self.animations[state["animation"]]
            state["frame_timer"] += 1

            if state["frame_timer"] >= animation["frame_duration"]:
                state["frame_timer"] = 0
                state["current_frame"] = (state["current_frame"] + 1) % animation[
                    "total_frames"
                ]

    def get_current_frame(self, entity_id):
        """Get the current animation frame for an entity."""
        if entity_id not in self.animation_states:
            return None

        state = self.animation_states[entity_id]
        animation = self.animations[state["animation"]]
        return animation["frames"][state["current_frame"]]


# Global instances
sprite_manager = SpriteManager()
animation_manager = AnimationManager()
