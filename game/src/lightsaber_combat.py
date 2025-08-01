"""
Star Wars Lightsaber Combat System

Advanced melee combat system featuring:
- Lightsaber swings and combos
- Blocking and parrying
- Clash effects
- Directional attacks
"""

import pygame
import math
import random
from config import *


class LightsaberAttack:
    """Represents a lightsaber attack."""

    def __init__(self, attacker, direction, attack_type="slash"):
        self.attacker = attacker
        self.direction = direction  # angle in radians
        self.attack_type = attack_type
        self.damage = 20
        self.range = 60
        self.duration = 20
        self.current_frame = 0
        self.hit_entities = set()

        # Visual properties
        self.color = (
            (100, 150, 255) if attacker.character_type == "jedi" else (255, 100, 100)
        )
        self.trail_points = []

    def update(self):
        """Update attack animation."""
        self.current_frame += 1

        # Calculate swing arc
        progress = self.current_frame / self.duration
        swing_angle = self.direction + math.sin(progress * math.pi) * 0.8

        # Calculate blade tip position
        blade_length = self.range
        tip_x = (
            self.attacker.x
            + self.attacker.size // 2
            + math.cos(swing_angle) * blade_length
        )
        tip_y = (
            self.attacker.y
            + self.attacker.size // 2
            + math.sin(swing_angle) * blade_length
        )

        # Add to trail
        self.trail_points.append((tip_x, tip_y))
        if len(self.trail_points) > 8:
            self.trail_points.pop(0)

        return self.current_frame < self.duration

    def check_collision(self, target):
        """Check if attack hits target."""
        if target in self.hit_entities or target == self.attacker:
            return False

        # Calculate attack area
        center_x = self.attacker.x + self.attacker.size // 2
        center_y = self.attacker.y + self.attacker.size // 2
        target_center_x = target.x + target.size // 2
        target_center_y = target.y + target.size // 2

        distance = math.sqrt(
            (target_center_x - center_x) ** 2 + (target_center_y - center_y) ** 2
        )

        if distance <= self.range:
            # Check if target is in swing arc
            target_angle = math.atan2(
                target_center_y - center_y, target_center_x - center_x
            )
            angle_diff = abs(target_angle - self.direction)
            angle_diff = min(angle_diff, 2 * math.pi - angle_diff)

            if angle_diff <= 0.6:  # ~34 degree arc
                self.hit_entities.add(target)
                return True

        return False

    def draw(self, surface):
        """Draw lightsaber attack."""
        if self.current_frame >= self.duration:
            return

        center_x = self.attacker.x + self.attacker.size // 2
        center_y = self.attacker.y + self.attacker.size // 2

        # Draw lightsaber blade
        progress = self.current_frame / self.duration
        swing_angle = self.direction + math.sin(progress * math.pi) * 0.8

        blade_length = self.range
        tip_x = center_x + math.cos(swing_angle) * blade_length
        tip_y = center_y + math.sin(swing_angle) * blade_length

        # Draw main blade
        pygame.draw.line(surface, self.color, (center_x, center_y), (tip_x, tip_y), 6)

        # Draw blade glow
        glow_color = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.line(surface, glow_color, (center_x, center_y), (tip_x, tip_y), 8)

        # Draw trail
        if len(self.trail_points) > 1:
            for i in range(1, len(self.trail_points)):
                alpha = (i / len(self.trail_points)) * 100
                trail_color = (*self.color, int(alpha))
                # Note: pygame doesn't support alpha in draw.line, so we'll use a simple trail
                pygame.draw.line(
                    surface,
                    self.color,
                    self.trail_points[i - 1],
                    self.trail_points[i],
                    2,
                )


class LightsaberBlock:
    """Represents a defensive blocking stance."""

    def __init__(self, defender, direction):
        self.defender = defender
        self.direction = direction
        self.duration = 30
        self.current_frame = 0
        self.color = (
            (100, 150, 255) if defender.character_type == "jedi" else (255, 100, 100)
        )

    def update(self):
        """Update block animation."""
        self.current_frame += 1
        return self.current_frame < self.duration

    def can_block(self, attack_direction):
        """Check if this block can defend against an attack."""
        angle_diff = abs(self.direction - attack_direction)
        angle_diff = min(angle_diff, 2 * math.pi - angle_diff)
        return angle_diff <= 1.0  # ~57 degree coverage

    def draw(self, surface):
        """Draw blocking lightsaber."""
        center_x = self.defender.x + self.defender.size // 2
        center_y = self.defender.y + self.defender.size // 2

        # Draw defensive blade position
        blade_length = 40
        tip_x = center_x + math.cos(self.direction) * blade_length
        tip_y = center_y + math.sin(self.direction) * blade_length

        # Draw blade with defensive glow
        pygame.draw.line(surface, self.color, (center_x, center_y), (tip_x, tip_y), 8)

        # Draw defensive energy field
        for i in range(3):
            radius = 15 + i * 5
            alpha = 50 - i * 15
            temp_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                temp_surf, (*self.color, alpha), (radius, radius), radius
            )
            surface.blit(temp_surf, (center_x - radius, center_y - radius))


