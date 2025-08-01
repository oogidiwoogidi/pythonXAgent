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
        self.animated_sprites = {}
        self._generate_default_sprites()
        self._generate_animated_sprites()

    def _generate_default_sprites(self):
        """Generate default static sprites for fallback and UI elements."""
        # Bullets
        self.generated_sprites["bullet"] = self._create_bullet_sprite(
            BULLET_WIDTH, BULLET_HEIGHT, BULLET_COLOR
        )
        self.generated_sprites["player_bullet"] = self._create_bullet_sprite(
            PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT, PLAYER_BULLET_COLOR
        )
        self.generated_sprites["player2_bullet"] = self._create_bullet_sprite(
            PLAYER2_BULLET_WIDTH, PLAYER2_BULLET_HEIGHT, PLAYER2_BULLET_COLOR
        )
        # Platform
        self.generated_sprites["platform"] = self._create_platform_texture(
            PLATFORM_MIN_WIDTH, PLATFORM_HEIGHT
        )
        # UI
        self.generated_sprites["crosshair"] = self._create_crosshair()

    def _generate_animated_sprites(self):
        """Generate animated sprite frame lists for player, player2, enemy, and weapons."""
        # Player animations: idle, walk, jump
        self.animated_sprites["player_idle"] = [
            self._create_player_sprite(PLAYER_SIZE, PLAYER_COLOR, pose="idle", frame=i)
            for i in range(4)
        ]
        self.animated_sprites["player_walk"] = [
            self._create_player_sprite(PLAYER_SIZE, PLAYER_COLOR, pose="walk", frame=i)
            for i in range(6)
        ]
        self.animated_sprites["player_jump"] = [
            self._create_player_sprite(PLAYER_SIZE, PLAYER_COLOR, pose="jump", frame=i)
            for i in range(2)
        ]

        self.animated_sprites["player2_idle"] = [
            self._create_player_sprite(
                PLAYER2_SIZE, PLAYER2_COLOR, pose="idle", frame=i
            )
            for i in range(4)
        ]
        self.animated_sprites["player2_walk"] = [
            self._create_player_sprite(
                PLAYER2_SIZE, PLAYER2_COLOR, pose="walk", frame=i
            )
            for i in range(6)
        ]
        self.animated_sprites["player2_jump"] = [
            self._create_player_sprite(
                PLAYER2_SIZE, PLAYER2_COLOR, pose="jump", frame=i
            )
            for i in range(2)
        ]

        # Enemy animations: idle, walk, attack
        self.animated_sprites["enemy_idle"] = [
            self._create_enemy_sprite(ENEMY_SIZE, ENEMY_COLOR, pose="idle", frame=i)
            for i in range(4)
        ]
        self.animated_sprites["enemy_walk"] = [
            self._create_enemy_sprite(ENEMY_SIZE, ENEMY_COLOR, pose="walk", frame=i)
            for i in range(6)
        ]
        self.animated_sprites["enemy_attack"] = [
            self._create_enemy_sprite(ENEMY_SIZE, ENEMY_COLOR, pose="attack", frame=i)
            for i in range(4)
        ]

        # Weapons (static for now, could animate firing later)
        self.animated_sprites["blaster"] = [self._create_blaster_sprite()]
        self.animated_sprites["pistol"] = [self._create_pistol_sprite()]

    def _create_player_sprite(
        self, size, color, pose="idle", frame=0, facing_right=True
    ):
        """Create a detailed soldier sprite with enhanced anatomy and directional face."""
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        # Soldier body proportions (taller with longer legs for proper support)
        head_radius = size // 7  # Slightly smaller head for taller proportions
        neck_height = size // 12  # Thinner neck
        torso_width = size // 2.8  # Slightly narrower torso
        torso_height = size // 2.2  # Shorter torso to make room for much longer legs

        # Military helmet head
        head_center = (size // 2, head_radius + 3)
        pygame.draw.circle(surf, (60, 80, 60), head_center, head_radius)  # Olive helmet
        pygame.draw.circle(
            surf, (40, 60, 40), head_center, head_radius, 2
        )  # Darker rim

        # Helmet chin strap
        strap_y = head_center[1] + head_radius // 2
        pygame.draw.line(
            surf,
            (40, 60, 40),
            (head_center[0] - head_radius + 2, strap_y),
            (head_center[0] + head_radius - 2, strap_y),
            2,
        )

        # Face under helmet (visible part)
        face_rect = pygame.Rect(
            size // 2 - head_radius + 3,
            head_center[1] - head_radius // 3,
            (head_radius - 3) * 2,
            head_radius // 2,
        )
        pygame.draw.rect(surf, (220, 180, 140), face_rect)  # Skin tone

        # Directional soldier face features
        eye_y = head_radius - 1
        if facing_right:
            # Eyes looking right
            pygame.draw.ellipse(surf, (255, 255, 255), (size // 2 - 4, eye_y, 5, 3))
            pygame.draw.ellipse(surf, (255, 255, 255), (size // 2 + 3, eye_y, 5, 3))
            # Blue military eyes looking right
            pygame.draw.circle(surf, (50, 100, 180), (size // 2 - 1, eye_y + 1), 1)
            pygame.draw.circle(surf, (50, 100, 180), (size // 2 + 6, eye_y + 1), 1)
        else:
            # Eyes looking left
            pygame.draw.ellipse(surf, (255, 255, 255), (size // 2 - 7, eye_y, 5, 3))
            pygame.draw.ellipse(surf, (255, 255, 255), (size // 2, eye_y, 5, 3))
            # Blue military eyes looking left
            pygame.draw.circle(surf, (50, 100, 180), (size // 2 - 6, eye_y + 1), 1)
            pygame.draw.circle(surf, (50, 100, 180), (size // 2 + 1, eye_y + 1), 1)

        # Neck with military collar
        neck_rect = pygame.Rect(size // 2 - 3, head_radius * 2 + 1, 6, neck_height)
        pygame.draw.rect(surf, (220, 180, 140), neck_rect)  # Skin tone

        # Military collar
        collar_rect = pygame.Rect(
            size // 2 - 5, head_radius * 2 + neck_height - 2, 10, 3
        )
        pygame.draw.rect(surf, (80, 100, 60), collar_rect)

        # Military uniform torso
        torso_y = head_radius * 2 + neck_height + 1
        torso_rect = pygame.Rect(
            size // 2 - torso_width // 2, torso_y, torso_width, int(torso_height)
        )
        pygame.draw.rect(surf, color, torso_rect)  # Main uniform
        pygame.draw.rect(surf, (70, 90, 70), torso_rect, 2)  # Military trim

        # Military details - chest pockets
        pocket_rect = pygame.Rect(
            size // 2 - torso_width // 3, torso_y + 6, torso_width // 2, 5
        )
        pygame.draw.rect(surf, (60, 80, 60), pocket_rect)
        pygame.draw.rect(surf, (40, 60, 40), pocket_rect, 1)

        # Military belt
        belt_y = torso_y + int(torso_height * 0.7)
        pygame.draw.rect(
            surf, (80, 60, 40), (size // 2 - torso_width // 2, belt_y, torso_width, 5)
        )
        # Belt buckle
        buckle_rect = pygame.Rect(size // 2 - 3, belt_y + 1, 6, 3)
        pygame.draw.rect(surf, (200, 180, 100), buckle_rect)

        # Enhanced soldier arms and legs with thicker limbs (MUCH TALLER)
        arm_width = size // 8  # Thicker arms
        arm_length = size // 2.5  # Longer arms
        leg_width = size // 10  # Thicker legs
        leg_length = (
            size // 1.3
        )  # MUCH LONGER legs - soldiers properly supported by legs

        # Shoulder positions
        shoulder_y = torso_y + 8
        left_shoulder = (size // 2 - torso_width // 2 + 3, shoulder_y)
        right_shoulder = (size // 2 + torso_width // 2 - 3, shoulder_y)

        # Hip positions for legs - CENTERED UNDER BODY instead of on sides
        hip_y = torso_y + int(torso_height) - 8
        left_hip = (size // 2 - 4, hip_y)  # Much closer to center
        right_hip = (size // 2 + 4, hip_y)  # Much closer to center

        # Animation: military marching movements with thicker limbs
        if pose == "walk":
            # Military marching with disciplined arm and leg movements
            swing = int(math.sin(frame / 6 * math.pi * 2) * 8)  # More controlled swing
            lean = int(math.sin(frame / 6 * math.pi * 2) * 2)  # Less body lean

            # Military left arm with elbow joint
            left_arm_mid = (
                left_shoulder[0] - 5 + swing // 2,
                left_shoulder[1] + arm_length // 2,
            )
            left_arm_end = (
                left_shoulder[0] - 8 + swing,
                left_shoulder[1] + arm_length - abs(swing) // 2,
            )
            pygame.draw.line(surf, color, left_shoulder, left_arm_mid, arm_width)
            pygame.draw.line(surf, color, left_arm_mid, left_arm_end, arm_width)
            pygame.draw.circle(
                surf, (220, 180, 140), left_arm_end, arm_width // 2 + 1
            )  # Skin tone hand

            # Military right arm with elbow joint
            right_arm_mid = (
                right_shoulder[0] + 5 - swing // 2,
                right_shoulder[1] + arm_length // 2,
            )
            right_arm_end = (
                right_shoulder[0] + 8 - swing,
                right_shoulder[1] + arm_length - abs(swing) // 2,
            )
            pygame.draw.line(surf, color, right_shoulder, right_arm_mid, arm_width)
            pygame.draw.line(surf, color, right_arm_mid, right_arm_end, arm_width)
            pygame.draw.circle(
                surf, (220, 180, 140), right_arm_end, arm_width // 2 + 1
            )  # Skin tone hand

            # Enhanced marching cycle - legs positioned under body
            # Calculate walking phase for each leg (opposite phases)
            left_leg_phase = math.sin(frame / 6 * math.pi * 2)  # -1 to 1
            right_leg_phase = math.sin(
                frame / 6 * math.pi * 2 + math.pi
            )  # Opposite phase

            # Left leg with realistic marching step cycle
            if left_leg_phase > 0:  # Lifting/forward phase
                left_step_height = int(left_leg_phase * 6)  # Military step height
                left_step_forward = int(
                    left_leg_phase * 10
                )  # Shorter, more controlled steps
                left_knee_bend = int(left_leg_phase * 8)  # Controlled knee bend

                left_knee = (
                    left_hip[0] + left_step_forward // 3,  # Knee follows forward motion
                    left_hip[1] + leg_length // 2 - left_knee_bend,
                )
                left_leg_end = (
                    left_hip[0] + left_step_forward,
                    left_hip[1] + leg_length - left_step_height,
                )
            else:  # Planted/pushing phase
                left_step_back = int(
                    abs(left_leg_phase) * 8
                )  # Push back for propulsion
                left_knee = (
                    left_hip[0] - left_step_back // 4,
                    left_hip[1] + leg_length // 2,
                )
                left_leg_end = (
                    left_hip[0] - left_step_back,
                    left_hip[1] + leg_length + lean,
                )

            pygame.draw.line(surf, color, left_hip, left_knee, leg_width)
            pygame.draw.line(surf, color, left_knee, left_leg_end, leg_width)
            # Military boots
            pygame.draw.rect(
                surf, (40, 30, 20), (left_leg_end[0] - 4, left_leg_end[1] - 2, 8, 5)
            )

            # Right leg with realistic marching step cycle (opposite of left)
            if right_leg_phase > 0:  # Lifting/forward phase
                right_step_height = int(right_leg_phase * 6)  # Military step height
                right_step_forward = int(
                    right_leg_phase * 10
                )  # Shorter, more controlled steps
                right_knee_bend = int(right_leg_phase * 8)  # Controlled knee bend

                right_knee = (
                    right_hip[0]
                    + right_step_forward // 3,  # Knee follows forward motion
                    right_hip[1] + leg_length // 2 - right_knee_bend,
                )
                right_leg_end = (
                    right_hip[0] + right_step_forward,
                    right_hip[1] + leg_length - right_step_height,
                )
            else:  # Planted/pushing phase
                right_step_back = int(
                    abs(right_leg_phase) * 8
                )  # Push back for propulsion
                right_knee = (
                    right_hip[0] - right_step_back // 4,
                    right_hip[1] + leg_length // 2,
                )
                right_leg_end = (
                    right_hip[0] - right_step_back,
                    right_hip[1] + leg_length - lean,
                )

            pygame.draw.line(surf, color, right_hip, right_knee, leg_width)
            pygame.draw.line(surf, color, right_knee, right_leg_end, leg_width)
            # Military boots
            pygame.draw.rect(
                surf, (40, 30, 20), (right_leg_end[0] - 4, right_leg_end[1] - 2, 8, 5)
            )

        elif pose == "idle":
            # Military at-attention stance with slight breathing animation
            breath_offset = int(math.sin(frame / 8 * math.pi * 2) * 1)

            # Military arms at sides (disciplined posture)
            left_arm_end = (
                left_shoulder[0] - 4,
                left_shoulder[1] + arm_length - 3 + breath_offset,
            )
            right_arm_end = (
                right_shoulder[0] + 4,
                right_shoulder[1] + arm_length - 3 + breath_offset,
            )

            # Left arm with elbow (straighter than ninja)
            left_arm_mid = (left_shoulder[0] - 2, left_shoulder[1] + arm_length // 2)
            pygame.draw.line(surf, color, left_shoulder, left_arm_mid, arm_width)
            pygame.draw.line(surf, color, left_arm_mid, left_arm_end, arm_width)
            pygame.draw.circle(
                surf, (220, 180, 140), left_arm_end, arm_width // 2 + 1
            )  # Skin tone hand

            # Right arm with elbow (straighter than ninja)
            right_arm_mid = (right_shoulder[0] + 2, right_shoulder[1] + arm_length // 2)
            pygame.draw.line(surf, color, right_shoulder, right_arm_mid, arm_width)
            pygame.draw.line(surf, color, right_arm_mid, right_arm_end, arm_width)
            pygame.draw.circle(
                surf, (220, 180, 140), right_arm_end, arm_width // 2 + 1
            )  # Skin tone hand

            # Military legs at attention (centered under body)
            left_leg_end = (left_hip[0], left_hip[1] + leg_length + breath_offset)
            right_leg_end = (right_hip[0], right_hip[1] + leg_length + breath_offset)

            # Left leg with knee (straight military posture)
            left_knee = (left_hip[0], left_hip[1] + leg_length // 2)
            pygame.draw.line(surf, color, left_hip, left_knee, leg_width)
            pygame.draw.line(surf, color, left_knee, left_leg_end, leg_width)
            pygame.draw.rect(
                surf, (40, 30, 20), (left_leg_end[0] - 4, left_leg_end[1] - 2, 8, 5)
            )  # Military boot

            # Right leg with knee (straight military posture)
            right_knee = (right_hip[0], right_hip[1] + leg_length // 2)
            pygame.draw.line(surf, color, right_hip, right_knee, leg_width)
            pygame.draw.line(surf, color, right_knee, right_leg_end, leg_width)
            pygame.draw.rect(
                surf, (40, 30, 20), (right_leg_end[0] - 4, right_leg_end[1] - 2, 8, 5)
            )  # Military boot

        elif pose == "jump":
            # Dynamic attack pose with raised weapon arm
            attack_intensity = int(math.sin(frame / 4 * math.pi * 2) * 5)

            # Left arm (weapon arm) raised up
            left_arm_mid = (
                left_shoulder[0] - 8,
                left_shoulder[1] - 10 + attack_intensity,
            )
            left_arm_end = (
                left_shoulder[0] - 15,
                left_shoulder[1] - 20 + attack_intensity,
            )
            pygame.draw.line(surf, color, left_shoulder, left_arm_mid, arm_width)
            pygame.draw.line(surf, color, left_arm_mid, left_arm_end, arm_width)
            pygame.draw.circle(surf, color, left_arm_end, arm_width // 2 + 1)  # Hand

            # Right arm extended for balance
            right_arm_mid = (right_shoulder[0] + 5, right_shoulder[1] + 5)
            right_arm_end = (right_shoulder[0] + 12, right_shoulder[1] + arm_length - 8)
            pygame.draw.line(surf, color, right_shoulder, right_arm_mid, arm_width)
            pygame.draw.line(surf, color, right_arm_mid, right_arm_end, arm_width)
            pygame.draw.circle(surf, color, right_arm_end, arm_width // 2 + 1)  # Hand

            # Spread legs for stability
            left_leg_end = (left_hip[0] - 8, left_hip[1] + leg_length - 3)
            right_leg_end = (right_hip[0] + 8, right_hip[1] + leg_length - 3)

            # Left leg with knee
            left_knee = (left_hip[0] - 4, left_hip[1] + leg_length // 2)
            pygame.draw.line(surf, color, left_hip, left_knee, leg_width)
            pygame.draw.line(surf, color, left_knee, left_leg_end, leg_width)
            pygame.draw.ellipse(
                surf, (50, 50, 50), (left_leg_end[0] - 3, left_leg_end[1] - 2, 6, 4)
            )  # Foot

            # Right leg with knee
            right_knee = (right_hip[0] + 4, right_hip[1] + leg_length // 2)
            pygame.draw.line(surf, color, right_hip, right_knee, leg_width)
            pygame.draw.line(surf, color, right_knee, right_leg_end, leg_width)
            pygame.draw.ellipse(
                surf, (50, 50, 50), (right_leg_end[0] - 3, right_leg_end[1] - 2, 6, 4)
            )  # Foot

        return surf

    def _create_enemy_sprite(self, size, color, pose="idle", frame=0):
        """Create a detailed robot-ninja enemy sprite with enhanced anatomy and animation."""
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        # Robot soldier proportions (much taller with proper leg support)
        head_size = size // 3.5  # Slightly smaller head for taller proportions
        neck_height = size // 14  # Thinner neck
        torso_width = size // 2.8  # Slightly narrower torso
        torso_height = size // 2.2  # Shorter torso to make room for much longer legs

        # Head (angular robot design)
        head_y = 3
        head_rect = pygame.Rect(
            size // 2 - head_size // 2, head_y, head_size, head_size
        )
        pygame.draw.rect(surf, color, head_rect)
        pygame.draw.rect(surf, (80, 80, 80), head_rect, 2)

        # Robot visor/face plate
        visor_rect = pygame.Rect(
            size // 2 - head_size // 2 + 2, head_y + 2, head_size - 4, head_size // 2
        )
        pygame.draw.rect(surf, (20, 20, 20), visor_rect)

        # Glowing red eyes (directional and larger for robot)
        eye_size = 4
        eye_y = head_y + head_size // 3

        # Determine eye direction based on frame animation
        eye_direction = int(math.sin(frame / 10 * math.pi * 2) * 2)  # -2 to 2 range

        # Eyes look slightly in direction (left/right scanning)
        left_eye_x = size // 2 - 6 + eye_direction
        right_eye_x = size // 2 + 6 + eye_direction

        pygame.draw.circle(surf, (255, 50, 50), (left_eye_x, eye_y), eye_size)
        pygame.draw.circle(surf, (255, 50, 50), (right_eye_x, eye_y), eye_size)
        # Eye glow effect
        pygame.draw.circle(surf, (255, 100, 100), (left_eye_x, eye_y), eye_size + 1, 1)
        pygame.draw.circle(surf, (255, 100, 100), (right_eye_x, eye_y), eye_size + 1, 1)

        # Antenna array
        antenna_x = size // 2
        antenna_top = head_y - 2
        pygame.draw.line(
            surf,
            (120, 120, 120),
            (antenna_x - 3, head_y),
            (antenna_x - 3, antenna_top),
            2,
        )
        pygame.draw.line(
            surf, (120, 120, 120), (antenna_x, head_y), (antenna_x, antenna_top - 3), 2
        )
        pygame.draw.line(
            surf,
            (120, 120, 120),
            (antenna_x + 3, head_y),
            (antenna_x + 3, antenna_top),
            2,
        )
        pygame.draw.circle(surf, (255, 0, 0), (antenna_x, antenna_top - 3), 2)

        # Neck joint
        neck_y = head_y + head_size
        neck_rect = pygame.Rect(size // 2 - 3, neck_y, 6, neck_height)
        pygame.draw.rect(surf, (60, 60, 60), neck_rect)

        # Mechanical torso with panels
        torso_y = neck_y + neck_height
        torso_rect = pygame.Rect(
            size // 2 - torso_width // 2, torso_y, torso_width, int(torso_height)
        )
        pygame.draw.rect(surf, color, torso_rect)
        pygame.draw.rect(surf, (100, 100, 100), torso_rect, 2)

        # Chest panel details
        panel_rect = pygame.Rect(
            size // 2 - torso_width // 3,
            torso_y + 3,
            torso_width // 1.5,
            torso_height // 3,
        )
        pygame.draw.rect(surf, (40, 40, 40), panel_rect)
        pygame.draw.rect(surf, (120, 120, 120), panel_rect, 1)

        # Power core (glowing center)
        core_center = (size // 2, torso_y + int(torso_height * 0.4))
        pygame.draw.circle(surf, (0, 150, 255), core_center, 3)
        pygame.draw.circle(surf, (100, 200, 255), core_center, 5, 1)

        # Enhanced mechanical arms and legs (MUCH TALLER - properly supported by legs)
        arm_width = size // 8  # Thicker robot arms
        arm_length = size // 2.3  # Longer arms
        leg_width = size // 10  # Thicker robot legs
        leg_length = size // 1.3  # MUCH LONGER legs - robot properly supported by legs

        # Joint positions
        shoulder_y = torso_y + 8
        left_shoulder = (size // 2 - torso_width // 2 + 2, shoulder_y)
        right_shoulder = (size // 2 + torso_width // 2 - 2, shoulder_y)

        hip_y = torso_y + int(torso_height) - 8
        left_hip = (size // 2 - 5, hip_y)  # Centered under body like player
        right_hip = (size // 2 + 5, hip_y)  # Centered under body like player

        if pose == "walk":
            # Mechanical walking with servo movements and thicker limbs
            swing = int(math.sin(frame / 6 * math.pi * 2) * 10)
            mechanical_offset = int(math.sin(frame / 6 * math.pi * 2 + math.pi / 4) * 3)

            # Left mechanical arm with elbow joint
            left_arm_mid = (
                left_shoulder[0] - 6 + swing // 2,
                left_shoulder[1] + arm_length // 2,
            )
            left_arm_end = (
                left_shoulder[0] - 12 + swing,
                left_shoulder[1] + arm_length + mechanical_offset,
            )
            pygame.draw.line(surf, color, left_shoulder, left_arm_mid, arm_width)
            pygame.draw.line(surf, color, left_arm_mid, left_arm_end, arm_width)
            pygame.draw.circle(
                surf, (80, 80, 80), left_shoulder, arm_width // 2 + 1
            )  # Joint
            pygame.draw.circle(
                surf, (80, 80, 80), left_arm_mid, arm_width // 3
            )  # Elbow joint
            pygame.draw.rect(
                surf, (60, 60, 60), (left_arm_end[0] - 4, left_arm_end[1] - 3, 8, 6)
            )  # Bigger hand

            # Right mechanical arm with elbow joint
            right_arm_mid = (
                right_shoulder[0] + 6 - swing // 2,
                right_shoulder[1] + arm_length // 2,
            )
            right_arm_end = (
                right_shoulder[0] + 12 - swing,
                right_shoulder[1] + arm_length - mechanical_offset,
            )
            pygame.draw.line(surf, color, right_shoulder, right_arm_mid, arm_width)
            pygame.draw.line(surf, color, right_arm_mid, right_arm_end, arm_width)
            pygame.draw.circle(
                surf, (80, 80, 80), right_shoulder, arm_width // 2 + 1
            )  # Joint
            pygame.draw.circle(
                surf, (80, 80, 80), right_arm_mid, arm_width // 3
            )  # Elbow joint
            pygame.draw.rect(
                surf, (60, 60, 60), (right_arm_end[0] - 4, right_arm_end[1] - 3, 8, 6)
            )  # Bigger hand

            # Enhanced mechanical walking - legs actually step with hydraulic precision
            # Calculate walking phase for each leg (opposite phases)
            left_leg_phase = math.sin(frame / 6 * math.pi * 2)  # -1 to 1
            right_leg_phase = math.sin(
                frame / 6 * math.pi * 2 + math.pi
            )  # Opposite phase

            # Left mechanical leg with realistic step cycle (centered under body)
            if left_leg_phase > 0:  # Lifting/forward phase
                left_step_height = int(
                    left_leg_phase * 6
                )  # Robot lifts less than soldier
                left_step_forward = int(
                    left_leg_phase * 10
                )  # Shorter steps, more precise
                left_knee_bend = int(left_leg_phase * 8)  # Mechanical knee bend

                left_knee = (
                    left_hip[0] + left_step_forward // 3,  # Knee follows forward motion
                    left_hip[1] + leg_length // 2 - left_knee_bend,
                )
                left_leg_end = (
                    left_hip[0] + left_step_forward,
                    left_hip[1] + leg_length - left_step_height,
                )
            else:  # Planted/pushing phase
                left_step_back = int(abs(left_leg_phase) * 6)  # Mechanical push back
                left_knee = (
                    left_hip[0] - left_step_back // 4,
                    left_hip[1] + leg_length // 2,
                )
                left_leg_end = (
                    left_hip[0] - left_step_back,
                    left_hip[1] + leg_length + mechanical_offset // 2,
                )

            pygame.draw.line(surf, color, left_hip, left_knee, leg_width)
            pygame.draw.line(surf, color, left_knee, left_leg_end, leg_width)
            pygame.draw.circle(
                surf, (80, 80, 80), left_hip, leg_width // 2 + 1
            )  # Hip joint
            pygame.draw.circle(
                surf, (80, 80, 80), left_knee, leg_width // 3
            )  # Knee joint
            pygame.draw.rect(
                surf, (40, 40, 40), (left_leg_end[0] - 5, left_leg_end[1] - 3, 10, 6)
            )  # Mechanical foot

            # Right mechanical leg with realistic step cycle (opposite of left, centered under body)
            if right_leg_phase > 0:  # Lifting/forward phase
                right_step_height = int(
                    right_leg_phase * 6
                )  # Robot lifts less than soldier
                right_step_forward = int(
                    right_leg_phase * 10
                )  # Shorter steps, more precise
                right_knee_bend = int(right_leg_phase * 8)  # Mechanical knee bend

                right_knee = (
                    right_hip[0]
                    + right_step_forward // 3,  # Knee follows forward motion
                    right_hip[1] + leg_length // 2 - right_knee_bend,
                )
                right_leg_end = (
                    right_hip[0] + right_step_forward,
                    right_hip[1] + leg_length - right_step_height,
                )
            else:  # Planted/pushing phase
                right_step_back = int(abs(right_leg_phase) * 6)  # Mechanical push back
                right_knee = (
                    right_hip[0] - right_step_back // 4,
                    right_hip[1] + leg_length // 2,
                )
                right_leg_end = (
                    right_hip[0] - right_step_back,
                    right_hip[1] + leg_length - mechanical_offset // 2,
                )

            pygame.draw.line(surf, color, right_hip, right_knee, leg_width)
            pygame.draw.line(surf, color, right_knee, right_leg_end, leg_width)
            pygame.draw.circle(
                surf, (80, 80, 80), right_hip, leg_width // 2 + 1
            )  # Hip joint
            pygame.draw.circle(
                surf, (80, 80, 80), right_knee, leg_width // 3
            )  # Knee joint
            pygame.draw.rect(
                surf, (40, 40, 40), (right_leg_end[0] - 5, right_leg_end[1] - 3, 10, 6)
            )  # Mechanical foot

        elif pose == "attack":
            # Aggressive attack pose - arms raised, weapons ready with thicker limbs
            attack_pulse = int(math.sin(frame / 4 * math.pi * 2) * 3)

            # Left arm raised with weapon (with elbow joint)
            left_arm_mid = (left_shoulder[0] - 8, left_shoulder[1] - 5 + attack_pulse)
            left_arm_end = (left_shoulder[0] - 15, left_shoulder[1] - 10 + attack_pulse)
            pygame.draw.line(surf, color, left_shoulder, left_arm_mid, arm_width)
            pygame.draw.line(surf, color, left_arm_mid, left_arm_end, arm_width)
            pygame.draw.circle(surf, (80, 80, 80), left_shoulder, arm_width // 2 + 1)
            pygame.draw.circle(
                surf, (80, 80, 80), left_arm_mid, arm_width // 3
            )  # Elbow
            # Weapon attachment
            pygame.draw.rect(
                surf,
                (150, 150, 150),
                (left_arm_end[0] - 3, left_arm_end[1] - 10, 6, 15),
            )

            # Right arm raised (with elbow joint)
            right_arm_mid = (
                right_shoulder[0] + 8,
                right_shoulder[1] - 5 + attack_pulse,
            )
            right_arm_end = (
                right_shoulder[0] + 15,
                right_shoulder[1] - 10 + attack_pulse,
            )
            pygame.draw.line(surf, color, right_shoulder, right_arm_mid, arm_width)
            pygame.draw.line(surf, color, right_arm_mid, right_arm_end, arm_width)
            pygame.draw.circle(surf, (80, 80, 80), right_shoulder, arm_width // 2 + 1)
            pygame.draw.circle(
                surf, (80, 80, 80), right_arm_mid, arm_width // 3
            )  # Elbow
            pygame.draw.rect(
                surf,
                (150, 150, 150),
                (right_arm_end[0] - 3, right_arm_end[1] - 10, 6, 15),
            )

            # Stable combat stance with knee joints
            left_knee = (left_hip[0] - 3, left_hip[1] + leg_length // 2)
            left_leg_end = (left_hip[0] - 5, left_hip[1] + leg_length)
            pygame.draw.line(surf, color, left_hip, left_knee, leg_width)
            pygame.draw.line(surf, color, left_knee, left_leg_end, leg_width)
            pygame.draw.circle(surf, (80, 80, 80), left_hip, leg_width // 2 + 1)
            pygame.draw.circle(surf, (80, 80, 80), left_knee, leg_width // 3)
            pygame.draw.rect(
                surf, (40, 40, 40), (left_leg_end[0] - 5, left_leg_end[1] - 3, 10, 6)
            )

            right_knee = (right_hip[0] + 3, right_hip[1] + leg_length // 2)
            right_leg_end = (right_hip[0] + 5, right_hip[1] + leg_length)
            pygame.draw.line(surf, color, right_hip, right_knee, leg_width)
            pygame.draw.line(surf, color, right_knee, right_leg_end, leg_width)
            pygame.draw.circle(surf, (80, 80, 80), right_hip, leg_width // 2 + 1)
            pygame.draw.circle(surf, (80, 80, 80), right_knee, leg_width // 3)
            pygame.draw.rect(
                surf, (40, 40, 40), (right_leg_end[0] - 5, right_leg_end[1] - 3, 10, 6)
            )

        else:  # idle - mechanical guard mode with thicker limbs
            # Standing guard stance with slight mechanical hum animation
            hum_offset = int(math.sin(frame / 12 * math.pi * 2) * 1)

            # Arms in defensive position with elbow joints
            left_arm_mid = (left_shoulder[0] - 4, left_shoulder[1] + arm_length // 2)
            left_arm_end = (
                left_shoulder[0] - 8,
                left_shoulder[1] + arm_length + hum_offset,
            )
            pygame.draw.line(surf, color, left_shoulder, left_arm_mid, arm_width)
            pygame.draw.line(surf, color, left_arm_mid, left_arm_end, arm_width)
            pygame.draw.circle(surf, (80, 80, 80), left_shoulder, arm_width // 2 + 1)
            pygame.draw.circle(surf, (80, 80, 80), left_arm_mid, arm_width // 3)
            pygame.draw.rect(
                surf, (60, 60, 60), (left_arm_end[0] - 4, left_arm_end[1] - 3, 8, 6)
            )

            right_arm_mid = (right_shoulder[0] + 5, right_shoulder[1] + arm_length // 2)
            right_arm_end = (
                right_shoulder[0] + 10,
                right_shoulder[1] + arm_length - 5 + hum_offset,
            )
            pygame.draw.line(surf, color, right_shoulder, right_arm_mid, arm_width)
            pygame.draw.line(surf, color, right_arm_mid, right_arm_end, arm_width)
            pygame.draw.circle(surf, (80, 80, 80), right_shoulder, arm_width // 2 + 1)
            pygame.draw.circle(surf, (80, 80, 80), right_arm_mid, arm_width // 3)
            pygame.draw.rect(
                surf, (60, 60, 60), (right_arm_end[0] - 4, right_arm_end[1] - 3, 8, 6)
            )

            # Stable mechanical stance with knee joints
            left_knee = (left_hip[0] - 2, left_hip[1] + leg_length // 2)
            left_leg_end = (left_hip[0] - 4, left_hip[1] + leg_length + hum_offset)
            pygame.draw.line(surf, color, left_hip, left_knee, leg_width)
            pygame.draw.line(surf, color, left_knee, left_leg_end, leg_width)
            pygame.draw.circle(surf, (80, 80, 80), left_hip, leg_width // 2 + 1)
            pygame.draw.circle(surf, (80, 80, 80), left_knee, leg_width // 3)
            pygame.draw.rect(
                surf, (40, 40, 40), (left_leg_end[0] - 5, left_leg_end[1] - 3, 10, 6)
            )

            right_knee = (right_hip[0] + 2, right_hip[1] + leg_length // 2)
            right_leg_end = (right_hip[0] + 4, right_hip[1] + leg_length + hum_offset)
            pygame.draw.line(surf, color, right_hip, right_knee, leg_width)
            pygame.draw.line(surf, color, right_knee, right_leg_end, leg_width)
            pygame.draw.circle(surf, (80, 80, 80), right_hip, leg_width // 2 + 1)
            pygame.draw.circle(surf, (80, 80, 80), right_knee, leg_width // 3)
            pygame.draw.rect(
                surf, (40, 40, 40), (right_leg_end[0] - 5, right_leg_end[1] - 3, 10, 6)
            )

        return surf

    def _create_blaster_sprite(self):
        """Create a blaster weapon sprite with Star Wars styling."""
        surf = pygame.Surface((30, 8), pygame.SRCALPHA)

        # Barrel (more futuristic look)
        pygame.draw.rect(surf, (80, 80, 120), (0, 2, 25, 4))

        # Energy chamber
        pygame.draw.rect(surf, (100, 100, 200), (20, 0, 10, 8))

        # Trigger guard (sleeker)
        pygame.draw.rect(surf, (80, 80, 120), (15, 3, 8, 2))

        # Energy glow effect
        pygame.draw.rect(surf, (150, 150, 255), (1, 3, 2, 2))

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

    def get_sprite(self, name, pose=None, frame=0):
        """Get a sprite or animation frame by name, pose, and frame index."""
        # For animated sprites
        if pose is not None:
            key = f"{name}_{pose}"
            if key in self.animated_sprites:
                frames = self.animated_sprites[key]
                return frames[frame % len(frames)]
        # For static sprites
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

    def _create_jedi_sprite(self, size, pose="idle", frame=0, facing_right=True):
        """Create a Jedi sprite with lightsaber and robes."""
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        # Jedi body proportions
        head_radius = size // 7
        torso_width = size // 2.8
        torso_height = size // 2.2

        # Jedi head with hood
        head_center = (size // 2, head_radius + 3)
        pygame.draw.circle(
            surf, (139, 69, 19), head_center, head_radius + 3
        )  # Brown hood
        pygame.draw.circle(surf, (220, 180, 140), head_center, head_radius - 1)  # Face

        # Eyes (wise Jedi eyes)
        eye_y = head_radius - 1
        if facing_right:
            pygame.draw.ellipse(surf, (255, 255, 255), (size // 2 - 4, eye_y, 5, 3))
            pygame.draw.ellipse(surf, (255, 255, 255), (size // 2 + 3, eye_y, 5, 3))
            pygame.draw.circle(
                surf, (50, 150, 200), (size // 2 - 1, eye_y + 1), 1
            )  # Blue eyes
            pygame.draw.circle(surf, (50, 150, 200), (size // 2 + 6, eye_y + 1), 1)
        else:
            pygame.draw.ellipse(surf, (255, 255, 255), (size // 2 - 7, eye_y, 5, 3))
            pygame.draw.ellipse(surf, (255, 255, 255), (size // 2, eye_y, 5, 3))
            pygame.draw.circle(surf, (50, 150, 200), (size // 2 - 6, eye_y + 1), 1)
            pygame.draw.circle(surf, (50, 150, 200), (size // 2 + 1, eye_y + 1), 1)

        # Jedi robe (tan/brown)
        torso_rect = pygame.Rect(
            size // 2 - torso_width // 2,
            head_radius * 2 + 5,
            torso_width,
            torso_height,
        )
        pygame.draw.rect(surf, (160, 130, 90), torso_rect)  # Tan robe
        pygame.draw.rect(surf, (120, 90, 60), torso_rect, 2)  # Darker outline

        # Jedi belt
        belt_y = torso_rect.centery
        pygame.draw.rect(surf, (101, 67, 33), (torso_rect.left, belt_y, torso_width, 3))

        # Arms with Jedi sleeves
        arm_width = size // 8
        arm_length = size // 3
        shoulder_y = head_radius * 2 + 8

        left_arm = pygame.Rect(
            size // 2 - torso_width // 2 - arm_width, shoulder_y, arm_width, arm_length
        )
        right_arm = pygame.Rect(
            size // 2 + torso_width // 2, shoulder_y, arm_width, arm_length
        )

        pygame.draw.rect(surf, (160, 130, 90), left_arm)  # Tan robe sleeves
        pygame.draw.rect(surf, (160, 130, 90), right_arm)

        # Hands
        pygame.draw.circle(
            surf, (220, 180, 140), (left_arm.centerx, left_arm.bottom), 3
        )
        pygame.draw.circle(
            surf, (220, 180, 140), (right_arm.centerx, right_arm.bottom), 3
        )

        # LIGHTSABER! (Blue blade)
        if facing_right:
            saber_x = right_arm.centerx + 2
        else:
            saber_x = left_arm.centerx - 2

        saber_y = right_arm.bottom
        # Lightsaber hilt
        pygame.draw.rect(surf, (150, 150, 150), (saber_x - 1, saber_y, 3, 8))
        # Blue lightsaber blade
        pygame.draw.rect(surf, (100, 150, 255), (saber_x, saber_y - 15, 1, 15))
        pygame.draw.rect(
            surf, (150, 200, 255), (saber_x - 1, saber_y - 15, 3, 15), 1
        )  # Glow

        # Much longer legs for taller figure
        leg_width = size // 10
        leg_length = size // 1.3  # Much taller legs
        legs_start_y = torso_rect.bottom

        left_leg = pygame.Rect(
            size // 2 - leg_width - 2, legs_start_y, leg_width, leg_length
        )
        right_leg = pygame.Rect(size // 2 + 2, legs_start_y, leg_width, leg_length)

        pygame.draw.rect(surf, (160, 130, 90), left_leg)  # Tan robe legs
        pygame.draw.rect(surf, (160, 130, 90), right_leg)

        # Jedi boots
        pygame.draw.rect(
            surf, (101, 67, 33), (left_leg.left, left_leg.bottom - 5, leg_width, 5)
        )
        pygame.draw.rect(
            surf, (101, 67, 33), (right_leg.left, right_leg.bottom - 5, leg_width, 5)
        )

        return surf

    def _create_sith_sprite(self, size, pose="idle", frame=0, facing_right=True):
        """Create a Sith Lord sprite with red lightsaber and dark robes."""
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        # Sith body proportions
        head_radius = size // 7
        torso_width = size // 2.8
        torso_height = size // 2.2

        # Sith head with dark hood
        head_center = (size // 2, head_radius + 3)
        pygame.draw.circle(
            surf, (30, 30, 30), head_center, head_radius + 3
        )  # Black hood
        pygame.draw.circle(
            surf, (200, 160, 120), head_center, head_radius - 1
        )  # Pale face

        # Eyes (menacing Sith eyes)
        eye_y = head_radius - 1
        if facing_right:
            pygame.draw.ellipse(surf, (255, 255, 255), (size // 2 - 4, eye_y, 5, 3))
            pygame.draw.ellipse(surf, (255, 255, 255), (size // 2 + 3, eye_y, 5, 3))
            pygame.draw.circle(
                surf, (255, 200, 0), (size // 2 - 1, eye_y + 1), 1
            )  # Yellow Sith eyes
            pygame.draw.circle(surf, (255, 200, 0), (size // 2 + 6, eye_y + 1), 1)
        else:
            pygame.draw.ellipse(surf, (255, 255, 255), (size // 2 - 7, eye_y, 5, 3))
            pygame.draw.ellipse(surf, (255, 255, 255), (size // 2, eye_y, 5, 3))
            pygame.draw.circle(surf, (255, 200, 0), (size // 2 - 6, eye_y + 1), 1)
            pygame.draw.circle(surf, (255, 200, 0), (size // 2 + 1, eye_y + 1), 1)

        # Dark Sith robe
        torso_rect = pygame.Rect(
            size // 2 - torso_width // 2,
            head_radius * 2 + 5,
            torso_width,
            torso_height,
        )
        pygame.draw.rect(surf, (40, 40, 40), torso_rect)  # Dark robe
        pygame.draw.rect(surf, (20, 20, 20), torso_rect, 2)  # Darker outline

        # Sith belt
        belt_y = torso_rect.centery
        pygame.draw.rect(surf, (60, 60, 60), (torso_rect.left, belt_y, torso_width, 3))

        # Arms with dark sleeves
        arm_width = size // 8
        arm_length = size // 3
        shoulder_y = head_radius * 2 + 8

        left_arm = pygame.Rect(
            size // 2 - torso_width // 2 - arm_width, shoulder_y, arm_width, arm_length
        )
        right_arm = pygame.Rect(
            size // 2 + torso_width // 2, shoulder_y, arm_width, arm_length
        )

        pygame.draw.rect(surf, (40, 40, 40), left_arm)  # Dark robe sleeves
        pygame.draw.rect(surf, (40, 40, 40), right_arm)

        # Hands
        pygame.draw.circle(
            surf, (200, 160, 120), (left_arm.centerx, left_arm.bottom), 3
        )
        pygame.draw.circle(
            surf, (200, 160, 120), (right_arm.centerx, right_arm.bottom), 3
        )

        # RED LIGHTSABER! (Sith weapon)
        if facing_right:
            saber_x = right_arm.centerx + 2
        else:
            saber_x = left_arm.centerx - 2

        saber_y = right_arm.bottom
        # Lightsaber hilt (more angular/menacing)
        pygame.draw.rect(surf, (80, 80, 80), (saber_x - 1, saber_y, 3, 8))
        # Red lightsaber blade
        pygame.draw.rect(surf, (255, 50, 50), (saber_x, saber_y - 15, 1, 15))
        pygame.draw.rect(
            surf, (255, 100, 100), (saber_x - 1, saber_y - 15, 3, 15), 1
        )  # Red glow

        # Much longer legs for taller figure
        leg_width = size // 10
        leg_length = size // 1.3  # Much taller legs
        legs_start_y = torso_rect.bottom

        left_leg = pygame.Rect(
            size // 2 - leg_width - 2, legs_start_y, leg_width, leg_length
        )
        right_leg = pygame.Rect(size // 2 + 2, legs_start_y, leg_width, leg_length)

        pygame.draw.rect(surf, (40, 40, 40), left_leg)  # Dark robe legs
        pygame.draw.rect(surf, (40, 40, 40), right_leg)

        # Dark boots
        pygame.draw.rect(
            surf, (20, 20, 20), (left_leg.left, left_leg.bottom - 5, leg_width, 5)
        )
        pygame.draw.rect(
            surf, (20, 20, 20), (right_leg.left, right_leg.bottom - 5, leg_width, 5)
        )

        return surf

    def get_character_sprite(
        self, character_type, size, pose="idle", frame=0, facing_right=True
    ):
        """Get a sprite based on character type (jedi, sith, or soldier)."""
        if character_type == "jedi":
            return self._create_jedi_sprite(size, pose, frame, facing_right)
        elif character_type == "sith":
            return self._create_sith_sprite(size, pose, frame, facing_right)
        else:
            # Default to soldier
            return self._create_player_sprite(
                size, PLAYER_COLOR, pose, frame, facing_right
            )


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
        """Start or switch an animation for an entity."""
        if animation_name in self.animations:
            self.animation_states[entity_id] = {
                "animation": animation_name,
                "current_frame": 0,
                "frame_timer": 0,
            }

    def update_animations(self):
        """Update all active animations for all entities."""
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

    def set_animation_state(self, entity_id, animation_name):
        """Switch to a new animation state for an entity, resetting frame if changed."""
        if (
            entity_id not in self.animation_states
            or self.animation_states[entity_id]["animation"] != animation_name
        ):
            self.start_animation(entity_id, animation_name)


# Global instances
sprite_manager = SpriteManager()
animation_manager = AnimationManager()
