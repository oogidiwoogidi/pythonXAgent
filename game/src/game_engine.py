"""
Game Engine

Main game engine that handles the game loop, entity management,
collision detection, and rendering.
"""

import pygame
import random
import os
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


class GameEngine:
    """Main game engine class that manages the entire game."""

    def __init__(self):
        """Initialize the game engine."""
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
        pygame.display.set_caption(WINDOW_TITLE)
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
        self.platforms = []

        # Entities
        self.player1 = None
        self.player2 = None
        self.enemy = None
        self.bullets = []
        # Removed: self.grenades = []

        # Game systems
        self.menu_manager = MenuManager(self.game_surface, self)

        # Enemy shooting system
        self.bullet_timer = 0
        self.bullet_interval = random.randint(40, 120)

        # Explosion tracking
        self.player1_exploded = False
        self.player2_exploded = False
        self.enemy_exploded = False

    def run(self):
        """Main game loop with enhanced menu system."""
        while self.running:
            # Show start menu and get game mode
            self.two_player_mode, self.difficulty = (
                self.menu_manager.show_start_and_difficulty_menu()
            )

            # Game session loop - allows for rematch without returning to menu
            session_running = True
            while session_running and self.running:
                # Initialize game
                self._initialize_game()

                # Run game loop
                game_result = self._game_loop()

                # Handle game result
                if game_result == "home":
                    session_running = False  # Return to main menu
                elif game_result == "quit":
                    self.running = False  # Exit game completely
                elif game_result == "rematch":
                    continue  # Restart with same settings
                else:
                    session_running = False  # Default: return to menu

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
        """Initialize game entities and state."""
        # Generate platforms
        self.platforms = generate_random_platforms()

        # Create players
        if self.two_player_mode:
            self.player1 = Player(
                WINDOW_WIDTH // 8 - PLAYER_SIZE // 2,
                WINDOW_HEIGHT // 2 - PLAYER_SIZE // 2,
                1,
            )
            self.player2 = Player(
                7 * WINDOW_WIDTH // 8 - PLAYER2_SIZE // 2,
                WINDOW_HEIGHT // 2 - PLAYER2_SIZE // 2,
                2,
            )
            self.enemy = None
        else:
            self.player1 = Player(
                WINDOW_WIDTH // 2 - PLAYER_SIZE // 2,
                WINDOW_HEIGHT // 2 - PLAYER_SIZE // 2,
                1,
            )
            self.player2 = None
            self.enemy = Enemy(
                WINDOW_WIDTH // 4 - ENEMY_SIZE // 2,
                WINDOW_HEIGHT // 2 - ENEMY_SIZE // 2,
            )

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
                        self.player1.switch_weapon(WEAPON_RIFLE)
                        enhanced_ui.add_floating_text(
                            self.player1.x,
                            self.player1.y - 30,
                            "RIFLE EQUIPPED",
                            GREEN,
                            20,
                        )
                        if self.two_player_mode and self.player2:
                            self.player2.switch_weapon(WEAPON_RIFLE)
                            enhanced_ui.add_floating_text(
                                self.player2.x,
                                self.player2.y - 30,
                                "RIFLE EQUIPPED",
                                BLUE,
                                20,
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
                                import math

                                angle = math.atan2(
                                    mouse_y - self.player1.y, mouse_x - self.player1.x
                                )
                                particle_system.add_muzzle_flash(
                                    self.player1.x + self.player1.size // 2,
                                    self.player1.y + self.player1.size // 2,
                                    angle,
                                )
                                screen_effects.add_screen_shake(2, 5)
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
                                screen_effects.add_screen_shake(2, 5)
                                self.sound_manager.play("shoot")

                    # Grenade throw
                    # Removed grenade throw logic for 'Q'

                # Shooting (mouse for single player)
                if not self.two_player_mode and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.player1.is_alive():
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        # Set facing direction based on mouse position
                        self.player1.facing_right = mouse_x > self.player1.x
                        new_bullets = self.player1.shoot()
                        self.bullets.extend(new_bullets)
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

            # Update bullets
            for bullet in self.bullets[:]:
                bullet.update()
                if bullet.is_off_screen():
                    self.bullets.remove(bullet)

            # Update grenades
            # Removed grenade update and explosion logic

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

            # Check for game over
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
        """Render all game objects with enhanced visuals and proper fullscreen scaling."""
        # Apply screen shake offset
        shake_x, shake_y = screen_effects.get_screen_offset()

        # Clear and draw to the game surface (original resolution)
        self.game_surface.fill(WHITE)
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

        # Draw entities with sprites
        if self.player1:
            player_sprite = sprite_manager.get_sprite("player")
            render_surface.blit(player_sprite, (self.player1.x, self.player1.y))
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
                        self.player1.x, self.player1.y - 20, "PLAYER DOWN!", RED, 32
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
            player2_sprite = sprite_manager.get_sprite("player2")
            render_surface.blit(player2_sprite, (self.player2.x, self.player2.y))
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
                        self.player2.x, self.player2.y - 20, "PLAYER 2 DOWN!", BLUE, 32
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
            enemy_sprite = sprite_manager.get_sprite("enemy")
            render_surface.blit(enemy_sprite, (self.enemy.x, self.enemy.y))
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

            # Draw enhanced bullet sprite
            bullet_sprite = sprite_manager.get_sprite("bullet")
            render_surface.blit(bullet_sprite, (bullet.x - 2, bullet.y - 1))

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
        """Draw user interface elements with enhanced visuals."""
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
            # Player 1 label
            font = pygame.font.Font(None, 24)
            label = font.render("Player 1", True, WHITE)
            self.game_surface.blit(label, (10, 35))

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
                # Player 2 label
                label = font.render("Player 2", True, WHITE)
                self.game_surface.blit(label, (WINDOW_WIDTH - 210, 35))

            # Enhanced weapon HUD for both players
            if self.player1.is_alive():
                enhanced_ui.draw_weapon_hud(
                    self.game_surface,
                    self.player1.weapon,
                    self.player1.magazine,
                    MAGAZINE_SIZE,
                    10,
                    60,
                )

            if self.player2 and self.player2.is_alive():
                enhanced_ui.draw_weapon_hud(
                    self.game_surface,
                    self.player2.weapon,
                    self.player2.magazine,
                    MAGAZINE_SIZE,
                    WINDOW_WIDTH - 160,
                    60,
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
            # Player label
            font = pygame.font.Font(None, 24)
            label = font.render("Player", True, WHITE)
            self.game_surface.blit(label, (10, 35))

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
                # Enemy label
                label = font.render("Enemy", True, WHITE)
                self.game_surface.blit(label, (WINDOW_WIDTH - 210, 35))

            # Enhanced weapon HUD
            if self.player1.is_alive():
                enhanced_ui.draw_weapon_hud(
                    self.game_surface,
                    self.player1.weapon,
                    self.player1.magazine,
                    MAGAZINE_SIZE,
                    10,
                    60,
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

        # Weapon info
        if self.player1:
            draw_weapon_info(self.game_surface, self.player1, 0, 0)

        if self.two_player_mode and self.player2:
            draw_weapon_info(self.game_surface, self.player2, 0, 0)

    def _check_game_over(self):
        """
        Check for game over conditions.

        Returns:
            str: Winner title or empty string if game continues
        """
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
