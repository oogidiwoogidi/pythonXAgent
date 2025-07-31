"""
Enhanced UI and Background System - Visual Mod Pack

This module provides enhanced UI elements, animated backgrounds,
and improved visual feedback systems.
"""

import pygame
import math
import random
from config import *


class BackgroundManager:
    """Manages animated backgrounds and environmental effects."""

    def __init__(self):
        self.stars = []
        self.clouds = []
        self.particles = []
        self.scroll_offset = 0
        self._generate_stars()
        self._generate_clouds()

    def _generate_stars(self):
        """Generate animated stars for space background."""
        for _ in range(100):
            star = {
                "x": random.randint(0, WINDOW_WIDTH),
                "y": random.randint(0, WINDOW_HEIGHT),
                "brightness": random.randint(100, 255),
                "twinkle_speed": random.uniform(0.02, 0.1),
                "size": random.randint(1, 3),
            }
            self.stars.append(star)

    def _generate_clouds(self):
        """Generate floating cloud particles."""
        for _ in range(20):
            cloud = {
                "x": random.randint(-50, WINDOW_WIDTH + 50),
                "y": random.randint(0, WINDOW_HEIGHT // 2),
                "speed": random.uniform(0.2, 0.8),
                "size": random.randint(30, 80),
                "alpha": random.randint(30, 80),
            }
            self.clouds.append(cloud)

    def update(self):
        """Update background animations."""
        # Update star twinkling
        for star in self.stars:
            star["brightness"] += (
                math.sin(pygame.time.get_ticks() * star["twinkle_speed"]) * 2
            )
            star["brightness"] = max(50, min(255, star["brightness"]))

        # Update clouds
        for cloud in self.clouds:
            cloud["x"] += cloud["speed"]
            if cloud["x"] > WINDOW_WIDTH + 100:
                cloud["x"] = -100
                cloud["y"] = random.randint(0, WINDOW_HEIGHT // 2)

    def draw_space_background(self, screen):
        """Draw animated space background."""
        # Dark space background with gradient
        for y in range(WINDOW_HEIGHT):
            intensity = int(20 + (y / WINDOW_HEIGHT) * 40)
            color = (intensity // 3, intensity // 4, intensity)
            pygame.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y))

        # Draw twinkling stars
        for star in self.stars:
            color = (
                int(star["brightness"]),
                int(star["brightness"]),
                int(star["brightness"] * 0.9),
            )
            if star["size"] == 1:
                screen.set_at((int(star["x"]), int(star["y"])), color)
            else:
                pygame.draw.circle(
                    screen, color, (int(star["x"]), int(star["y"])), star["size"]
                )

    def draw_city_background(self, screen):
        """Draw animated city background."""
        # Sky gradient
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            r = int(135 * (1 - ratio) + 25 * ratio)
            g = int(206 * (1 - ratio) + 25 * ratio)
            b = int(235 * (1 - ratio) + 112 * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

        # Draw clouds
        for cloud in self.clouds:
            cloud_surf = pygame.Surface(
                (cloud["size"], cloud["size"] // 2), pygame.SRCALPHA
            )
            cloud_color = (255, 255, 255, cloud["alpha"])

            # Draw cloud shape (multiple circles)
            for i in range(3):
                circle_x = i * cloud["size"] // 3
                circle_y = cloud["size"] // 4
                radius = cloud["size"] // 4 + random.randint(-5, 5)
                pygame.draw.circle(
                    cloud_surf, cloud_color, (circle_x, circle_y), radius
                )

            screen.blit(cloud_surf, (cloud["x"], cloud["y"]))

        # City silhouette
        building_heights = [200, 150, 300, 180, 250, 120, 280, 160]
        building_width = WINDOW_WIDTH // len(building_heights)

        for i, height in enumerate(building_heights):
            x = i * building_width
            y = WINDOW_HEIGHT - height

            # Building body
            pygame.draw.rect(screen, (30, 30, 30), (x, y, building_width, height))

            # Building windows
            for window_y in range(y + 20, WINDOW_HEIGHT - 20, 25):
                for window_x in range(x + 10, x + building_width - 10, 20):
                    if random.random() > 0.3:  # Some windows are lit
                        window_color = (
                            (255, 255, 100)
                            if random.random() > 0.7
                            else (100, 100, 150)
                        )
                        pygame.draw.rect(
                            screen, window_color, (window_x, window_y, 8, 12)
                        )


class EnhancedUI:
    """Enhanced UI elements with animations and effects."""

    def __init__(self):
        self.crosshair_rotation = 0
        self.damage_indicators = []
        self.floating_text = []

    def add_damage_indicator(self, x, y, damage, color=RED):
        """Add floating damage number."""
        indicator = {
            "x": x,
            "y": y,
            "damage": int(damage),
            "color": color,
            "life": 60,
            "velocity_y": -2,
            "scale": 1.0,
        }
        self.damage_indicators.append(indicator)

    def add_floating_text(self, x, y, text, color=WHITE, size=24):
        """Add floating text effect."""
        text_obj = {
            "x": x,
            "y": y,
            "text": text,
            "color": color,
            "size": size,
            "life": 90,
            "velocity_y": -1,
            "alpha": 255,
        }
        self.floating_text.append(text_obj)

    def update(self):
        """Update UI animations."""
        self.crosshair_rotation += 1

        # Update damage indicators
        for indicator in self.damage_indicators[:]:
            indicator["y"] += indicator["velocity_y"]
            indicator["life"] -= 1
            indicator["scale"] = max(0.5, indicator["scale"] - 0.01)

            if indicator["life"] <= 0:
                self.damage_indicators.remove(indicator)

        # Update floating text
        for text_obj in self.floating_text[:]:
            text_obj["y"] += text_obj["velocity_y"]
            text_obj["life"] -= 1
            text_obj["alpha"] = max(0, int(255 * (text_obj["life"] / 90)))

            if text_obj["life"] <= 0:
                self.floating_text.remove(text_obj)

    def draw_enhanced_crosshair(self, screen, x, y):
        """Draw animated crosshair."""
        # Rotating outer ring
        ring_radius = 15
        for i in range(8):
            angle = (self.crosshair_rotation + i * 45) * math.pi / 180
            start_x = x + math.cos(angle) * (ring_radius - 3)
            start_y = y + math.sin(angle) * (ring_radius - 3)
            end_x = x + math.cos(angle) * ring_radius
            end_y = y + math.sin(angle) * ring_radius
            pygame.draw.line(screen, WHITE, (start_x, start_y), (end_x, end_y), 2)

        # Inner crosshair
        pygame.draw.line(screen, RED, (x - 8, y), (x - 3, y), 2)
        pygame.draw.line(screen, RED, (x + 3, y), (x + 8, y), 2)
        pygame.draw.line(screen, RED, (x, y - 8), (x, y - 3), 2)
        pygame.draw.line(screen, RED, (x, y + 3), (x, y + 8), 2)

        # Center dot
        pygame.draw.circle(screen, RED, (x, y), 1)

    def draw_weapon_hud(self, screen, weapon_type, ammo, max_ammo, x, y):
        """Draw enhanced weapon HUD."""
        font = pygame.font.Font(None, 24)

        # Weapon background
        hud_rect = pygame.Rect(x, y, 150, 60)
        pygame.draw.rect(screen, (0, 0, 0, 150), hud_rect)
        pygame.draw.rect(screen, WHITE, hud_rect, 2)

        # Weapon name
        weapon_text = font.render(weapon_type.upper(), True, WHITE)
        screen.blit(weapon_text, (x + 10, y + 5))

        # Ammo counter
        ammo_text = font.render(f"{ammo}/{max_ammo}", True, WHITE)
        screen.blit(ammo_text, (x + 10, y + 30))

        # Ammo bar
        bar_width = 120
        bar_height = 8
        bar_x = x + 10
        bar_y = y + 50

        # Background
        pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))

        # Ammo fill
        if max_ammo > 0:
            fill_width = int(bar_width * (ammo / max_ammo))
            fill_color = (
                GREEN if ammo > max_ammo * 0.3 else (ORANGE if ammo > 0 else RED)
            )
            pygame.draw.rect(screen, fill_color, (bar_x, bar_y, fill_width, bar_height))

        # Border
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)

    def draw_damage_indicators(self, screen):
        """Draw floating damage numbers."""
        for indicator in self.damage_indicators:
            font_size = int(24 * indicator["scale"])
            font = pygame.font.Font(None, font_size)

            # Create text with outline
            text = str(indicator["damage"])

            # Outline
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                outline_surf = font.render(text, True, BLACK)
                screen.blit(outline_surf, (indicator["x"] + dx, indicator["y"] + dy))

            # Main text
            text_surf = font.render(text, True, indicator["color"])
            screen.blit(text_surf, (indicator["x"], indicator["y"]))

    def draw_floating_text(self, screen):
        """Draw floating text effects."""
        for text_obj in self.floating_text:
            font = pygame.font.Font(None, text_obj["size"])

            # Create surface with alpha
            text_surf = font.render(text_obj["text"], True, text_obj["color"])
            alpha_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
            alpha_surf.set_alpha(text_obj["alpha"])
            alpha_surf.blit(text_surf, (0, 0))

            screen.blit(alpha_surf, (text_obj["x"], text_obj["y"]))

    def draw_mini_map(self, screen, players, enemies, platforms):
        """Draw a mini-map in the corner."""
        map_size = 120
        map_x = WINDOW_WIDTH - map_size - 10
        map_y = 10

        # Map background
        map_surf = pygame.Surface((map_size, map_size), pygame.SRCALPHA)
        pygame.draw.rect(map_surf, (0, 0, 0, 150), (0, 0, map_size, map_size))
        pygame.draw.rect(map_surf, WHITE, (0, 0, map_size, map_size), 2)

        # Scale factor
        scale_x = map_size / WINDOW_WIDTH
        scale_y = map_size / WINDOW_HEIGHT

        # Draw platforms
        for platform in platforms:
            scaled_x = int(platform.x * scale_x)
            scaled_y = int(platform.y * scale_y)
            scaled_w = max(2, int(platform.width * scale_x))
            scaled_h = max(2, int(platform.height * scale_y))
            pygame.draw.rect(map_surf, GRAY, (scaled_x, scaled_y, scaled_w, scaled_h))

        # Draw players
        for player in players:
            scaled_x = int(player.x * scale_x)
            scaled_y = int(player.y * scale_y)
            pygame.draw.circle(map_surf, GREEN, (scaled_x, scaled_y), 3)

        # Draw enemies
        for enemy in enemies:
            scaled_x = int(enemy.x * scale_x)
            scaled_y = int(enemy.y * scale_y)
            pygame.draw.circle(map_surf, RED, (scaled_x, scaled_y), 2)

        screen.blit(map_surf, (map_x, map_y))


# Global instances
background_manager = BackgroundManager()
enhanced_ui = EnhancedUI()
