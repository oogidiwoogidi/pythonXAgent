"""
Entity Classes

This module contains all the entity classes for the game including
Player, Enemy, and Bullet classes with their respective behaviors.
"""

import pygame
import random
import os
from config import *


class Entity:
    """Base class for all game entities."""

    def __init__(self, x, y, size, color):
        """Initialize a basic entity."""
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.velocity_y = 0
        self.is_jumping = False
        self.rect = pygame.Rect(x, y, size, size)

    def update_rect(self):
        """Update the collision rectangle."""
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface):
        """Draw the entity on the given surface."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))


class Player(Entity):
    """Player entity with movement, jumping, and combat capabilities."""

    def __init__(self, x, y, player_id=1):
        """Initialize a player."""
        if player_id == 1:
            super().__init__(x, y, PLAYER_SIZE, PLAYER_COLOR)
            self.max_health = PLAYER_MAX_HEALTH
            self.speed = PLAYER_SPEED
        else:
            super().__init__(x, y, PLAYER2_SIZE, PLAYER2_COLOR)
            self.max_health = PLAYER2_MAX_HEALTH
            self.speed = PLAYER2_SPEED

        self.player_id = player_id
        self.health = self.max_health
        self.facing_right = True

        # Weapon system
        self.weapon = WEAPON_RIFLE
        self.magazine = MAGAZINE_SIZE
        self.reloading = False
        self.reload_timer = 0
        self.rifle_cooldown = 0

        # Knockback system
        self.knockback_timer = 0
        self.knockback_dx = 0
        self.knockback_dy = 0

    def update(self, keys, platforms):
        """Update player state including movement, gravity, and weapons."""
        # Handle reloading
        if self.reloading:
            self.reload_timer += 1
            if self.reload_timer >= RELOAD_FRAMES:
                self.magazine = MAGAZINE_SIZE
                self.reloading = False
                self.reload_timer = 0

        # Handle weapon cooldowns
        if self.rifle_cooldown > 0:
            self.rifle_cooldown -= 1

        # Handle knockback
        if self.knockback_timer > 0:
            self.x += self.knockback_dx
            self.y += self.knockback_dy
            self.knockback_dy += GRAVITY

            # Add shake effect
            self.x += random.randint(-2, 2)
            self.y += random.randint(-2, 2)

            # Constrain within window
            self.x = max(0, min(self.x, WINDOW_WIDTH - self.size))
            self.y = max(0, min(self.y, WINDOW_HEIGHT - self.size))

            self.knockback_timer -= 1
        else:
            # Normal movement (only if not in knockback)
            self._handle_movement(keys)

        # Apply gravity and platform collisions
        self._apply_gravity_and_platforms(platforms)

        # Update collision rectangle
        self.update_rect()

    def _handle_movement(self, keys):
        """Handle player movement based on input keys."""
        if self.player_id == 1:
            # Player 1 controls (WASD)
            # Only allow left/right/down movement; jumping is handled by jump() method
            if keys[pygame.K_s]:
                self.y += self.speed
            if keys[pygame.K_a]:
                self.x -= self.speed
                self.facing_right = False
            if keys[pygame.K_d]:
                self.x += self.speed
                self.facing_right = True
        else:
            # Player 2 controls (Arrow keys)
            if keys[pygame.K_DOWN]:
                self.y += self.speed
            if keys[pygame.K_LEFT]:
                self.x -= self.speed
                self.facing_right = False
            if keys[pygame.K_RIGHT]:
                self.x += self.speed
                self.facing_right = True

        # Constrain horizontally
        self.x = max(0, min(self.x, WINDOW_WIDTH - self.size))

    def _apply_gravity_and_platforms(self, platforms):
        """Apply gravity and handle platform collisions. Prevent landing glitch."""
        landed = False
        new_y = self.y + self.velocity_y
        temp_rect = pygame.Rect(self.x, new_y, self.size, self.size)

        for platform in platforms:
            if temp_rect.colliderect(platform) and self.velocity_y >= 0:
                # Snap player exactly on top of platform
                self.y = platform.top - self.size
                self.velocity_y = 0
                landed = True
                break

        if not landed and new_y + self.size >= WINDOW_HEIGHT:
            # Snap player exactly on ground
            self.y = WINDOW_HEIGHT - self.size
            self.velocity_y = 0
            landed = True

        if not landed:
            self.y = new_y
            self.velocity_y += GRAVITY
        else:
            self.is_jumping = False

    def jump(self):
        """Make the player jump if not already jumping."""
        if not self.is_jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.is_jumping = True

    def shoot(self):
        """Shoot a bullet based on the current weapon."""
        bullets = []

        if self.weapon == WEAPON_RIFLE:
            if not self.reloading and self.magazine > 0 and self.rifle_cooldown == 0:
                direction = 1 if self.facing_right else -1
                bullet = Bullet(
                    self.x + self.size // 2,
                    self.y + self.size // 2,
                    direction
                    * (
                        PLAYER_BULLET_SPEED
                        if self.player_id == 1
                        else PLAYER2_BULLET_SPEED
                    ),
                    self.player_id,
                )
                bullets.append(bullet)
                self.magazine -= 1
                self.rifle_cooldown = RIFLE_COOLDOWN_FRAMES

                if self.magazine == 0:
                    self.reloading = True
                    self.reload_timer = 0

        return bullets

    def switch_weapon(self, key):
        """Switch to rifle only (shotgun removed)."""
        if key == pygame.K_1 or key == pygame.K_KP1:
            self.weapon = WEAPON_RIFLE

    def take_damage(self, damage, bullet_direction):
        """Take damage and apply knockback."""
        self.health = max(0, self.health - damage)

        # Apply knockback
        self.knockback_dx = (
            KNOCKBACK_DISTANCE if bullet_direction > 0 else -KNOCKBACK_DISTANCE
        )
        self.knockback_dy = -KNOCKBACK_VERTICAL
        self.knockback_timer = KNOCKBACK_DURATION

    def is_alive(self):
        """Check if the player is still alive."""
        return self.health > 0

    def draw(self, surface):
        """Draw the player block split into two colored halves indicating shooting direction."""
        half_size = self.size // 2
        # Determine colors for each half
        if self.facing_right:
            left_color = GRAY
            right_color = GREEN
        else:
            left_color = RED
            right_color = GRAY

        # Draw left half
        pygame.draw.rect(surface, left_color, (self.x, self.y, half_size, self.size))
        # Draw right half
        pygame.draw.rect(
            surface, right_color, (self.x + half_size, self.y, half_size, self.size)
        )


class Enemy(Entity):
    """Enemy AI entity with movement, jumping, and shooting capabilities."""

    def __init__(self, x, y):
        """Initialize an enemy."""
        super().__init__(x, y, ENEMY_SIZE, ENEMY_COLOR)
        self.health = ENEMY_MAX_HEALTH
        self.max_health = ENEMY_MAX_HEALTH

        # AI behavior
        self.jump_timer = 0
        self.jump_interval = 120

        # Knockback system
        self.knockback_timer = 0
        self.knockback_dx = 0
        self.knockback_dy = 0

    def update(self, player, platforms, difficulty):
        """Update enemy AI behavior."""
        difficulty_config = DIFFICULTY_LEVELS[difficulty]
        self.jump_interval = difficulty_config["enemy_jump_interval"]

        # Handle knockback
        if self.knockback_timer > 0:
            self.x += self.knockback_dx
            self.y += self.knockback_dy
            self.knockback_dy += GRAVITY

            # Add shake effect
            self.x += random.randint(-2, 2)
            self.y += random.randint(-2, 2)

            # Constrain within window
            self.x = max(0, min(self.x, WINDOW_WIDTH - self.size))
            self.y = max(0, min(self.y, WINDOW_HEIGHT - self.size))

            self.knockback_timer -= 1
        else:
            # AI movement
            self._ai_movement(player, difficulty_config)

        # Apply gravity and platform collisions
        self._apply_gravity_and_platforms(platforms)

        # Update collision rectangle
        self.update_rect()

    def _ai_movement(self, player, difficulty_config):
        """Handle AI movement toward player."""
        enemy_speed = difficulty_config["enemy_speed"]
        distance_x = abs(player.x - self.x)

        # Only move if player is more than 8 blocks away
        if distance_x > 8 * BLOCK_SIZE:
            if player.x > self.x:
                self.x += enemy_speed
            elif player.x < self.x:
                self.x -= enemy_speed

        # Constrain horizontally
        self.x = max(0, min(self.x, WINDOW_WIDTH - self.size))

    def _apply_gravity_and_platforms(self, platforms):
        """Apply gravity and handle platform collisions."""
        landed = False
        new_y = self.y + self.velocity_y
        temp_rect = pygame.Rect(self.x, new_y, self.size, self.size)

        for platform in platforms:
            if temp_rect.colliderect(platform) and self.velocity_y >= 0:
                new_y = platform.top - self.size
                self.velocity_y = 0
                landed = True
                break

        if new_y + self.size >= WINDOW_HEIGHT:
            new_y = WINDOW_HEIGHT - self.size
            self.velocity_y = 0
            landed = True

        self.y = new_y
        if not landed:
            self.velocity_y += GRAVITY

        # AI jumping
        self.jump_timer += 1
        if landed and self.jump_timer >= self.jump_interval:
            if random.random() < 0.7:  # 70% chance to jump
                self.velocity_y = -ENEMY_JUMP_STRENGTH
            self.jump_timer = 0

    def take_damage(self, damage, bullet_direction):
        """Take damage and apply knockback."""
        self.health = max(0, self.health - damage)

        # Apply knockback
        self.knockback_dx = (
            KNOCKBACK_DISTANCE if bullet_direction > 0 else -KNOCKBACK_DISTANCE
        )
        self.knockback_dy = -KNOCKBACK_VERTICAL
        self.knockback_timer = KNOCKBACK_DURATION

    def is_alive(self):
        """Check if the enemy is still alive."""
        return self.health > 0

    def shoot_at_player(self, player):
        """Shoot at the player."""
        if self.shoot_timer <= 0:
            # Create bullet towards player
            direction = 1 if player.x > self.x else -1


class Bullet:
    """Bullet projectile class."""

    def __init__(self, x, y, dx, owner_id, is_shotgun=False):
        """Initialize a bullet."""
        self.x = x
        self.y = y
        self.dx = dx
        self.owner_id = owner_id  # 1 for player1, 2 for player2, 0 for enemy
        self.is_shotgun = is_shotgun

        # Set bullet properties based on owner
        if owner_id == 1:
            self.width = PLAYER_BULLET_WIDTH
            self.height = PLAYER_BULLET_HEIGHT
            self.color = PLAYER_BULLET_COLOR
            self.damage = PLAYER_BULLET_DAMAGE
        elif owner_id == 2:
            self.width = PLAYER2_BULLET_WIDTH
            self.height = PLAYER2_BULLET_HEIGHT
            self.color = PLAYER2_BULLET_COLOR
            self.damage = PLAYER2_BULLET_DAMAGE
        else:  # Enemy bullet
            self.width = BULLET_WIDTH
            self.height = BULLET_HEIGHT
            self.color = BULLET_COLOR
            self.damage = ENEMY_BULLET_DAMAGE

        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self):
        """Update bullet position."""
        self.x += self.dx
        self.rect.x = self.x

    def draw(self, surface):
        """Draw the bullet on the given surface."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        """Check if bullet is off screen."""
        return self.x < 0 or self.x > WINDOW_WIDTH
        self.x += self.dx
        self.rect.x = self.x

    def draw(self, surface):
        """Draw the bullet on the given surface."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        """Check if bullet is off screen."""
        return self.x < 0 or self.x > WINDOW_WIDTH
        self.x += self.dx
        self.rect.x = self.x

    def draw(self, surface):
        """Draw the bullet on the given surface."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        """Check if bullet is off screen."""
        return self.x < 0 or self.x > WINDOW_WIDTH
