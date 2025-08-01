"""
Game Modes System

Comprehensive game modes for the Star Wars Ultimate Battle experience.
Each mode has unique rules, objectives, and gameplay mechanics.
"""

import pygame
import random
import math
from config import *
from entities import Player, Enemy, Bullet
from visual_effects import particle_system, screen_effects
from enhanced_ui import enhanced_ui


class GameModeManager:
    """Manages different game modes and their specific rules."""

    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.current_mode = "classic"
        self.mode_timer = 0
        self.mode_data = {}

        # Define all available game modes (compatible with both single and two-player)
        self.game_modes = {
            "classic": {
                "name": "Classic Battle",
                "description": "Traditional combat with all weapons and Force powers",
                "icon": "⚔️",
                "color": WHITE,
                "supports_two_player": True,
            },
            "lightsaber_duel": {
                "name": "Lightsaber Duels",
                "description": "Pure lightsaber combat - no blasters, only Force and sabers",
                "icon": "🗡️",
                "color": (0, 255, 255),
                "supports_two_player": True,
            },
            "blaster_battle": {
                "name": "Blaster Battles",
                "description": "Intense blaster combat - no Force powers, rapid fire",
                "icon": "🔫",
                "color": (255, 128, 0),
                "supports_two_player": True,
            },
            "force_arena": {
                "name": "Force Arena",
                "description": "Force powers only - no weapons, pure Force mastery",
                "icon": "⚡",
                "color": BLUE,
                "supports_two_player": True,
            },
            "survival_coop": {
                "name": "Co-op Survival",
                "description": "Team up against endless waves of enemies",
                "icon": "🛡️",
                "color": GREEN,
                "supports_two_player": True,
            },
            "king_of_hill": {
                "name": "King of the Hill",
                "description": "Control the center platform to score points (PvP)",
                "icon": "👑",
                "color": (255, 215, 0),
                "supports_two_player": True,
            },
            "capture_flag": {
                "name": "Capture the Flag",
                "description": "Steal the enemy's holocron and return it to base (PvP)",
                "icon": "🏆",
                "color": (255, 100, 100),
                "supports_two_player": True,
            },
            "force_race": {
                "name": "Force Race",
                "description": "Race through checkpoints using Force powers",
                "icon": "🏁",
                "color": (255, 0, 255),
                "supports_two_player": True,
            },
        }

    def get_mode_list(self):
        """Get list of all available game modes."""
        return list(self.game_modes.keys())

    def get_mode_info(self, mode_key):
        """Get information about a specific game mode."""
        return self.game_modes.get(mode_key, self.game_modes["classic"])

    def set_mode(self, mode_key):
        """Set the current game mode and initialize mode-specific data."""
        if mode_key in self.game_modes:
            self.current_mode = mode_key
            self.mode_timer = 0
            self.mode_data = {}
            self._initialize_mode()

    def _initialize_mode(self):
        """Initialize mode-specific data and settings."""
        mode = self.current_mode
        is_two_player = getattr(self.game_engine, "two_player_mode", False)

        if mode == "lightsaber_duel":
            self.mode_data = {
                "blasters_disabled": True,
                "force_multiplier": 1.5,
                "lightsaber_damage_bonus": 10,
                "energy_regen_bonus": 2.0,
            }

        elif mode == "blaster_battle":
            self.mode_data = {
                "force_disabled": True,
                "rapid_fire": True,
                "magazine_bonus": 20,
                "reload_speed_bonus": 0.5,
                "bullet_speed_bonus": 1.5,
            }

        elif mode == "force_arena":
            self.mode_data = {
                "weapons_disabled": True,
                "force_multiplier": 2.0,
                "energy_regen_bonus": 3.0,
                "force_damage_bonus": 15,
            }

        elif mode == "survival_coop":
            self.mode_data = {
                "wave": 1,
                "enemies_remaining": 3,
                "score": 0,
                "spawn_timer": 0,
                "difficulty_multiplier": 1.0,
                "enemy_list": [],
                "coop_mode": is_two_player,
                "team_lives": 3 if is_two_player else 1,
            }

        elif mode == "king_of_hill":
            self.mode_data = {
                "king_zone": pygame.Rect(
                    WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50, 200, 100
                ),
                "player1_score": 0,
                "player2_score": 0,
                "control_time": 0,
                "score_to_win": 500,
                "points_per_second": 1,
                "contested": False,
            }

        elif mode == "capture_flag":
            self.mode_data = {
                "flag1_pos": [150, WINDOW_HEIGHT // 2],
                "flag2_pos": [WINDOW_WIDTH - 150, WINDOW_HEIGHT // 2],
                "flag1_captured": False,
                "flag2_captured": False,
                "flag1_carrier": None,
                "flag2_carrier": None,
                "player1_score": 0,
                "player2_score": 0,
                "captures_to_win": 3,
            }

        elif mode == "force_race":
            self.mode_data = {
                "checkpoints": self._generate_race_checkpoints(),
                "player1_checkpoint": 0,
                "player2_checkpoint": 0,
                "player1_lap": 0,
                "player2_lap": 0,
                "race_time": 0,
                "laps_to_win": 3,
                "race_finished": False,
                "winner": None,
            }

    def _generate_race_checkpoints(self):
        """Generate checkpoints for Force Race mode."""
        checkpoints = []
        num_checkpoints = 8

        for i in range(num_checkpoints):
            angle = (2 * math.pi * i) / num_checkpoints
            center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
            radius = 200

            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)

            checkpoints.append({"pos": [x, y], "radius": 30, "collected": False})

        return checkpoints

    def update(self, game_state):
        """Update mode-specific logic."""
        self.mode_timer += 1
        mode = self.current_mode
        is_two_player = getattr(self.game_engine, "two_player_mode", False)

        if mode == "survival_coop":
            self._update_survival_coop(game_state, is_two_player)
        elif mode == "king_of_hill":
            self._update_king_of_hill(game_state, is_two_player)
        elif mode == "capture_flag":
            self._update_capture_flag(game_state, is_two_player)
        elif mode == "force_race":
            self._update_force_race(game_state, is_two_player)

    def _update_survival(self, game_state):
        """Update survival mode logic."""
        data = self.mode_data

        # Spawn enemies
        if len(data["enemy_list"]) < data["enemies_remaining"]:
            data["spawn_timer"] += 1
            if data["spawn_timer"] > 60:  # Spawn every second
                self._spawn_survival_enemy(game_state)
                data["spawn_timer"] = 0

        # Check wave completion
        if data["enemies_remaining"] <= 0 and len(data["enemy_list"]) == 0:
            data["wave"] += 1
            data["enemies_remaining"] = 3 + data["wave"]
            data["difficulty_multiplier"] += 0.2

            enhanced_ui.add_floating_text(
                WINDOW_WIDTH // 2, 100, f"WAVE {data['wave']}!", (255, 255, 0), 48
            )
            screen_effects.add_screen_flash((0, 255, 0), 120, 8)

    def _spawn_survival_enemy(self, game_state):
        """Spawn an enemy for survival mode."""
        # Random spawn position at edges
        if random.choice([True, False]):
            x = random.choice([0, WINDOW_WIDTH - ENEMY_SIZE])
            y = random.randint(0, WINDOW_HEIGHT - ENEMY_SIZE)
        else:
            x = random.randint(0, WINDOW_WIDTH - ENEMY_SIZE)
            y = random.choice([0, WINDOW_HEIGHT - ENEMY_SIZE])

        enemy = Enemy(x, y, random.choice(["sith", "jedi"]))

        # Apply difficulty scaling
        multiplier = self.mode_data["difficulty_multiplier"]
        enemy.health = int(enemy.health * multiplier)
        enemy.max_health = enemy.health

        self.mode_data["enemy_list"].append(enemy)
        self.mode_data["enemies_remaining"] -= 1

    def _update_king_of_hill(self, game_state):
        """Update King of the Hill mode."""
        data = self.mode_data
        player1 = game_state.get("player1")
        player2 = game_state.get("player2")

        if not player1 or not player2:
            return

        zone = data["king_zone"]

        # Check who's in the zone
        p1_in_zone = zone.colliderect(player1.rect) if player1.is_alive() else False
        p2_in_zone = zone.colliderect(player2.rect) if player2.is_alive() else False

        # Award points
        if p1_in_zone and not p2_in_zone:
            data["player1_score"] += data["points_per_second"]
            data["control_time"] += 1
        elif p2_in_zone and not p1_in_zone:
            data["player2_score"] += data["points_per_second"]
            data["control_time"] += 1
        elif p1_in_zone and p2_in_zone:
            # Contested - no points awarded
            data["control_time"] = 0

    def _update_capture_flag(self, game_state):
        """Update Capture the Flag mode."""
        data = self.mode_data
        player1 = game_state.get("player1")
        player2 = game_state.get("player2")

        if not player1 or not player2:
            return

        # Check flag captures and returns
        # This would need more detailed implementation
        pass

    def _update_force_race(self, game_state):
        """Update Force Race mode."""
        data = self.mode_data
        data["race_time"] += 1

        # Check checkpoint collection
        # This would need more detailed implementation
        pass

    def apply_mode_restrictions(self, entity):
        """Apply mode-specific restrictions to entities."""
        mode = self.current_mode

        if mode == "lightsaber_duel":
            # Disable blasters, enhance Force and lightsaber
            if hasattr(entity, "weapon"):
                entity.blaster_disabled = True
            if hasattr(entity, "force_energy"):
                entity.force_regen_rate *= self.mode_data.get("energy_regen_bonus", 1.0)

        elif mode == "blaster_battle":
            # Disable Force powers, enhance blasters
            if hasattr(entity, "force_energy"):
                entity.force_disabled = True
            if hasattr(entity, "magazine"):
                entity.magazine += self.mode_data.get("magazine_bonus", 0)

        elif mode == "force_arena":
            # Disable weapons, enhance Force powers
            if hasattr(entity, "weapon"):
                entity.weapons_disabled = True
            if hasattr(entity, "force_energy"):
                entity.force_regen_rate *= self.mode_data.get("energy_regen_bonus", 1.0)

    def check_win_condition(self, game_state):
        """Check if win condition is met for current mode."""
        mode = self.current_mode

        if mode == "survival":
            # Survival continues until player dies
            player1 = game_state.get("player1")
            if player1 and not player1.is_alive():
                return f"Wave {self.mode_data['wave']} Complete!"

        elif mode == "king_of_hill":
            data = self.mode_data
            if data["player1_score"] >= data["score_to_win"]:
                return "Player 1 Dominates!"
            elif data["player2_score"] >= data["score_to_win"]:
                return "Player 2 Dominates!"

        elif mode == "capture_flag":
            data = self.mode_data
            if data["player1_score"] >= data["captures_to_win"]:
                return "Player 1 Captures Victory!"
            elif data["player2_score"] >= data["captures_to_win"]:
                return "Player 2 Captures Victory!"

        elif mode == "force_race":
            # Check if someone completed all laps
            data = self.mode_data
            if (
                data["player1_checkpoint"]
                >= len(data["checkpoints"]) * data["laps_to_win"]
            ):
                return "Player 1 Wins the Race!"
            elif (
                data["player2_checkpoint"]
                >= len(data["checkpoints"]) * data["laps_to_win"]
            ):
                return "Player 2 Wins the Race!"

        # Default win conditions for other modes
        return None

    def draw_mode_ui(self, surface):
        """Draw mode-specific UI elements."""
        mode = self.current_mode
        font = pygame.font.Font(None, 24)

        # Mode name display
        mode_info = self.game_modes[mode]
        mode_text = font.render(
            f"{mode_info['icon']} {mode_info['name']}", True, mode_info["color"]
        )
        surface.blit(mode_text, (WINDOW_WIDTH // 2 - mode_text.get_width() // 2, 10))

        if mode == "survival":
            self._draw_survival_ui(surface, font)
        elif mode == "king_of_hill":
            self._draw_king_of_hill_ui(surface, font)
        elif mode == "capture_flag":
            self._draw_capture_flag_ui(surface, font)
        elif mode == "force_race":
            self._draw_force_race_ui(surface, font)

    def _draw_survival_ui(self, surface, font):
        """Draw survival mode UI."""
        data = self.mode_data
        wave_text = font.render(f"Wave: {data['wave']}", True, WHITE)
        enemies_text = font.render(
            f"Enemies: {data['enemies_remaining'] + len(data['enemy_list'])}",
            True,
            WHITE,
        )
        score_text = font.render(f"Score: {data['score']}", True, WHITE)

        surface.blit(wave_text, (10, 100))
        surface.blit(enemies_text, (10, 125))
        surface.blit(score_text, (10, 150))

    def _draw_king_of_hill_ui(self, surface, font):
        """Draw King of the Hill UI."""
        data = self.mode_data

        # Draw the king zone
        pygame.draw.rect(surface, (255, 215, 0, 100), data["king_zone"], 3)

        # Scores
        p1_score = font.render(f"P1: {data['player1_score']}", True, BLUE)
        p2_score = font.render(f"P2: {data['player2_score']}", True, RED)

        surface.blit(p1_score, (10, 100))
        surface.blit(p2_score, (WINDOW_WIDTH - 100, 100))

    def _draw_capture_flag_ui(self, surface, font):
        """Draw Capture the Flag UI."""
        data = self.mode_data

        # Draw flags
        flag_color1 = BLUE if not data["flag1_captured"] else GRAY
        flag_color2 = RED if not data["flag2_captured"] else GRAY

        pygame.draw.circle(surface, flag_color1, data["flag1_pos"], 20)
        pygame.draw.circle(surface, flag_color2, data["flag2_pos"], 20)

        # Scores
        p1_score = font.render(f"P1 Captures: {data['player1_score']}", True, BLUE)
        p2_score = font.render(f"P2 Captures: {data['player2_score']}", True, RED)

        surface.blit(p1_score, (10, 100))
        surface.blit(p2_score, (WINDOW_WIDTH - 150, 100))

    def _draw_force_race_ui(self, surface, font):
        """Draw Force Race UI."""
        data = self.mode_data

        # Draw checkpoints
        for i, checkpoint in enumerate(data["checkpoints"]):
            color = GREEN if checkpoint["collected"] else (255, 255, 0)
            pygame.draw.circle(
                surface,
                color,
                [int(checkpoint["pos"][0]), int(checkpoint["pos"][1])],
                checkpoint["radius"],
                3,
            )

            # Checkpoint number
            num_text = font.render(str(i + 1), True, WHITE)
            surface.blit(num_text, (checkpoint["pos"][0] - 8, checkpoint["pos"][1] - 8))

        # Race info
        lap_text = font.render(
            f"Lap: {data['current_lap']}/{data['laps_to_win']}", True, WHITE
        )
        time_text = font.render(f"Time: {data['race_time'] // 60}s", True, WHITE)

        surface.blit(lap_text, (10, 100))
        surface.blit(time_text, (10, 125))


# Game mode instances
def create_game_mode_manager(game_engine):
    """Create and return a game mode manager instance."""
    return GameModeManager(game_engine)
