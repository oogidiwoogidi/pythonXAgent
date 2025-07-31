"""
Visual Effects System - Mod Pack for Enhanced Graphics

This module provides visual enhancements including particle effects,
animations, screen effects, and improved rendering for the game.
"""

import pygame
import math
import random
from config import *


class Particle:
    """Individual particle for effects."""

    def __init__(self, x, y, velocity_x, velocity_y, color, life, size=2):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity = 0.2

    def update(self):
        """Update particle position and life."""
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += self.gravity
        self.life -= 1

        # Fade out particle
        alpha = int(255 * (self.life / self.max_life))
        if len(self.color) == 3:
            self.color = (*self.color, alpha)

    def draw(self, screen):
        """Draw the particle with alpha blending."""
        if self.life > 0:
            # Create a surface for alpha blending
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            alpha = int(255 * (self.life / self.max_life))
            color_with_alpha = (*self.color[:3], alpha)
            pygame.draw.circle(
                surf, color_with_alpha, (self.size, self.size), self.size
            )
            screen.blit(surf, (self.x - self.size, self.y - self.size))


class ParticleSystem:
    """Manages all particle effects in the game."""

    def __init__(self):
        self.particles = []

    def add_explosion(self, x, y, color=(255, 100, 0), count=15):
        """Add explosion particle effect."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            life = random.randint(20, 40)
            size = random.randint(2, 4)
            self.particles.append(
                Particle(x, y, velocity_x, velocity_y, color, life, size)
            )

    def add_bullet_trail(self, x, y, velocity_x, velocity_y, color=(255, 255, 100)):
        """Add bullet trail effect."""
        for _ in range(3):
            offset_x = random.uniform(-2, 2)
            offset_y = random.uniform(-2, 2)
            trail_velocity_x = velocity_x * 0.3 + random.uniform(-1, 1)
            trail_velocity_y = velocity_y * 0.3 + random.uniform(-1, 1)
            life = random.randint(5, 15)
            self.particles.append(
                Particle(
                    x + offset_x,
                    y + offset_y,
                    trail_velocity_x,
                    trail_velocity_y,
                    color,
                    life,
                    1,
                )
            )

    def add_muzzle_flash(self, x, y, direction, color=(255, 255, 150)):
        """Add muzzle flash effect."""
        for _ in range(8):
            angle = direction + random.uniform(-0.5, 0.5)
            speed = random.uniform(3, 6)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            life = random.randint(8, 15)
            size = random.randint(1, 3)
            self.particles.append(
                Particle(x, y, velocity_x, velocity_y, color, life, size)
            )

    def add_blood_splatter(self, x, y, color=(150, 0, 0)):
        """Add blood splatter effect."""
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed - 2  # Upward bias
            life = random.randint(15, 30)
            size = random.randint(1, 2)
            self.particles.append(
                Particle(x, y, velocity_x, velocity_y, color, life, size)
            )

    def add_jump_dust(self, x, y, color=(200, 180, 120)):
        """Add dust effect when jumping/landing."""
        for _ in range(6):
            velocity_x = random.uniform(-3, 3)
            velocity_y = random.uniform(-2, 0)
            life = random.randint(10, 20)
            size = random.randint(1, 2)
            self.particles.append(
                Particle(x, y, velocity_x, velocity_y, color, life, size)
            )

    def update(self):
        """Update all particles and remove dead ones."""
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update()

    def draw(self, screen):
        """Draw all particles."""
        for particle in self.particles:
            particle.draw(screen)


class ScreenEffects:
    """Screen-wide visual effects like screen shake, flash, etc."""

    def __init__(self):
        self.shake_intensity = 0
        self.shake_duration = 0
        self.flash_intensity = 0
        self.flash_duration = 0
        self.flash_color = WHITE

    def add_screen_shake(self, intensity=5, duration=10):
        """Add screen shake effect."""
        self.shake_intensity = max(self.shake_intensity, intensity)
        self.shake_duration = max(self.shake_duration, duration)

    def add_screen_flash(self, color=WHITE, intensity=100, duration=5):
        """Add screen flash effect."""
        self.flash_color = color
        self.flash_intensity = max(self.flash_intensity, intensity)
        self.flash_duration = max(self.flash_duration, duration)

    def get_screen_offset(self):
        """Get current screen shake offset."""
        if self.shake_duration > 0:
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            return offset_x, offset_y
        return 0, 0

    def update(self):
        """Update screen effects."""
        if self.shake_duration > 0:
            self.shake_duration -= 1
            if self.shake_duration <= 0:
                self.shake_intensity = 0

        if self.flash_duration > 0:
            self.flash_duration -= 1
            self.flash_intensity = max(0, self.flash_intensity - 20)

    def draw_flash(self, screen):
        """Draw screen flash overlay."""
        if self.flash_intensity > 0:
            flash_surface = pygame.Surface(
                (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA
            )
            color_with_alpha = (*self.flash_color[:3], self.flash_intensity)
            flash_surface.fill(color_with_alpha)
            screen.blit(flash_surface, (0, 0))


class EnhancedRenderer:
    """Enhanced rendering system with gradients, shadows, and improved visuals."""

    @staticmethod
    def draw_gradient_rect(screen, rect, top_color, bottom_color):
        """Draw a rectangle with vertical gradient."""
        for i in range(rect.height):
            ratio = i / rect.height
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            pygame.draw.line(
                screen,
                (r, g, b),
                (rect.x, rect.y + i),
                (rect.x + rect.width, rect.y + i),
            )

    @staticmethod
    def draw_glowing_rect(screen, rect, color, glow_size=3):
        """Draw a rectangle with glowing effect."""
        # Draw multiple layers for glow effect
        for i in range(glow_size, 0, -1):
            alpha = 255 // (i + 1)
            glow_surf = pygame.Surface(
                (rect.width + i * 2, rect.height + i * 2), pygame.SRCALPHA
            )
            glow_color = (*color[:3], alpha)
            pygame.draw.rect(
                glow_surf, glow_color, (0, 0, rect.width + i * 2, rect.height + i * 2)
            )
            screen.blit(glow_surf, (rect.x - i, rect.y - i))

        # Draw main rectangle
        pygame.draw.rect(screen, color, rect)

    @staticmethod
    def draw_shadow_rect(
        screen, rect, color, shadow_offset=(3, 3), shadow_color=(0, 0, 0, 100)
    ):
        """Draw a rectangle with drop shadow."""
        # Draw shadow
        shadow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        shadow_surf.fill(shadow_color)
        screen.blit(shadow_surf, (rect.x + shadow_offset[0], rect.y + shadow_offset[1]))

        # Draw main rectangle
        pygame.draw.rect(screen, color, rect)

    @staticmethod
    def draw_health_bar_enhanced(screen, x, y, width, height, health, max_health):
        """Draw an enhanced health bar with gradient and glow."""
        # Background
        bg_rect = pygame.Rect(x - 2, y - 2, width + 4, height + 4)
        pygame.draw.rect(screen, BLACK, bg_rect)

        # Health bar background
        pygame.draw.rect(screen, DARK_GRAY, (x, y, width, height))

        # Health bar fill
        health_width = int(width * (health / max_health))
        if health_width > 0:
            health_rect = pygame.Rect(x, y, health_width, height)

            # Choose color based on health
            if health / max_health > 0.7:
                top_color = (0, 255, 0)
                bottom_color = (0, 200, 0)
            elif health / max_health > 0.3:
                top_color = (255, 255, 0)
                bottom_color = (255, 200, 0)
            else:
                top_color = (255, 0, 0)
                bottom_color = (200, 0, 0)

            EnhancedRenderer.draw_gradient_rect(
                screen, health_rect, top_color, bottom_color
            )

        # Border
        pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)


# Global instances for easy access
particle_system = ParticleSystem()
screen_effects = ScreenEffects()
