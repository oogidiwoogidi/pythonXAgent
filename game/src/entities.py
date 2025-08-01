"""
Entity Classes

This module contains all the entity classes for the game including
Player, Enemy, and Bullet classes with their respective behaviors.
Enhanced with Force powers, lightsaber combat, and legendary characters.
"""

import pygame
import random
import os
import math
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
        # Import sprite manager for enhanced character sprites
        try:
            from sprite_system import sprite_manager

            if hasattr(self, "character_type"):
                character_sprite = sprite_manager.get_character_sprite(
                    self.character_type, self.size
                )
                surface.blit(character_sprite, (self.x, self.y))
            else:
                pygame.draw.rect(
                    surface, self.color, (self.x, self.y, self.size, self.size)
                )
        except:
            pygame.draw.rect(
                surface, self.color, (self.x, self.y, self.size, self.size)
            )


class Player(Entity):
    """Enhanced Player entity with Force powers, lightsaber combat, and legendary character support."""

    def __init__(self, x, y, player_id=1, character_type="jedi"):
        """Initialize a player with character type (jedi or sith)."""
        if player_id == 1:
            super().__init__(x, y, PLAYER_SIZE, PLAYER_COLOR)
            self.max_health = PLAYER_MAX_HEALTH
            self.speed = PLAYER_SPEED
        else:
            super().__init__(x, y, PLAYER2_SIZE, PLAYER2_COLOR)
            self.max_health = PLAYER2_MAX_HEALTH
            self.speed = PLAYER2_SPEED

        self.player_id = player_id
        self.character_type = character_type  # 'jedi' or 'sith'
        self.health = self.max_health
        self.facing_right = True

        # Enhanced Force and combat systems
        self.max_force_energy = 100
        self.force_energy = self.max_force_energy
        self.force_regen_rate = 1
        self.force_power_bonus = 1.0

        # Lightsaber combat
        self.lightsaber_cooldown = 0
        self.lightsaber_damage_bonus = 0
        self.is_blocking = False
        self.stunned = 0

        # Legendary character support
        self.character_name = "Unknown Warrior"
        self.character_description = "A Force-sensitive warrior"
        self.special_abilities = []

        # Weapon system (enhanced for Star Wars)
        self.weapon = WEAPON_BLASTER
        self.magazine = MAGAZINE_SIZE
        self.reloading = False
        self.reload_timer = 0
        self.blaster_cooldown = 0

        # Knockback system
        self.knockback_timer = 0
        self.knockback_dx = 0
        self.knockback_dy = 0

    def update(self, keys, platforms):
        """Update player state including movement, gravity, weapons, and Force powers."""
        # Handle stunning
        if self.stunned > 0:
            self.stunned -= 1
            return  # Skip other updates while stunned

        # Force energy regeneration
        if self.force_energy < self.max_force_energy:
            self.force_energy = min(
                self.max_force_energy, self.force_energy + self.force_regen_rate * 0.1
            )

        # Handle reloading
        if self.reloading:
            self.reload_timer += 1
            if self.reload_timer >= RELOAD_FRAMES:
                self.magazine = MAGAZINE_SIZE
                self.reloading = False
                self.reload_timer = 0

        # Handle weapon cooldowns
        if self.blaster_cooldown > 0:
            self.blaster_cooldown -= 1

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

        if self.weapon == WEAPON_BLASTER:
            if not self.reloading and self.magazine > 0 and self.blaster_cooldown == 0:
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
                self.blaster_cooldown = BLASTER_COOLDOWN_FRAMES

                if self.magazine == 0:
                    self.reloading = True
                    self.reload_timer = 0

        return bullets

    def use_force_power(self, power_name, target_x, target_y, entities):
        """Use a Force power."""
        try:
            from force_powers import force_manager

            return force_manager.use_power(
                power_name, self, target_x, target_y, entities
            )
        except ImportError:
            return False

    def lightsaber_attack(self, target_x, target_y):
        """Perform a lightsaber attack."""
        try:
            from lightsaber_combat import lightsaber_combat

            return lightsaber_combat.start_attack(self, target_x, target_y)
        except ImportError:
            return False

    def lightsaber_block(self, direction):
        """Start blocking with lightsaber."""
        try:
            from lightsaber_combat import lightsaber_combat

            self.is_blocking = True
            return lightsaber_combat.start_block(self, direction)
        except ImportError:
            return False

    def stop_blocking(self):
        """Stop blocking."""
        self.is_blocking = False

    def apply_legendary_character(self, character_key):
        """Apply legendary character profile."""
        try:
            from legendary_characters import apply_character_profile

            return apply_character_profile(self, character_key)
        except ImportError:
            return False

    def draw(self, surface):
        """Enhanced draw method with Force energy and status effects."""
        # Draw character sprite
        super().draw(surface)

        # Draw Force energy bar above character
        if hasattr(self, "force_energy"):
            bar_width = 40
            bar_height = 4
            bar_x = self.x + (self.size - bar_width) // 2
            bar_y = self.y - 15

            # Background
            pygame.draw.rect(
                surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height)
            )

            # Force energy
            energy_width = int((self.force_energy / self.max_force_energy) * bar_width)
            energy_color = (
                (100, 150, 255) if self.character_type == "jedi" else (255, 100, 100)
            )
            pygame.draw.rect(
                surface, energy_color, (bar_x, bar_y, energy_width, bar_height)
            )

        # Draw character name
        if hasattr(self, "character_name"):
            font = pygame.font.Font(None, 20)
            name_text = font.render(self.character_name, True, WHITE)
            name_x = self.x + (self.size - name_text.get_width()) // 2
            name_y = self.y - 35
            surface.blit(name_text, (name_x, name_y))

        # Draw status effects
        if hasattr(self, "stunned") and self.stunned > 0:
            # Draw stun effect
            for i in range(3):
                angle = (pygame.time.get_ticks() + i * 120) * 0.01
                star_x = self.x + self.size // 2 + math.cos(angle) * 20
                star_y = self.y + self.size // 2 + math.sin(angle) * 20
                pygame.draw.circle(
                    surface, (255, 255, 0), (int(star_x), int(star_y)), 3
                )

        # Draw blocking effect
        if hasattr(self, "is_blocking") and self.is_blocking:
            # Draw defensive aura
            center_x = self.x + self.size // 2
            center_y = self.y + self.size // 2
            for radius in range(30, 50, 5):
                alpha = 100 - (radius - 30) * 10
                temp_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                block_color = (
                    (100, 150, 255, alpha)
                    if self.character_type == "jedi"
                    else (255, 100, 100, alpha)
                )
                pygame.draw.circle(temp_surf, block_color, (radius, radius), radius, 2)
                surface.blit(temp_surf, (center_x - radius, center_y - radius))

    def switch_weapon(self, key):
        """Switch to blaster only (shotgun removed)."""
        if key == pygame.K_1 or key == pygame.K_KP1:
            self.weapon = WEAPON_BLASTER

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
        """Draw the animated player sprite based on movement state and character type."""
        from src.sprite_system import sprite_manager, animation_manager

        # Determine animation state
        if self.knockback_timer > 0:
            pose = "jump"
        elif self.is_jumping:
            pose = "jump"
        elif self._is_moving():
            pose = "walk"
        else:
            pose = "idle"

        # Get character-specific sprite
        if self.character_type in ["jedi", "sith"]:
            # Use Star Wars character sprites
            sprite = sprite_manager.get_character_sprite(
                self.character_type, self.size, pose, 0, self.facing_right
            )
            surface.blit(sprite, (self.x, self.y))
        else:
            # Use default soldier animation system for regular soldiers
            name = "player2" if self.player_id == 2 else "player"
            anim_key = f"{name}_{pose}"
            # Register animation if not already
            if anim_key not in animation_manager.animations:
                frames = sprite_manager.animated_sprites[anim_key]
                animation_manager.create_animation(anim_key, frames, frame_duration=6)
            # Set animation state
            animation_manager.set_animation_state(id(self), anim_key)
            # Get current frame
            frame = animation_manager.get_current_frame(id(self))
            # Always use animated sprite, never fallback to block
            if frame is not None:
                if not self.facing_right:
                    frame = pygame.transform.flip(frame, True, False)
                surface.blit(frame, (self.x, self.y))

    def _is_moving(self):
        # Simple check for movement (could be improved for diagonal)
        keys = pygame.key.get_pressed()
        if self.player_id == 1:
            return keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_s]
        else:
            return keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_DOWN]


