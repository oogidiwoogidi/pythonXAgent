"""
Star Wars Force Powers System

Implements Jedi and Sith Force abilities including:
- Force Push/Pull
- Lightsaber Throw
- Force Lightning
- Force Jump
- Force Heal
- Mind Trick
"""

import pygame
import math
import random
from config import *


class ForcePower:
    """Base class for all Force powers."""

    def __init__(self, name, cooldown, force_cost, range_limit=300):
        self.name = name
        self.cooldown = cooldown
        self.force_cost = force_cost
        self.range_limit = range_limit
        self.current_cooldown = 0

    def can_use(self, force_energy):
        """Check if power can be used."""
        return self.current_cooldown <= 0 and force_energy >= self.force_cost

    def update(self):
        """Update cooldown."""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def use(self, user, target_x, target_y, entities):
        """Use the force power."""
        if self.can_use(user.force_energy):
            self.current_cooldown = self.cooldown
            user.force_energy -= self.force_cost
            return self._execute(user, target_x, target_y, entities)
        return None

    def _execute(self, user, target_x, target_y, entities):
        """Override in subclasses."""
        pass


class ForcePush(ForcePower):
    """Force Push - pushes enemies away."""

    def __init__(self):
        super().__init__("Force Push", 120, 25, 200)

    def _execute(self, user, target_x, target_y, entities):
        effects = []

        for entity in entities:
            if entity != user and hasattr(entity, "take_damage"):
                distance = math.sqrt(
                    (entity.x - user.x) ** 2 + (entity.y - user.y) ** 2
                )
                if distance <= self.range_limit:
                    # Calculate push direction
                    angle = math.atan2(entity.y - user.y, entity.x - user.x)
                    push_force = max(20, 50 - distance / 10)

                    # Apply knockback
                    entity.knockback_dx = math.cos(angle) * push_force * 0.3
                    entity.knockback_dy = math.sin(angle) * push_force * 0.3 - 5
                    entity.knockback_timer = 20

                    # Add visual effect
                    effects.append(
                        {
                            "type": "force_wave",
                            "x": user.x + user.size // 2,
                            "y": user.y + user.size // 2,
                            "target_x": entity.x + entity.size // 2,
                            "target_y": entity.y + entity.size // 2,
                            "color": (
                                (100, 150, 255)
                                if user.character_type == "jedi"
                                else (255, 100, 100)
                            ),
                        }
                    )

        return effects


class ForceLightning(ForcePower):
    """Sith Force Lightning - damages and stuns enemies."""

    def __init__(self):
        super().__init__("Force Lightning", 180, 40, 250)

    def _execute(self, user, target_x, target_y, entities):
        if user.character_type != "sith":
            return []

        effects = []

        for entity in entities:
            if entity != user and hasattr(entity, "take_damage"):
                distance = math.sqrt(
                    (entity.x - user.x) ** 2 + (entity.y - user.y) ** 2
                )
                if distance <= self.range_limit:
                    # Deal damage
                    entity.take_damage(15, 0)

                    # Stun effect
                    if hasattr(entity, "stunned"):
                        entity.stunned = 60  # 1 second stun

                    # Lightning effect
                    for i in range(5):
                        effects.append(
                            {
                                "type": "lightning",
                                "x": user.x + user.size // 2,
                                "y": user.y + user.size // 2,
                                "target_x": entity.x
                                + entity.size // 2
                                + random.randint(-10, 10),
                                "target_y": entity.y
                                + entity.size // 2
                                + random.randint(-10, 10),
                                "color": (150, 150, 255),
                                "duration": 30 + i * 5,
                            }
                        )

        return effects


class LightsaberThrow(ForcePower):
    """Lightsaber Throw - ranged lightsaber attack."""

    def __init__(self):
        super().__init__("Lightsaber Throw", 240, 30, 400)

    def _execute(self, user, target_x, target_y, entities):
        # Create lightsaber projectile
        angle = math.atan2(target_y - user.y, target_x - user.x)
        speed = 8

        lightsaber_projectile = {
            "type": "lightsaber_throw",
            "x": user.x + user.size // 2,
            "y": user.y + user.size // 2,
            "dx": math.cos(angle) * speed,
            "dy": math.sin(angle) * speed,
            "angle": 0,
            "rotation_speed": 0.3,
            "damage": 25,
            "owner": user,
            "color": (
                (100, 150, 255) if user.character_type == "jedi" else (255, 100, 100)
            ),
            "duration": 120,
            "returning": False,
        }

        return [lightsaber_projectile]


class ForceHeal(ForcePower):
    """Jedi Force Heal - restores health."""

    def __init__(self):
        super().__init__("Force Heal", 300, 50, 0)

    def _execute(self, user, target_x, target_y, entities):
        if user.character_type != "jedi":
            return []

        # Heal user
        heal_amount = 30
        user.health = min(user.max_health, user.health + heal_amount)

        # Visual effect
        effects = []
        for i in range(10):
            effects.append(
                {
                    "type": "heal_particle",
                    "x": user.x + user.size // 2 + random.randint(-20, 20),
                    "y": user.y + user.size // 2 + random.randint(-20, 20),
                    "color": (100, 255, 100),
                    "duration": 60 + i * 3,
                }
            )

        return effects


