"""
Game Engine

Main game engine that handles the game loop, entity management,
collision detection, and rendering.
"""

import pygame
import random
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


class GameEngine:
    """Main game engine class that manages the entire game."""

    def __init__(self):
        """Initialize the game engine."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

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

        # Game systems
        self.menu_manager = MenuManager(self.screen)

        # Enemy shooting system
        self.bullet_timer = 0
        self.bullet_interval = random.randint(40, 120)

        # Explosion tracking
        self.player1_exploded = False
        self.player2_exploded = False
        self.enemy_exploded = False

    def run(self):
        """Main game loop."""
        while self.running:
            # Show start menu and get game mode
            self.two_player_mode, self.difficulty = (
                self.menu_manager.show_start_and_difficulty_menu()
            )

            # Initialize game
            self._initialize_game()

            # Run game loop
            self._game_loop()

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
        """Main game loop."""
        game_over = False
        winner_title = ""

        while not game_over and self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart game
                        return

                    # Weapon switching
                    if event.key == pygame.K_1:
                        self.player1.switch_weapon(WEAPON_RIFLE)
                    if event.key == pygame.K_2:
                        self.player1.switch_weapon(WEAPON_SHOTGUN)

                    if self.two_player_mode:
                        if event.key == pygame.K_KP1:
                            self.player2.switch_weapon(WEAPON_RIFLE)
                        if event.key == pygame.K_KP2:
                            self.player2.switch_weapon(WEAPON_SHOTGUN)

                    # Jumping
                    if event.key == pygame.K_SPACE and self.player1.is_alive():
                        self.player1.jump()

                    if (
                        self.two_player_mode
                        and event.key == pygame.K_UP
                        and self.player2.is_alive()
                    ):
                        self.player2.jump()

                    # Shooting (keyboard)
                    if self.two_player_mode:
                        if event.key == pygame.K_e and self.player1.is_alive():
                            new_bullets = self.player1.shoot()
                            self.bullets.extend(new_bullets)

                        if event.key == pygame.K_KP0 and self.player2.is_alive():
                            new_bullets = self.player2.shoot()
                            self.bullets.extend(new_bullets)

                # Shooting (mouse for single player)
                if not self.two_player_mode and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.player1.is_alive():
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        # Set facing direction based on mouse position
                        self.player1.facing_right = mouse_x > self.player1.x
                        new_bullets = self.player1.shoot()
                        self.bullets.extend(new_bullets)

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

            # Handle collisions
            self._handle_collisions()

            # Render everything
            self._render()

            # Check for game over
            winner_title = self._check_game_over()
            if winner_title:
                game_over = True

            self.clock.tick(FPS)

        # Show game over screen if needed
        if winner_title:
            restart_clicked = self.menu_manager.show_game_over(winner_title)
            if not restart_clicked:
                self.running = False

    def _handle_collisions(self):
        """Handle all collision detection and responses."""
        # Bullet vs Player collisions
        for bullet in self.bullets[:]:
            bullet_hit = False

            # Enemy bullets vs Player 1
            if bullet.owner_id == 0 and self.player1.is_alive():
                if bullet.rect.colliderect(self.player1.rect):
                    self.player1.take_damage(bullet.damage, bullet.dx)
                    self.bullets.remove(bullet)
                    bullet_hit = True

            # Player 1 bullets vs Enemy (single player mode)
            elif (
                bullet.owner_id == 1
                and not self.two_player_mode
                and self.enemy
                and self.enemy.is_alive()
            ):
                if bullet.rect.colliderect(self.enemy.rect):
                    # Shotgun range check
                    if bullet.is_shotgun:
                        if abs(bullet.x - self.enemy.x) <= 5 * BLOCK_SIZE:
                            self.enemy.take_damage(bullet.damage, bullet.dx)
                            self.bullets.remove(bullet)
                            bullet_hit = True
                    else:
                        self.enemy.take_damage(bullet.damage, bullet.dx)
                        self.bullets.remove(bullet)
                        bullet_hit = True

            # Player 1 bullets vs Player 2 (two player mode)
            elif (
                bullet.owner_id == 1
                and self.two_player_mode
                and self.player2
                and self.player2.is_alive()
            ):
                if bullet.rect.colliderect(self.player2.rect):
                    # Shotgun range check
                    if bullet.is_shotgun:
                        if abs(bullet.x - self.player2.x) <= 5 * BLOCK_SIZE:
                            self.player2.take_damage(bullet.damage, bullet.dx)
                            self.bullets.remove(bullet)
                            bullet_hit = True
                    else:
                        self.player2.take_damage(bullet.damage, bullet.dx)
                        self.bullets.remove(bullet)
                        bullet_hit = True

            # Player 2 bullets vs Player 1 (two player mode)
            elif (
                bullet.owner_id == 2
                and self.two_player_mode
                and self.player1.is_alive()
            ):
                if bullet.rect.colliderect(self.player1.rect):
                    # Shotgun range check
                    if bullet.is_shotgun:
                        if abs(bullet.x - self.player1.x) <= 5 * BLOCK_SIZE:
                            self.player1.take_damage(bullet.damage, bullet.dx)
                            self.bullets.remove(bullet)
                            bullet_hit = True
                    else:
                        self.player1.take_damage(bullet.damage, bullet.dx)
                        self.bullets.remove(bullet)
                        bullet_hit = True

    def _render(self):
        """Render all game objects."""
        # Clear screen
        self.screen.fill(WHITE)

        # Draw platforms
        for platform in self.platforms:
            pygame.draw.rect(self.screen, PLATFORM_COLOR, platform)

        # Draw entities
        if self.player1:
            self.player1.draw(self.screen)
            if not self.player1.is_alive():
                draw_x_above(
                    self.screen, self.player1.x, self.player1.y, self.player1.size
                )
                if not self.player1_exploded:
                    break_into_pieces(
                        self.screen,
                        self.player1.x,
                        self.player1.y,
                        self.player1.size,
                        self.player1.color,
                    )
                    self.player1_exploded = True

        if self.two_player_mode and self.player2:
            self.player2.draw(self.screen)
            if not self.player2.is_alive():
                draw_x_above(
                    self.screen, self.player2.x, self.player2.y, self.player2.size
                )
                if not self.player2_exploded:
                    break_into_pieces(
                        self.screen,
                        self.player2.x,
                        self.player2.y,
                        self.player2.size,
                        self.player2.color,
                    )
                    self.player2_exploded = True

        if not self.two_player_mode and self.enemy:
            self.enemy.draw(self.screen)
            if not self.enemy.is_alive():
                draw_x_above(self.screen, self.enemy.x, self.enemy.y, self.enemy.size)
                if not self.enemy_exploded:
                    break_into_pieces(
                        self.screen,
                        self.enemy.x,
                        self.enemy.y,
                        self.enemy.size,
                        self.enemy.color,
                    )
                    self.enemy_exploded = True

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # Draw UI
        self._draw_ui()

        pygame.display.flip()

    def _draw_ui(self):
        """Draw user interface elements."""
        # Health bars
        if self.two_player_mode:
            draw_labeled_health_bar(
                self.screen,
                10,
                10,
                self.player1.health,
                self.player1.max_health,
                "Player 1",
            )
            if self.player2:
                draw_labeled_health_bar(
                    self.screen,
                    WINDOW_WIDTH - 110,
                    10,
                    self.player2.health,
                    self.player2.max_health,
                    "Player 2",
                )
        else:
            draw_labeled_health_bar(
                self.screen,
                10,
                10,
                self.player1.health,
                self.player1.max_health,
                "Player",
            )
            if self.enemy:
                draw_labeled_health_bar(
                    self.screen,
                    WINDOW_WIDTH - 110,
                    10,
                    self.enemy.health,
                    self.enemy.max_health,
                    "NPC",
                )

        # Weapon info
        if self.player1:
            draw_weapon_info(self.screen, self.player1, 0, 0)

        if self.two_player_mode and self.player2:
            draw_weapon_info(self.screen, self.player2, 0, 0)

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