class Enemy(Entity):
    """Enhanced Enemy AI entity with Force powers and intelligent combat."""

    def __init__(self, x, y, character_type="sith"):
        """Initialize an enemy with character type."""
        super().__init__(x, y, ENEMY_SIZE, ENEMY_COLOR)
        self.health = ENEMY_MAX_HEALTH
        self.max_health = ENEMY_MAX_HEALTH
        self.character_type = character_type  # 'jedi', 'sith', or 'soldier'

        # Enhanced Force and combat systems
        self.max_force_energy = 80
        self.force_energy = self.max_force_energy
        self.force_regen_rate = 0.8
        self.force_power_bonus = 1.0

        # Lightsaber combat
        self.lightsaber_cooldown = 0
        self.lightsaber_damage_bonus = 0
        self.is_blocking = False
        self.stunned = 0

        # Legendary character support
        self.character_name = "Dark Warrior"
        self.character_description = "A powerful Force user"
        self.special_abilities = []

        # AI behavior
        self.jump_timer = 0
        self.jump_interval = 120
        self.force_power_timer = 0
        self.combat_mode = "ranged"  # "ranged", "melee", "force"

        # Knockback system
        self.knockback_timer = 0
        self.knockback_dx = 0
        self.knockback_dy = 0

    def draw(self, surface):
        """Draw the animated enemy sprite based on movement state and character type."""
        from src.sprite_system import sprite_manager, animation_manager

        # Determine animation state
        if self.knockback_timer > 0:
            pose = "attack"
        elif self.velocity_y < 0:
            pose = "attack"
        elif abs(self.velocity_y) > 1:
            pose = "walk"
        else:
            pose = "idle"

        # Get character-specific sprite
        if self.character_type in ["jedi", "sith"]:
            # Use Star Wars character sprites
            sprite = sprite_manager.get_character_sprite(
                self.character_type,
                self.size,
                pose,
                0,
                True,  # Always face right for enemies
            )
            surface.blit(sprite, (self.x, self.y))
        else:
            # Use default enemy animation system for regular soldiers
            anim_key = f"enemy_{pose}"
            if anim_key not in animation_manager.animations:
                frames = sprite_manager.animated_sprites[anim_key]
                animation_manager.create_animation(anim_key, frames, frame_duration=6)
            animation_manager.set_animation_state(id(self), anim_key)
            frame = animation_manager.get_current_frame(id(self))
            # Always use animated sprite, never fallback to block
            if frame is not None:
                surface.blit(frame, (self.x, self.y))

    def update(self, player, platforms, difficulty):
        """Enhanced enemy AI behavior with Force powers and intelligent combat."""
        # Handle stunning
        if self.stunned > 0:
            self.stunned -= 1
            return

        # Force energy regeneration
        if self.force_energy < self.max_force_energy:
            self.force_energy = min(
                self.max_force_energy, self.force_energy + self.force_regen_rate * 0.1
            )

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
            # Enhanced AI with multiple combat modes
            self._enhanced_ai_behavior(player, difficulty_config)

        # Apply gravity and platform collisions
        self._apply_gravity_and_platforms(platforms)

        # Update collision rectangle
        self.update_rect()

    def _enhanced_ai_behavior(self, player, difficulty_config):
        """Enhanced AI with Force powers and tactical behavior."""
        distance_to_player = math.sqrt(
            (player.x - self.x) ** 2 + (player.y - self.y) ** 2
        )

        # Determine combat mode based on distance and Force energy
        if distance_to_player < 80 and self.force_energy > 30:
            self.combat_mode = "melee"
        elif distance_to_player < 200 and self.force_energy > 50:
            self.combat_mode = "force"
        else:
            self.combat_mode = "ranged"

        # Execute behavior based on combat mode
        if self.combat_mode == "melee":
            self._melee_behavior(player, difficulty_config)
        elif self.combat_mode == "force":
            self._force_power_behavior(player)
        else:
            self._ranged_behavior(player, difficulty_config)

    def _melee_behavior(self, player, difficulty_config):
        """Melee combat behavior - move close and use lightsaber."""
        enemy_speed = difficulty_config["enemy_speed"] * 1.5

        # Move towards player aggressively
        if player.x > self.x + 10:
            self.x += enemy_speed
        elif player.x < self.x - 10:
            self.x -= enemy_speed

        # Attempt lightsaber attack if close enough
        if abs(player.x - self.x) < 60 and abs(player.y - self.y) < 60:
            try:
                from lightsaber_combat import lightsaber_combat

                if not hasattr(self, "lightsaber_cooldown"):
                    self.lightsaber_cooldown = 0
                if self.lightsaber_cooldown <= 0:
                    lightsaber_combat.start_attack(self, player.x, player.y)
                    self.lightsaber_cooldown = 60
            except ImportError:
                pass

    def _force_power_behavior(self, player):
        """Force power behavior - use Force abilities."""
        self.force_power_timer += 1

        if self.force_power_timer > 120:  # Use Force power every 2 seconds
            self.force_power_timer = 0

            # Choose Force power based on character type
            if self.character_type == "sith" and self.force_energy >= 40:
                try:
                    from force_powers import force_manager

                    # Use Force Lightning
                    force_manager.use_power(
                        "force_lightning", self, player.x, player.y, [player]
                    )
                except ImportError:
                    pass
            elif self.character_type == "jedi" and self.force_energy >= 25:
                try:
                    from force_powers import force_manager

                    # Use Force Push
                    force_manager.use_power(
                        "force_push", self, player.x, player.y, [player]
                    )
                except ImportError:
                    pass

    def _ranged_behavior(self, player, difficulty_config):
        """Ranged combat behavior - maintain distance and shoot."""
        enemy_speed = difficulty_config["enemy_speed"]
        distance_x = abs(player.x - self.x)

        # Maintain optimal distance (not too close, not too far)
        if distance_x < 150:
            # Too close, back away
            if player.x > self.x:
                self.x -= enemy_speed
            else:
                self.x += enemy_speed
        elif distance_x > 300:
            # Too far, move closer
            if player.x > self.x:
                self.x += enemy_speed
            else:
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

    def __init__(self, x, y, dx, owner_id):
        """Initialize a bullet."""
        self.x = x
        self.y = y
        self.dx = dx
        self.owner_id = owner_id  # 1 for player1, 2 for player2, 0 for enemy

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
        """Draw the bullet using enhanced sprite only."""
        from src.sprite_system import sprite_manager

        if self.owner_id == 1:
            sprite = sprite_manager.get_sprite("player_bullet")
        elif self.owner_id == 2:
            sprite = sprite_manager.get_sprite("player2_bullet")
        else:
            sprite = sprite_manager.get_sprite("bullet")
        # Always use enhanced sprite, never fallback to block
        if sprite:
            surface.blit(sprite, (self.x - 2, self.y - 1))

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
