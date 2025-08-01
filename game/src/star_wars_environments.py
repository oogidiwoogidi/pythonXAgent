"""
Epic Star Wars Environments

Iconic locations from the Star Wars universe with unique visual effects,
hazards, and environmental interactions.
"""

import pygame
import random
import math
from config import *


class Environment:
    """Base class for Star Wars environments."""

    def __init__(self, name, background_color, special_effects=None):
        self.name = name
        self.background_color = background_color
        self.special_effects = special_effects or []
        self.particles = []
        self.environmental_hazards = []

    def update(self):
        """Update environment effects."""
        # Update particles
        self.particles = [p for p in self.particles if self._update_particle(p)]

        # Update hazards
        for hazard in self.environmental_hazards:
            hazard.update()

    def _update_particle(self, particle):
        """Update individual particle."""
        particle["x"] += particle.get("dx", 0)
        particle["y"] += particle.get("dy", 0)
        particle["life"] -= 1
        return particle["life"] > 0

    def add_particle(self, x, y, dx, dy, color, life):
        """Add environmental particle."""
        self.particles.append(
            {"x": x, "y": y, "dx": dx, "dy": dy, "color": color, "life": life}
        )

    def draw_background(self, surface):
        """Draw environment background."""
        surface.fill(self.background_color)
        self._draw_specific_background(surface)

    def _draw_specific_background(self, surface):
        """Override in subclasses for specific background elements."""
        pass

    def draw_effects(self, surface):
        """Draw environmental effects."""
        self._draw_particles(surface)
        self._draw_hazards(surface)

    def _draw_particles(self, surface):
        """Draw environment particles."""
        for particle in self.particles:
            alpha = min(255, particle["life"] * 3)
            if alpha > 0:
                temp_surf = pygame.Surface((4, 4), pygame.SRCALPHA)
                pygame.draw.circle(temp_surf, (*particle["color"], alpha), (2, 2), 2)
                surface.blit(temp_surf, (particle["x"] - 2, particle["y"] - 2))

    def _draw_hazards(self, surface):
        """Draw environmental hazards."""
        for hazard in self.environmental_hazards:
            hazard.draw(surface)


