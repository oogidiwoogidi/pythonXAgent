"""
Game Engine

Enhanced Star Wars game engine with Force powers, lightsaber combat,
legendary characters, and epic environments.
"""

import pygame
import random
import os
import math
from config import *
from entities import Player, Enemy, Bullet
from utils import (
    generate_random_platforms,
    draw_labeled_health_bar,
    draw_x_above,
    break_into_pieces,
    draw_weapon_info,
)
from menus import MenuManager
from visual_effects import particle_system, screen_effects, EnhancedRenderer
from sprite_system import sprite_manager, animation_manager
from enhanced_ui import background_manager, enhanced_ui

# Import Star Wars systems
try:
    from force_powers import force_manager
    from lightsaber_combat import lightsaber_combat
    from legendary_characters import LEGENDARY_CHARACTERS, apply_character_profile
    from star_wars_environments import EnvironmentManager
    from game_modes import create_game_mode_manager

    STAR_WARS_ENABLED = True
except ImportError as e:
    print(f"Star Wars systems not available: {e}")
    STAR_WARS_ENABLED = False


class GameEngine:
    """Main game engine class that manages the entire game."""

    def __init__(self):
        """Initialize the enhanced Star Wars game engine."""
        pygame.init()
        pygame.mixer.init()

        # Display setup with fullscreen support
        self.fullscreen = FULLSCREEN_ENABLED
        self.original_size = (WINDOW_WIDTH, WINDOW_HEIGHT)

        # Create game surface (always the original game size)
        self.game_surface = pygame.Surface(self.original_size)

        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.original_size)
        pygame.display.set_caption("STAR WARS: ULTIMATE BATTLE")
        self.clock = pygame.time.Clock()

        # Calculate scaling and positioning for fullscreen
        self._calculate_scaling()

        # Sound manager
        from sound_manager import SoundManager

        self.sound_manager = SoundManager(
            os.path.join(os.path.dirname(__file__), "../assets")
        )

        # Game state
        self.running = True
        self.two_player_mode = False
        self.difficulty = "Medium"
        self.current_game_mode = "classic"
        self.platforms = []

        # Entities
        self.player1 = None
        self.player2 = None
        self.enemy = None
        self.bullets = []

        # Game systems
        self.menu_manager = MenuManager(self.game_surface, self)

        # Enemy shooting system
        self.bullet_timer = 0
        self.bullet_interval = random.randint(40, 120)

        # Explosion tracking
        self.player1_exploded = False
        self.player2_exploded = False
        self.enemy_exploded = False

        # Star Wars systems
        if STAR_WARS_ENABLED:
            self.environment_manager = EnvironmentManager()
            self.current_environment = "death_star"
            self.force_manager = force_manager
            self.lightsaber_combat = lightsaber_combat
            self.game_mode_manager = create_game_mode_manager(self)

    def run(self):
        """Main game loop with enhanced menu system and Star Wars character selection."""
        while self.running:
            # Reset game state before showing menu
            self._reset_game_state()

            # Show start menu and get game mode (player count selection)
            result = self.menu_manager.show_start_and_difficulty_menu()

            if result is None:
                continue  # User quit, restart menu

            self.two_player_mode, _ = result  # Difficulty will be handled later

            # Game Mode Selection (now comes first)
            if STAR_WARS_ENABLED and hasattr(self, "game_mode_manager"):
                selected_mode = self.menu_manager.show_game_mode_selection()
                if selected_mode is None:
                    continue  # User cancelled, return to menu
                self.current_game_mode = selected_mode
                self.game_mode_manager.set_mode(selected_mode)
            else:
                self.current_game_mode = "classic"

            # Difficulty Selection (only for single player, after game mode)
            if not self.two_player_mode:
                difficulty = self.menu_manager._show_difficulty_selection()
                if difficulty is None:
                    continue  # User cancelled, return to menu
                self.difficulty = difficulty
            else:
                # Set default difficulty for two-player mode
                self.difficulty = "Medium"

            # Character selection based on game mode
            if self.two_player_mode:
                # Two player mode: character selection only
                character_selections = self.menu_manager.show_character_selection("two")
            else:
                # Single player mode: dedicated character selection page after difficulty
                character_selections = (
                    self.menu_manager.show_single_player_character_selection()
                )

            if character_selections is None:
                continue  # User quit during character selection, return to menu

            self.character_selections = character_selections

            # Game session loop - allows for rematch without returning to menu
            session_running = True
            while session_running and self.running:
                # Initialize game with character selections
                self._initialize_game()

                # Run game loop
                game_result = self._game_loop()

                # Handle game result
                if game_result == "home":
                    session_running = False  # Return to main menu
                elif game_result == "quit":
                    self.running = False  # Exit game completely
                elif game_result == "rematch":
                    continue  # Restart with same settings and characters
                else:
                    session_running = False  # Default: return to menu

    def _reset_game_state(self):
        """Reset game state to prepare for new menu session."""
        # Clear pygame event queue to prevent stuck events
        pygame.event.clear()

        # Reset game entities
        self.player1 = None
        self.player2 = None
        self.enemy = None
        self.bullets = []

        # Reset explosion tracking
        self.player1_exploded = False
        self.player2_exploded = False
        self.enemy_exploded = False

        # Reset enemy shooting system
        self.bullet_timer = 0
        self.bullet_interval = random.randint(40, 120)

        # Clear platforms
        self.platforms = []

    def _calculate_scaling(self):
        """Calculate scaling factors and positioning for fullscreen mode."""
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        if self.fullscreen:
            # Calculate scale factor to fit game while maintaining aspect ratio
            scale_x = self.screen_width / WINDOW_WIDTH
            scale_y = self.screen_height / WINDOW_HEIGHT
            self.scale_factor = min(scale_x, scale_y)

            # Calculate scaled dimensions
            self.scaled_width = int(WINDOW_WIDTH * self.scale_factor)
            self.scaled_height = int(WINDOW_HEIGHT * self.scale_factor)

            # Calculate centering offset
            self.offset_x = (self.screen_width - self.scaled_width) // 2
            self.offset_y = (self.screen_height - self.scaled_height) // 2
        else:
            # Windowed mode - no scaling needed
            self.scale_factor = 1.0
            self.scaled_width = WINDOW_WIDTH
            self.scaled_height = WINDOW_HEIGHT
            self.offset_x = 0
            self.offset_y = 0

    def _display_menu_with_scaling(self):
        """Display the game surface (with menu content) with proper scaling."""
        if self.fullscreen:
            # Clear screen
            self.screen.fill(BLACK)

            # Scale and center the game surface
            scaled_surface = pygame.transform.scale(
                self.game_surface, (self.scaled_width, self.scaled_height)
            )
            self.screen.blit(scaled_surface, (self.offset_x, self.offset_y))
        else:
            # Windowed mode - direct blit
            self.screen.blit(self.game_surface, (0, 0))

        pygame.display.flip()

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode with proper scaling."""
        self.fullscreen = not self.fullscreen

        if self.fullscreen:
            # Switch to fullscreen
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            # Switch to windowed mode
            self.screen = pygame.display.set_mode(self.original_size)

        # Recalculate scaling for new mode
        self._calculate_scaling()

        # Add visual feedback
        if self.fullscreen:
            enhanced_ui.add_floating_text(
                WINDOW_WIDTH // 2 - 100, 50, "FULLSCREEN MODE", GREEN, 32
            )
        else:
            enhanced_ui.add_floating_text(
                WINDOW_WIDTH // 2 - 80, 50, "WINDOWED MODE", GREEN, 32
            )

    def _initialize_game(self):
        """Initialize game entities and state with character selections and game mode."""
        # Generate platforms
        self.platforms = generate_random_platforms()

        # Create players with character types
        if self.two_player_mode:
            self.player1 = Player(
                WINDOW_WIDTH // 8 - PLAYER_SIZE // 2,
                WINDOW_HEIGHT // 2 - PLAYER_SIZE // 2,
                1,
                self.character_selections["player1"],
            )
            self.player2 = Player(
                7 * WINDOW_WIDTH // 8 - PLAYER2_SIZE // 2,
                WINDOW_HEIGHT // 2 - PLAYER2_SIZE // 2,
                2,
                self.character_selections["player2"],
            )
            self.enemy = None
        else:
            # Single player mode
            self.player1 = Player(
                WINDOW_WIDTH // 2 - PLAYER_SIZE // 2,
                WINDOW_HEIGHT // 2 - PLAYER_SIZE // 2,
                1,
                self.character_selections["player1"],
            )
            self.player2 = None
            # AI gets the opposite character type
            ai_character = self.character_selections["ai"]
            self.enemy = Enemy(
                WINDOW_WIDTH // 4 - ENEMY_SIZE // 2,
                WINDOW_HEIGHT // 2 - ENEMY_SIZE // 2,
                ai_character,
            )

        # Apply game mode restrictions and bonuses
        if STAR_WARS_ENABLED and hasattr(self, "game_mode_manager"):
            # Apply mode-specific restrictions to all entities
            if self.player1:
                self.game_mode_manager.apply_mode_restrictions(self.player1)
            if self.player2:
                self.game_mode_manager.apply_mode_restrictions(self.player2)
            if self.enemy:
                self.game_mode_manager.apply_mode_restrictions(self.enemy)

        # Reset game state
        self.bullets = []
        self.bullet_timer = 0
        self.bullet_interval = random.randint(40, 120)
        self.player1_exploded = False
        self.player2_exploded = False
        self.enemy_exploded = False

    def _game_loop(self):
        """Main game loop with enhanced visual effects."""
        game_over = False
        winner_title = ""

        while not game_over and self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Quick restart (rematch)
                        return "rematch"

                    if event.key == pygame.K_F11:
                        # Toggle fullscreen
                        self.toggle_fullscreen()
                        enhanced_ui.add_floating_text(
                            self.screen_width // 2 - 100,
                            100,
                            "Press F11 to toggle fullscreen",
                            WHITE,
                            24,
                        )

                    # Weapon switching
                    if event.key == pygame.K_1:
                        self.player1.switch_weapon(WEAPON_BLASTER)
                        enhanced_ui.add_floating_text(
                            self.player1.x,
                            self.player1.y - 30,
                            "BLASTER EQUIPPED",
                            GREEN,
                            20,
                        )
                        if self.two_player_mode and self.player2:
                            self.player2.switch_weapon(WEAPON_BLASTER)
                            enhanced_ui.add_floating_text(
                                self.player2.x,
                                self.player2.y - 30,
                                "BLASTER EQUIPPED",
                                BLUE,
                                20,
                            )

                    # Force Powers (Star Wars Mode)
                    if STAR_WARS_ENABLED:
                        # Force Push - Q key
                        if event.key == pygame.K_q and self.player1.is_alive():
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            targets = []
                            if self.two_player_mode and self.player2:
                                targets.append(self.player2)
                            elif self.enemy:
                                targets.append(self.enemy)

                            if self.force_manager.use_power(
                                "force_push", self.player1, mouse_x, mouse_y, targets
                            ):
                                enhanced_ui.add_floating_text(
                                    self.player1.x,
                                    self.player1.y - 40,
                                    "FORCE PUSH!",
                                    BLUE,
                                    24,
                                )

                        # Force Lightning - E key (in two-player mode, different from shooting)
                        if event.key == pygame.K_t and self.player1.is_alive():
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            targets = []
                            if self.two_player_mode and self.player2:
                                targets.append(self.player2)
                            elif self.enemy:
                                targets.append(self.enemy)

                            if self.force_manager.use_power(
                                "force_lightning",
                                self.player1,
                                mouse_x,
                                mouse_y,
                                targets,
                            ):
                                enhanced_ui.add_floating_text(
                                    self.player1.x,
                                    self.player1.y - 40,
                                    "FORCE LIGHTNING!",
                                    (128, 0, 128),
                                    24,
                                )

                        # Lightsaber Throw - G key
                        if event.key == pygame.K_g and self.player1.is_alive():
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            targets = []
                            if self.two_player_mode and self.player2:
                                targets.append(self.player2)
                            elif self.enemy:
                                targets.append(self.enemy)

                            if self.force_manager.use_power(
                                "lightsaber_throw",
                                self.player1,
                                mouse_x,
                                mouse_y,
                                targets,
                            ):
                                enhanced_ui.add_floating_text(
                                    self.player1.x,
                                    self.player1.y - 40,
                                    "LIGHTSABER THROW!",
                                    (0, 255, 255),
                                    24,
                                )

                        # Force Heal - H key
                        if event.key == pygame.K_h and self.player1.is_alive():
                            if self.force_manager.use_power(
                                "force_heal",
                                self.player1,
                                self.player1.x,
                                self.player1.y,
                                [self.player1],
                            ):
                                enhanced_ui.add_floating_text(
                                    self.player1.x,
                                    self.player1.y - 40,
                                    "FORCE HEAL!",
                                    GREEN,
                                    24,
                                )

                        # Lightsaber Attack - F key
                        if event.key == pygame.K_f and self.player1.is_alive():
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            if self.lightsaber_combat.start_attack(
                                self.player1, mouse_x, mouse_y
                            ):
                                enhanced_ui.add_floating_text(
                                    self.player1.x,
                                    self.player1.y - 40,
                                    "LIGHTSABER STRIKE!",
                                    RED,
                                    24,
                                )

                        # Environment Switching - Number keys 2-5
                        if event.key == pygame.K_2:
                            self.current_environment = "death_star"
                            enhanced_ui.add_floating_text(
                                WINDOW_WIDTH // 2, 50, "DEATH STAR", WHITE, 32
                            )
                        elif event.key == pygame.K_3:
                            self.current_environment = "tatooine"
                            enhanced_ui.add_floating_text(
                                WINDOW_WIDTH // 2, 50, "TATOOINE", (255, 255, 0), 32
                            )
                        elif event.key == pygame.K_4:
                            self.current_environment = "endor"
                            enhanced_ui.add_floating_text(
                                WINDOW_WIDTH // 2, 50, "ENDOR", GREEN, 32
                            )
                        elif event.key == pygame.K_5:
                            self.current_environment = "hoth"
                            enhanced_ui.add_floating_text(
                                WINDOW_WIDTH // 2, 50, "HOTH", (0, 255, 255), 32
                            )

                    # Jumping with dust effects
                    if self.two_player_mode:
                        if event.key == pygame.K_w and self.player1.is_alive():
                            self.player1.jump()
                            particle_system.add_jump_dust(
                                self.player1.x + self.player1.size // 2,
                                self.player1.y + self.player1.size,
                            )
                            self.sound_manager.play("jump")
                        if event.key == pygame.K_UP and self.player2.is_alive():
                            self.player2.jump()
                            particle_system.add_jump_dust(
                                self.player2.x + self.player2.size // 2,
                                self.player2.y + self.player2.size,
                            )
                            self.sound_manager.play("jump")
                    else:
                        if event.key == pygame.K_SPACE and self.player1.is_alive():
                            self.player1.jump()
                            particle_system.add_jump_dust(
                                self.player1.x + self.player1.size // 2,
                                self.player1.y + self.player1.size,
                            )
                            self.sound_manager.play("jump")

                    # Shooting with muzzle flash effects
                    if self.two_player_mode:
                        if event.key == pygame.K_e and self.player1.is_alive():
                            new_bullets = self.player1.shoot()
                            if new_bullets:
                                self.bullets.extend(new_bullets)
                                # Add muzzle flash
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                angle = math.atan2(
                                    mouse_y - self.player1.y, mouse_x - self.player1.x
                                )
                                particle_system.add_muzzle_flash(
                                    self.player1.x + self.player1.size // 2,
                                    self.player1.y + self.player1.size // 2,
                                    angle,
                                )
                                screen_effects.add_screen_shake(8, 15)
                                screen_effects.add_screen_flash((255, 255, 255), 120, 6)
                                self.sound_manager.play("shoot")

                        if event.key == pygame.K_KP0 and self.player2.is_alive():
                            new_bullets = self.player2.shoot()
                            if new_bullets:
                                self.bullets.extend(new_bullets)
                                # Add muzzle flash for player 2
                                particle_system.add_muzzle_flash(
                                    self.player2.x + self.player2.size // 2,
                                    self.player2.y + self.player2.size // 2,
                                    0,  # Facing right by default
                                )
                                screen_effects.add_screen_shake(8, 15)
                                screen_effects.add_screen_flash((255, 255, 255), 120, 6)
                                self.sound_manager.play("shoot")

                # Shooting (mouse for single player)
                if not self.two_player_mode and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.player1.is_alive():
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        # Set facing direction based on mouse position
                        self.player1.facing_right = mouse_x > self.player1.x
                        new_bullets = self.player1.shoot()
                        if new_bullets:
                            self.bullets.extend(new_bullets)
                            # Calculate angle towards mouse for muzzle flash
                            import math

                            dx = mouse_x - (self.player1.x + self.player1.size // 2)
                            dy = mouse_y - (self.player1.y + self.player1.size // 2)
                            angle = math.atan2(dy, dx)

                            # Add muzzle flash effect
                            particle_system.add_muzzle_flash(
                                self.player1.x + self.player1.size // 2,
                                self.player1.y + self.player1.size // 2,
                                angle,
                            )
                            screen_effects.add_screen_shake(
                                8, 15
                            )  # Much more intense shake
                            screen_effects.add_screen_flash(
                                (255, 255, 255), 120, 6
                            )  # Brighter, longer flash
                            self.sound_manager.play("shoot")

            # Update entities
            keys = pygame.key.get_pressed()

            if self.player1.is_alive():
                self.player1.update(keys, self.platforms)

            if self.two_player_mode and self.player2 and self.player2.is_alive():
                self.player2.update(keys, self.platforms)

            if not self.two_player_mode and self.enemy and self.enemy.is_alive():
                self.enemy.update(self.player1, self.platforms, self.difficulty)

                # Enemy shooting
                if self.player1.is_alive():
                    self.bullet_timer += 1
                    difficulty_config = DIFFICULTY_LEVELS[self.difficulty]
                    if self.bullet_timer >= random.randint(
                        difficulty_config["interval_min"],
                        difficulty_config["interval_max"],
                    ):
                        self.bullet_timer = 0
                        direction = 1 if self.player1.x > self.enemy.x else -1
                        enemy_bullet = Bullet(
                            self.enemy.x + self.enemy.size // 2,
                            self.enemy.y + self.enemy.size // 2,
                            direction * difficulty_config["bullet_speed"],
                            0,  # Enemy owner ID
                        )
                        self.bullets.append(enemy_bullet)

                        # Add muzzle flash for enemy shooting
                        dx = self.player1.x - self.enemy.x
                        dy = self.player1.y - self.enemy.y
                        angle = math.atan2(dy, dx)

                        particle_system.add_muzzle_flash(
                            self.enemy.x + self.enemy.size // 2,
                            self.enemy.y + self.enemy.size // 2,
                            angle,
                        )
                        screen_effects.add_screen_shake(6, 10)
                        screen_effects.add_screen_flash((255, 255, 200), 80, 4)
                        self.sound_manager.play("shoot")

            # Update bullets
            for bullet in self.bullets[:]:
                bullet.update()
                if bullet.is_off_screen():
                    self.bullets.remove(bullet)

            # Update Star Wars systems
            if STAR_WARS_ENABLED:
                self.force_manager.update()
                self.lightsaber_combat.update()
                if hasattr(self, "environment_manager"):
                    self.environment_manager.update()

                # Update game mode manager
                if hasattr(self, "game_mode_manager"):
                    game_state = {
                        "player1": self.player1,
                        "player2": self.player2,
                        "enemy": self.enemy,
                        "bullets": self.bullets,
                        "platforms": self.platforms,
                    }
                    self.game_mode_manager.update(game_state)

            # Handle collisions
            self._handle_collisions()

            # Update visual effects
            particle_system.update()
            screen_effects.update()
            enhanced_ui.update()
            animation_manager.update_animations()
            background_manager.update()

            # Render everything
            self._render()

            # Check for game over (including mode-specific win conditions)
            winner_title = self._check_game_over()
            if winner_title:
                game_over = True

            self.clock.tick(FPS)

        # Show game over screen if needed
        if winner_title:
            self.sound_manager.play("game_over")
            menu_choice = self.menu_manager.show_game_over(winner_title)
            return menu_choice

        return "home"  # Default return to home if no winner

    def _handle_collisions(self):
        """Handle all collision detection and responses."""
        # Bullet vs Player collisions
        for bullet in self.bullets[:]:
            bullet_hit = False

            # Enemy bullets vs Player 1
            if bullet.owner_id == 0 and self.player1.is_alive():
                if bullet.rect.colliderect(self.player1.rect):
                    self.player1.take_damage(bullet.damage, bullet.dx)
                    # Add visual effects
                    enhanced_ui.add_damage_indicator(
                        bullet.x, bullet.y, bullet.damage, RED
                    )
                    particle_system.add_blood_splatter(
                        self.player1.x + self.player1.size // 2,
                        self.player1.y + self.player1.size // 2,
                    )
                    screen_effects.add_screen_shake(3, 8)
                    screen_effects.add_screen_flash(RED, 80, 3)
                    self.bullets.remove(bullet)
                    bullet_hit = True
                    self.sound_manager.play("damage")

            # Player 1 bullets vs Enemy (single player mode)
            elif (
                bullet.owner_id == 1
                and not self.two_player_mode
                and self.enemy
                and self.enemy.is_alive()
            ):
                if bullet.rect.colliderect(self.enemy.rect):
                    self.enemy.take_damage(bullet.damage, bullet.dx)
                    # Add visual effects
                    enhanced_ui.add_damage_indicator(
                        bullet.x, bullet.y, bullet.damage, ORANGE
                    )
                    particle_system.add_explosion(
                        self.enemy.x + self.enemy.size // 2,
                        self.enemy.y + self.enemy.size // 2,
                        (255, 150, 0),
                        8,
                    )
                    screen_effects.add_screen_shake(2, 6)
                    self.bullets.remove(bullet)
                    bullet_hit = True
                    self.sound_manager.play("damage")

            # Player 1 bullets vs Player 2 (two player mode)
            elif (
                bullet.owner_id == 1
                and self.two_player_mode
                and self.player2
                and self.player2.is_alive()
            ):
                if bullet.rect.colliderect(self.player2.rect):
                    self.player2.take_damage(bullet.damage, bullet.dx)
                    # Add visual effects
                    enhanced_ui.add_damage_indicator(
                        bullet.x, bullet.y, bullet.damage, RED
                    )
                    particle_system.add_blood_splatter(
                        self.player2.x + self.player2.size // 2,
                        self.player2.y + self.player2.size // 2,
                    )
                    screen_effects.add_screen_shake(3, 8)
                    screen_effects.add_screen_flash(RED, 80, 3)
                    self.bullets.remove(bullet)
                    bullet_hit = True
                    self.sound_manager.play("damage")

            # Player 2 bullets vs Player 1 (two player mode)
            elif (
                bullet.owner_id == 2
                and self.two_player_mode
                and self.player1.is_alive()
            ):
                if bullet.rect.colliderect(self.player1.rect):
                    self.player1.take_damage(bullet.damage, bullet.dx)
                    self.bullets.remove(bullet)
                    bullet_hit = True
                    self.sound_manager.play("damage")

    def _render(self):
        """Render all game objects with enhanced Star Wars visuals and proper fullscreen scaling."""
        # Update all entity animations before rendering
        animation_manager.update_animations()

        # Apply screen shake offset
        shake_x, shake_y = screen_effects.get_screen_offset()

        # Clear and draw to the game surface (original resolution)
        self.game_surface.fill(WHITE)

        # Draw Star Wars environment background
        if STAR_WARS_ENABLED and hasattr(self, "environment_manager"):
            self.environment_manager.draw_environment(
                self.game_surface, self.current_environment
            )
        else:
            background_manager.draw_space_background(self.game_surface)

        # Create a temporary surface for shake effect
        if shake_x != 0 or shake_y != 0:
            temp_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            temp_surface.fill((0, 0, 0))
            render_surface = temp_surface
        else:
            render_surface = self.game_surface

        # Draw platforms with enhanced visuals
        for platform in self.platforms:
            platform_sprite = sprite_manager.get_sprite("platform")
            scaled_sprite = sprite_manager.scale_sprite(
                platform_sprite, platform.width, platform.height
            )
            render_surface.blit(scaled_sprite, (platform.x, platform.y))

        # Draw Star Wars Force power effects
        if STAR_WARS_ENABLED:
            self.force_manager.draw(render_surface)
            self.lightsaber_combat.draw(render_surface)

        # Draw entities with sprites
        if self.player1:
            self.player1.draw(render_surface)
            if not self.player1.is_alive():
                draw_x_above(
                    render_surface, self.player1.x, self.player1.y, self.player1.size
                )
                if not self.player1_exploded:
                    particle_system.add_explosion(
                        self.player1.x + self.player1.size // 2,
                        self.player1.y + self.player1.size // 2,
                        self.player1.color,
                    )
                    screen_effects.add_screen_shake(8, 15)
                    enhanced_ui.add_floating_text(
                        self.player1.x, self.player1.y - 20, "JEDI DOWN!", RED, 32
                    )
                    break_into_pieces(
                        render_surface,
                        self.player1.x,
                        self.player1.y,
                        self.player1.size,
                        self.player1.color,
                    )
                    self.player1_exploded = True

        if self.two_player_mode and self.player2:
            self.player2.draw(render_surface)
            if not self.player2.is_alive():
                draw_x_above(
                    render_surface, self.player2.x, self.player2.y, self.player2.size
                )
                if not self.player2_exploded:
                    particle_system.add_explosion(
                        self.player2.x + self.player2.size // 2,
                        self.player2.y + self.player2.size // 2,
                        self.player2.color,
                    )
                    screen_effects.add_screen_shake(8, 15)
                    enhanced_ui.add_floating_text(
                        self.player2.x, self.player2.y - 20, "SITH DOWN!", BLUE, 32
                    )
                    break_into_pieces(
                        render_surface,
                        self.player2.x,
                        self.player2.y,
                        self.player2.size,
                        self.player2.color,
                    )
                    self.player2_exploded = True

        if not self.two_player_mode and self.enemy:
            self.enemy.draw(render_surface)
            if not self.enemy.is_alive():
                draw_x_above(
                    render_surface, self.enemy.x, self.enemy.y, self.enemy.size
                )
                if not self.enemy_exploded:
                    particle_system.add_explosion(
                        self.enemy.x + self.enemy.size // 2,
                        self.enemy.y + self.enemy.size // 2,
                        self.enemy.color,
                    )
                    screen_effects.add_screen_shake(6, 12)
                    enhanced_ui.add_floating_text(
                        self.enemy.x, self.enemy.y - 20, "ENEMY DESTROYED!", GREEN, 28
                    )
                    break_into_pieces(
                        render_surface,
                        self.enemy.x,
                        self.enemy.y,
                        self.enemy.size,
                        self.enemy.color,
                    )
                    self.enemy_exploded = True

        # Draw bullets with enhanced effects
        for bullet in self.bullets:
            # Add bullet trails
            particle_system.add_bullet_trail(
                bullet.x, bullet.y, bullet.dx, 0, bullet.color
            )
            # Draw bullet using its draw method (supports enhanced/animated sprites)
            bullet.draw(render_surface)

        # Draw particle effects
        particle_system.draw(render_surface)

        # Apply screen shake by blitting the temp surface with offset
        if shake_x != 0 or shake_y != 0:
            self.game_surface.blit(temp_surface, (shake_x, shake_y))

        # Draw screen flash to game surface
        screen_effects.draw_flash(self.game_surface)

        # Draw UI elements to game surface
        self._draw_ui()

        # Draw floating UI elements to game surface
        enhanced_ui.draw_damage_indicators(self.game_surface)
        enhanced_ui.draw_floating_text(self.game_surface)

        # Draw mini-map to game surface
        players = [p for p in [self.player1, self.player2] if p and p.is_alive()]
        enemies = [self.enemy] if self.enemy and self.enemy.is_alive() else []
        enhanced_ui.draw_mini_map(self.game_surface, players, enemies, self.platforms)

        # Now handle the final display with proper scaling
        self.screen.fill(BLACK)  # Fill with black borders

        if self.fullscreen and self.scale_factor != 1.0:
            # Scale and center the game surface for fullscreen
            scaled_surface = pygame.transform.scale(
                self.game_surface, (self.scaled_width, self.scaled_height)
            )
            self.screen.blit(scaled_surface, (self.offset_x, self.offset_y))
        else:
            # Direct blit for windowed mode
            self.screen.blit(self.game_surface, (0, 0))

        pygame.display.flip()

    def _draw_ui(self):
        """Draw enhanced Star Wars user interface elements."""
        font = pygame.font.Font(None, 24)

        # Enhanced health bars
        if self.two_player_mode:
            EnhancedRenderer.draw_health_bar_enhanced(
                self.game_surface,
                10,
                10,
                200,
                20,
                self.player1.health,
                self.player1.max_health,
            )
            # Player 1 label with character name
            if hasattr(self.player1, "character_name"):
                label_text = f"{self.player1.character_name}"
            else:
                label_text = "Player 1"
            label = font.render(label_text, True, WHITE)
            self.game_surface.blit(label, (10, 35))

            # Force energy bar for Player 1
            if STAR_WARS_ENABLED and hasattr(self.player1, "force_energy"):
                EnhancedRenderer.draw_health_bar_enhanced(
                    self.game_surface,
                    10,
                    50,
                    200,
                    15,
                    self.player1.force_energy,
                    self.player1.max_force_energy,
                    bar_color=BLUE,
                    bg_color=(30, 30, 100),
                )
                force_label = font.render("Force Energy", True, BLUE)
                self.game_surface.blit(force_label, (10, 70))

            if self.player2:
                EnhancedRenderer.draw_health_bar_enhanced(
                    self.game_surface,
                    WINDOW_WIDTH - 210,
                    10,
                    200,
                    20,
                    self.player2.health,
                    self.player2.max_health,
                )
                # Player 2 label with character name
                if hasattr(self.player2, "character_name"):
                    label_text = f"{self.player2.character_name}"
                else:
                    label_text = "Player 2"
                label = font.render(label_text, True, WHITE)
                self.game_surface.blit(label, (WINDOW_WIDTH - 210, 35))

                # Force energy bar for Player 2
                if STAR_WARS_ENABLED and hasattr(self.player2, "force_energy"):
                    EnhancedRenderer.draw_health_bar_enhanced(
                        self.game_surface,
                        WINDOW_WIDTH - 210,
                        50,
                        200,
                        15,
                        self.player2.force_energy,
                        self.player2.max_force_energy,
                        bar_color=RED,
                        bg_color=(100, 30, 30),
                    )
                    force_label = font.render("Force Energy", True, RED)
                    self.game_surface.blit(force_label, (WINDOW_WIDTH - 210, 70))

            # Enhanced weapon HUD for both players
            if self.player1.is_alive():
                enhanced_ui.draw_weapon_hud(
                    self.game_surface,
                    self.player1.weapon,
                    self.player1.magazine,
                    MAGAZINE_SIZE,
                    10,
                    90,
                )

            if self.player2 and self.player2.is_alive():
                enhanced_ui.draw_weapon_hud(
                    self.game_surface,
                    self.player2.weapon,
                    self.player2.magazine,
                    MAGAZINE_SIZE,
                    WINDOW_WIDTH - 160,
                    90,
                )
        else:
            # Single player mode
            EnhancedRenderer.draw_health_bar_enhanced(
                self.game_surface,
                10,
                10,
                200,
                20,
                self.player1.health,
                self.player1.max_health,
            )
            # Player label with character name
            if hasattr(self.player1, "character_name"):
                label_text = f"{self.player1.character_name}"
            else:
                label_text = "Player"
            label = font.render(label_text, True, WHITE)
            self.game_surface.blit(label, (10, 35))

            # Force energy bar for Player
            if STAR_WARS_ENABLED and hasattr(self.player1, "force_energy"):
                EnhancedRenderer.draw_health_bar_enhanced(
                    self.game_surface,
                    10,
                    50,
                    200,
                    15,
                    self.player1.force_energy,
                    self.player1.max_force_energy,
                    bar_color=BLUE,
                    bg_color=(30, 30, 100),
                )
                force_label = font.render("Force Energy", True, BLUE)
                self.game_surface.blit(force_label, (10, 70))

            if self.enemy and self.enemy.is_alive():
                EnhancedRenderer.draw_health_bar_enhanced(
                    self.game_surface,
                    WINDOW_WIDTH - 210,
                    10,
                    200,
                    20,
                    self.enemy.health,
                    self.enemy.max_health,
                )
                # Enemy label with character name
                if hasattr(self.enemy, "character_name"):
                    label_text = f"{self.enemy.character_name}"
                else:
                    label_text = "Enemy"
                label = font.render(label_text, True, WHITE)
                self.game_surface.blit(label, (WINDOW_WIDTH - 210, 35))

                # Force energy bar for Enemy
                if STAR_WARS_ENABLED and hasattr(self.enemy, "force_energy"):
                    EnhancedRenderer.draw_health_bar_enhanced(
                        self.game_surface,
                        WINDOW_WIDTH - 210,
                        50,
                        200,
                        15,
                        self.enemy.force_energy,
                        self.enemy.max_force_energy,
                        bar_color=RED,
                        bg_color=(100, 30, 30),
                    )
                    force_label = font.render("Force Energy", True, RED)
                    self.game_surface.blit(force_label, (WINDOW_WIDTH - 210, 70))

            # Enhanced weapon HUD
            if self.player1.is_alive():
                enhanced_ui.draw_weapon_hud(
                    self.game_surface,
                    self.player1.weapon,
                    self.player1.magazine,
                    MAGAZINE_SIZE,
                    10,
                    90,
                )

        # Draw crosshair for mouse aiming (single player mode)
        if not self.two_player_mode:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Scale mouse position for the game surface if in fullscreen
            if self.fullscreen:
                # Convert screen mouse position to game surface coordinates
                scaled_mouse_x = int((mouse_x - self.offset_x) / self.scale_factor)
                scaled_mouse_y = int((mouse_y - self.offset_y) / self.scale_factor)
                # Clamp to game surface bounds
                scaled_mouse_x = max(0, min(WINDOW_WIDTH, scaled_mouse_x))
                scaled_mouse_y = max(0, min(WINDOW_HEIGHT, scaled_mouse_y))
                enhanced_ui.draw_enhanced_crosshair(
                    self.game_surface, scaled_mouse_x, scaled_mouse_y
                )
            else:
                enhanced_ui.draw_enhanced_crosshair(self.game_surface, mouse_x, mouse_y)

        # Star Wars control hints
        if STAR_WARS_ENABLED:
            hints_font = pygame.font.Font(None, 20)
            hints = [
                "Q: Force Push",
                "T: Force Lightning",
                "G: Lightsaber Throw",
                "H: Force Heal",
                "F: Lightsaber Attack",
                "2-5: Change Environment",
            ]

            for i, hint in enumerate(hints):
                hint_surface = hints_font.render(hint, True, WHITE)
                self.game_surface.blit(
                    hint_surface, (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 150 + i * 20)
                )

        # Environment indicator
        if STAR_WARS_ENABLED and hasattr(self, "current_environment"):
            env_font = pygame.font.Font(None, 32)
            env_name = self.current_environment.replace("_", " ").title()
            env_surface = env_font.render(env_name, True, (255, 255, 0))
            self.game_surface.blit(env_surface, (WINDOW_WIDTH // 2 - 100, 10))

        # Game mode UI
        if STAR_WARS_ENABLED and hasattr(self, "game_mode_manager"):
            self.game_mode_manager.draw_mode_ui(self.game_surface)

        # Weapon info
        if self.player1:
            draw_weapon_info(self.game_surface, self.player1, 0, 0)

        if self.two_player_mode and self.player2:
            draw_weapon_info(self.game_surface, self.player2, 0, 0)

    def _check_game_over(self):
        """
        Check for game over conditions including mode-specific win conditions.

        Returns:
            str: Winner title or empty string if game continues
        """
        # Check mode-specific win conditions first
        if STAR_WARS_ENABLED and hasattr(self, "game_mode_manager"):
            game_state = {
                "player1": self.player1,
                "player2": self.player2,
                "enemy": self.enemy,
                "bullets": self.bullets,
                "platforms": self.platforms,
            }
            mode_winner = self.game_mode_manager.check_win_condition(game_state)
            if mode_winner:
                return mode_winner

        # Standard win conditions
        if not self.player1.is_alive():
            if self.two_player_mode:
                return "Player 2"
            else:
                return "NPC"
        elif self.two_player_mode and self.player2 and not self.player2.is_alive():
            return "Player 1"
        elif not self.two_player_mode and self.enemy and not self.enemy.is_alive():
            return "Player"

        return ""