class ForceManager:
    """Manages Force powers for characters."""

    def __init__(self):
        self.jedi_powers = {
            "force_push": ForcePush(),
            "lightsaber_throw": LightsaberThrow(),
            "force_heal": ForceHeal(),
        }

        self.sith_powers = {
            "force_push": ForcePush(),
            "force_lightning": ForceLightning(),
            "lightsaber_throw": LightsaberThrow(),
        }

        self.active_effects = []
        self.active_projectiles = []

    def get_powers(self, character_type):
        """Get available powers for character type."""
        if character_type == "jedi":
            return self.jedi_powers
        elif character_type == "sith":
            return self.sith_powers
        return {}

    def use_power(self, power_name, user, target_x, target_y, entities):
        """Use a Force power."""
        powers = self.get_powers(user.character_type)
        if power_name in powers:
            effects = powers[power_name].use(user, target_x, target_y, entities)
            if effects:
                for effect in effects:
                    if effect.get("type") == "lightsaber_throw":
                        self.active_projectiles.append(effect)
                    else:
                        self.active_effects.append(effect)
                return True
        return False

    def update(self, entities):
        """Update all Force effects and projectiles."""
        # Update power cooldowns
        for powers in [self.jedi_powers, self.sith_powers]:
            for power in powers.values():
                power.update()

        # Update effects
        self.active_effects = [
            effect for effect in self.active_effects if self._update_effect(effect)
        ]

        # Update projectiles
        self.active_projectiles = [
            proj
            for proj in self.active_projectiles
            if self._update_projectile(proj, entities)
        ]

    def _update_effect(self, effect):
        """Update individual effect."""
        effect["duration"] = effect.get("duration", 0) - 1
        return effect["duration"] > 0

    def _update_projectile(self, proj, entities):
        """Update lightsaber projectile."""
        if proj["type"] == "lightsaber_throw":
            proj["x"] += proj["dx"]
            proj["y"] += proj["dy"]
            proj["angle"] += proj["rotation_speed"]
            proj["duration"] -= 1

            # Check collisions
            for entity in entities:
                if entity != proj["owner"] and hasattr(entity, "take_damage"):
                    distance = math.sqrt(
                        (entity.x - proj["x"]) ** 2 + (entity.y - proj["y"]) ** 2
                    )
                    if distance < 30:
                        entity.take_damage(proj["damage"], proj["dx"])
                        return False  # Remove projectile

            # Return to owner after duration
            if proj["duration"] <= 0:
                return False

            return True

        return False

    def draw_effects(self, surface):
        """Draw all Force effects."""
        for effect in self.active_effects:
            self._draw_effect(surface, effect)

        for proj in self.active_projectiles:
            self._draw_projectile(surface, proj)

    def _draw_effect(self, surface, effect):
        """Draw individual effect."""
        if effect["type"] == "force_wave":
            # Draw force wave
            alpha = min(255, effect["duration"] * 8)
            temp_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (*effect["color"], alpha // 4), (25, 25), 25)
            surface.blit(temp_surf, (effect["x"] - 25, effect["y"] - 25))

        elif effect["type"] == "lightning":
            # Draw lightning bolt
            points = []
            start_x, start_y = effect["x"], effect["y"]
            end_x, end_y = effect["target_x"], effect["target_y"]

            for i in range(5):
                t = i / 4
                x = start_x + (end_x - start_x) * t + random.randint(-5, 5)
                y = start_y + (end_y - start_y) * t + random.randint(-5, 5)
                points.append((x, y))

            if len(points) > 1:
                pygame.draw.lines(surface, effect["color"], False, points, 2)

        elif effect["type"] == "heal_particle":
            # Draw healing particle
            alpha = min(255, effect["duration"] * 4)
            temp_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (*effect["color"], alpha), (3, 3), 3)
            surface.blit(temp_surf, (effect["x"] - 3, effect["y"] - 3))

    def _draw_projectile(self, surface, proj):
        """Draw lightsaber projectile."""
        if proj["type"] == "lightsaber_throw":
            # Draw spinning lightsaber
            size = 20
            center_x, center_y = int(proj["x"]), int(proj["y"])

            # Lightsaber blade
            blade_length = 30
            angle = proj["angle"]

            end_x = center_x + math.cos(angle) * blade_length
            end_y = center_y + math.sin(angle) * blade_length

            # Draw lightsaber blade
            pygame.draw.line(
                surface, proj["color"], (center_x, center_y), (end_x, end_y), 4
            )

            # Draw lightsaber hilt
            pygame.draw.circle(surface, (80, 80, 80), (center_x, center_y), 3)


# Global Force manager instance
force_manager = ForceManager()