class DeathStarEnvironment(Environment):
    """Death Star interior environment."""

    def __init__(self):
        super().__init__("Death Star", (40, 40, 50))
        self.reactor_core_glow = 0
        self.panel_lights = []

        # Initialize control panel lights
        for _ in range(20):
            self.panel_lights.append(
                {
                    "x": random.randint(50, WINDOW_WIDTH - 50),
                    "y": random.randint(50, WINDOW_HEIGHT - 50),
                    "color": random.choice([(0, 255, 0), (255, 0, 0), (0, 0, 255)]),
                    "blink_timer": random.randint(0, 120),
                }
            )

    def update(self):
        super().update()
        self.reactor_core_glow = (self.reactor_core_glow + 2) % 360

        # Update panel lights
        for light in self.panel_lights:
            light["blink_timer"] = (light["blink_timer"] + 1) % 120

    def _draw_specific_background(self, surface):
        """Draw Death Star interior."""
        # Draw metallic walls
        for i in range(0, WINDOW_WIDTH, 100):
            pygame.draw.line(surface, (80, 80, 90), (i, 0), (i, WINDOW_HEIGHT), 2)
        for i in range(0, WINDOW_HEIGHT, 100):
            pygame.draw.line(surface, (80, 80, 90), (0, i), (WINDOW_WIDTH, i), 2)

        # Draw reactor core glow
        glow_intensity = abs(math.sin(self.reactor_core_glow * 0.05)) * 100 + 50
        core_center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT + 100)

        for radius in range(200, 50, -20):
            alpha = max(0, glow_intensity - radius)
            if alpha > 0:
                temp_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    temp_surf,
                    (255, 100, 100, int(alpha // 4)),
                    (radius, radius),
                    radius,
                )
                surface.blit(
                    temp_surf, (core_center[0] - radius, core_center[1] - radius)
                )

        # Draw control panel lights
        for light in self.panel_lights:
            if light["blink_timer"] < 60:
                pygame.draw.circle(surface, light["color"], (light["x"], light["y"]), 3)


class TatooineEnvironment(Environment):
    """Tatooine desert environment."""

    def __init__(self):
        super().__init__("Tatooine", (194, 154, 108))
        self.sand_particles = []
        self.twin_suns_angle = 0

        # Add initial sand particles
        for _ in range(50):
            self.add_sand_particle()

    def add_sand_particle(self):
        """Add blowing sand particle."""
        self.particles.append(
            {
                "x": -10,
                "y": random.randint(0, WINDOW_HEIGHT),
                "dx": random.uniform(1, 3),
                "dy": random.uniform(-0.5, 0.5),
                "color": (218, 165, 120),
                "life": random.randint(200, 400),
            }
        )

    def update(self):
        super().update()
        self.twin_suns_angle += 0.01

        # Add new sand particles
        if random.randint(1, 10) == 1:
            self.add_sand_particle()

    def _draw_specific_background(self, surface):
        """Draw Tatooine landscape."""
        # Draw twin suns
        sun1_x = WINDOW_WIDTH - 80 + math.cos(self.twin_suns_angle) * 20
        sun1_y = 60 + math.sin(self.twin_suns_angle) * 10
        sun2_x = WINDOW_WIDTH - 50 + math.cos(self.twin_suns_angle + 0.5) * 15
        sun2_y = 80 + math.sin(self.twin_suns_angle + 0.5) * 8

        # Draw sun glows
        for sun_x, sun_y, color in [
            (sun1_x, sun1_y, (255, 255, 150)),
            (sun2_x, sun2_y, (255, 200, 100)),
        ]:
            for radius in range(30, 10, -5):
                alpha = 150 - radius * 3
                temp_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(temp_surf, (*color, alpha), (radius, radius), radius)
                surface.blit(temp_surf, (sun_x - radius, sun_y - radius))

        # Draw sand dunes
        dune_points = []
        for i in range(0, WINDOW_WIDTH + 50, 50):
            height = 300 + math.sin(i * 0.01 + self.twin_suns_angle * 10) * 30
            dune_points.append((i, height))
        dune_points.append((WINDOW_WIDTH, WINDOW_HEIGHT))
        dune_points.append((0, WINDOW_HEIGHT))

        pygame.draw.polygon(surface, (180, 140, 95), dune_points)


class EndorEnvironment(Environment):
    """Endor forest environment."""

    def __init__(self):
        super().__init__("Endor", (34, 80, 34))
        self.trees = []
        self.forest_sounds = 0

        # Generate forest
        for _ in range(15):
            self.trees.append(
                {
                    "x": random.randint(0, WINDOW_WIDTH),
                    "y": random.randint(WINDOW_HEIGHT // 2, WINDOW_HEIGHT),
                    "height": random.randint(100, 200),
                    "width": random.randint(20, 40),
                }
            )

    def update(self):
        super().update()

        # Add forest ambiance particles (leaves, spores)
        if random.randint(1, 30) == 1:
            self.add_particle(
                random.randint(0, WINDOW_WIDTH),
                random.randint(0, WINDOW_HEIGHT // 2),
                random.uniform(-1, 1),
                random.uniform(0.5, 2),
                random.choice([(100, 150, 50), (120, 180, 60), (80, 120, 40)]),
                random.randint(120, 300),
            )

    def _draw_specific_background(self, surface):
        """Draw Endor forest."""
        # Draw distant forest background
        for layer in range(3):
            tree_color = (20 + layer * 15, 60 + layer * 20, 20 + layer * 15)
            for i in range(0, WINDOW_WIDTH, 30):
                tree_height = 80 + layer * 40 + random.randint(-20, 20)
                tree_y = WINDOW_HEIGHT - tree_height + layer * 50
                pygame.draw.rect(surface, tree_color, (i, tree_y, 20, tree_height))

        # Draw main trees
        for tree in self.trees:
            # Tree trunk
            trunk_color = (101, 67, 33)
            pygame.draw.rect(
                surface,
                trunk_color,
                (tree["x"] - 5, tree["y"] - tree["height"], 10, tree["height"]),
            )

            # Tree canopy
            canopy_color = (50, 120, 50)
            pygame.draw.circle(
                surface,
                canopy_color,
                (tree["x"], tree["y"] - tree["height"] + 20),
                tree["width"],
            )


class HothEnvironment(Environment):
    """Hoth ice planet environment."""

    def __init__(self):
        super().__init__("Hoth", (240, 248, 255))
        self.snow_particles = []
        self.wind_direction = 0

        # Add initial snow
        for _ in range(100):
            self.add_snowflake()

    def add_snowflake(self):
        """Add falling snowflake."""
        self.particles.append(
            {
                "x": random.randint(-50, WINDOW_WIDTH + 50),
                "y": -10,
                "dx": random.uniform(-1, 1),
                "dy": random.uniform(1, 3),
                "color": (255, 255, 255),
                "life": random.randint(200, 500),
            }
        )

    def update(self):
        super().update()
        self.wind_direction += 0.02

        # Add new snowflakes
        if random.randint(1, 5) == 1:
            self.add_snowflake()

        # Update existing snow with wind
        for particle in self.particles:
            particle["dx"] += math.sin(self.wind_direction) * 0.1

    def _draw_specific_background(self, surface):
        """Draw Hoth landscape."""
        # Draw ice formations
        ice_color = (200, 220, 240)
        for i in range(0, WINDOW_WIDTH, 80):
            height = 100 + math.sin(i * 0.02) * 30
            pygame.draw.polygon(
                surface,
                ice_color,
                [
                    (i, WINDOW_HEIGHT),
                    (i + 40, WINDOW_HEIGHT - height),
                    (i + 80, WINDOW_HEIGHT),
                ],
            )

        # Draw blizzard effect
        if random.randint(1, 20) == 1:
            for _ in range(10):
                self.add_particle(
                    random.randint(0, WINDOW_WIDTH),
                    random.randint(0, WINDOW_HEIGHT),
                    random.uniform(-3, 3),
                    random.uniform(-1, 1),
                    (255, 255, 255),
                    30,
                )


# Environment registry
ENVIRONMENTS = {
    "death_star": DeathStarEnvironment,
    "tatooine": TatooineEnvironment,
    "endor": EndorEnvironment,
    "hoth": HothEnvironment,
}


def create_environment(env_name):
    """Create environment by name."""
    env_class = ENVIRONMENTS.get(env_name)
    return env_class() if env_class else Environment("Default", WHITE)


def get_random_environment():
    """Get a random environment."""
    env_name = random.choice(list(ENVIRONMENTS.keys()))
    return create_environment(env_name)


class EnvironmentManager:
    """Manages Star Wars environments and their effects."""

    def __init__(self):
        self.current_environment = None
        self.environments = ENVIRONMENTS

    def set_environment(self, env_name):
        """Set the current environment."""
        if env_name in self.environments:
            self.current_environment = create_environment(env_name)

    def update(self):
        """Update current environment."""
        if self.current_environment:
            self.current_environment.update()

    def draw_environment(self, surface, env_name=None):
        """Draw the specified environment or current one."""
        if env_name:
            env = create_environment(env_name)
            env.draw_background(surface)
            env.draw_effects(surface)
        elif self.current_environment:
            self.current_environment.draw_background(surface)
            self.current_environment.draw_effects(surface)