class LightsaberClash:
    """Represents a lightsaber clash between two opponents."""

    def __init__(self, attacker, defender, clash_point):
        self.attacker = attacker
        self.defender = defender
        self.clash_point = clash_point
        self.duration = 60
        self.current_frame = 0
        self.intensity = 0.0

    def update(self):
        """Update clash effect."""
        self.current_frame += 1
        self.intensity = math.sin(self.current_frame * 0.3) * 0.5 + 0.5
        return self.current_frame < self.duration

    def draw(self, surface):
        """Draw clash effect."""
        # Draw sparks and energy
        for i in range(8):
            angle = (self.current_frame + i * 45) * 0.1
            distance = 20 + self.intensity * 10
            spark_x = self.clash_point[0] + math.cos(angle) * distance
            spark_y = self.clash_point[1] + math.sin(angle) * distance

            # Draw spark
            pygame.draw.circle(
                surface, (255, 255, 255), (int(spark_x), int(spark_y)), 2
            )

        # Draw central energy burst
        burst_radius = int(15 + self.intensity * 10)
        for radius in range(burst_radius, 0, -3):
            alpha = (burst_radius - radius) * 20
            temp_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                temp_surf, (255, 255, 255, alpha), (radius, radius), radius
            )
            surface.blit(
                temp_surf, (self.clash_point[0] - radius, self.clash_point[1] - radius)
            )


class LightsaberCombat:
    """Manages lightsaber combat system."""

    def __init__(self):
        self.active_attacks = []
        self.active_blocks = []
        self.active_clashes = []

    def start_attack(self, attacker, target_x, target_y):
        """Start a lightsaber attack."""
        if not hasattr(attacker, "lightsaber_cooldown"):
            attacker.lightsaber_cooldown = 0

        if attacker.lightsaber_cooldown <= 0:
            center_x = attacker.x + attacker.size // 2
            center_y = attacker.y + attacker.size // 2
            direction = math.atan2(target_y - center_y, target_x - center_x)

            attack = LightsaberAttack(attacker, direction)
            self.active_attacks.append(attack)
            attacker.lightsaber_cooldown = 40
            return True
        return False

    def start_block(self, defender, direction):
        """Start a defensive block."""
        # Remove existing blocks from this defender
        self.active_blocks = [
            block for block in self.active_blocks if block.defender != defender
        ]

        block = LightsaberBlock(defender, direction)
        self.active_blocks.append(block)
        return True

    def update(self, entities):
        """Update all combat actions."""
        # Update entity cooldowns
        for entity in entities:
            if (
                hasattr(entity, "lightsaber_cooldown")
                and entity.lightsaber_cooldown > 0
            ):
                entity.lightsaber_cooldown -= 1

        # Update attacks
        for attack in self.active_attacks[:]:
            if not attack.update():
                self.active_attacks.remove(attack)
                continue

            # Check for hits
            for entity in entities:
                if hasattr(entity, "take_damage") and attack.check_collision(entity):
                    # Check if target is blocking
                    blocked = False
                    for block in self.active_blocks:
                        if block.defender == entity and block.can_block(
                            attack.direction
                        ):
                            # Create clash effect
                            clash_point = (
                                (attack.attacker.x + entity.x) // 2 + 20,
                                (attack.attacker.y + entity.y) // 2 + 20,
                            )
                            self.active_clashes.append(
                                LightsaberClash(attack.attacker, entity, clash_point)
                            )
                            blocked = True
                            break

                    if not blocked:
                        # Deal damage
                        knockback_x = math.cos(attack.direction) * 15
                        entity.take_damage(attack.damage, knockback_x)

        # Update blocks
        self.active_blocks = [block for block in self.active_blocks if block.update()]

        # Update clashes
        self.active_clashes = [clash for clash in self.active_clashes if clash.update()]

    def draw(self, surface):
        """Draw all combat effects."""
        for attack in self.active_attacks:
            attack.draw(surface)

        for block in self.active_blocks:
            block.draw(surface)

        for clash in self.active_clashes:
            clash.draw(surface)


# Global lightsaber combat instance
lightsaber_combat = LightsaberCombat()
