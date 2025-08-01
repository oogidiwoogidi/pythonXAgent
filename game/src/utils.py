"""
Utility Functions

This module contains utility functions for common game operations
such as health bar rendering, platform generation, and UI elements.
"""

import pygame
import random
import array
import math
import os
from config import *


def get_health_color(health, max_health):
    """
    Return the appropriate color based on health percentage.

    Args:
        health (int): Current health value
        max_health (int): Maximum health value

    Returns:
        tuple: RGB color tuple
    """
    percent = health / max_health
    if percent > 0.7:
        return LIGHT_GREEN
    elif percent > 0.4:
        return GOLD
    elif percent > 0.15:
        return ORANGE
    else:
        return DARK_RED


def draw_health_bar(surface, x, y, health, max_health):
    """
    Draw a health bar at the specified position.

    Args:
        surface (pygame.Surface): Surface to draw on
        x (int): X coordinate
        y (int): Y coordinate
        health (int): Current health
        max_health (int): Maximum health
    """
    bar_width = 100
    bar_height = 12
    health_ratio = max(0, health) / max_health
    color = get_health_color(health, max_health)

    # Background
    pygame.draw.rect(surface, DARK_GRAY, (x, y, bar_width, bar_height))
    # Health
    pygame.draw.rect(surface, color, (x, y, int(bar_width * health_ratio), bar_height))
    # Border
    pygame.draw.rect(surface, BLACK, (x, y, bar_width, bar_height), 2)


def draw_labeled_health_bar(surface, x, y, health, max_health, label):
    """
    Draw a labeled health bar with text above it.

    Args:
        surface (pygame.Surface): Surface to draw on
        x (int): X coordinate
        y (int): Y coordinate
        health (int): Current health
        max_health (int): Maximum health
        label (str): Label text
    """
    draw_health_bar(surface, x, y, health, max_health)
    font_label = pygame.font.SysFont(None, UI_LABEL_FONT_SIZE)
    text = f"{label}: {health}/{max_health}"
    text_surface = font_label.render(text, True, WHITE)
    surface.blit(text_surface, (x, y - 18))


def draw_x_above(surface, x, y, size):
    """
    Draw a red 'X' above an entity to indicate defeat.

    Args:
        surface (pygame.Surface): Surface to draw on
        x (int): Entity X coordinate
        y (int): Entity Y coordinate
        size (int): Entity size
    """
    center_x = x + size // 2
    top_y = y - 18
    font_x = pygame.font.SysFont(None, 32)
    x_surface = font_x.render("X", True, DARK_RED)
    surface.blit(x_surface, (center_x - x_surface.get_width() // 2, top_y))


def break_into_pieces(surface, x, y, size, color):
    """
    Display a simple explosion effect by breaking the entity into pieces.

    Args:
        surface (pygame.Surface): Surface to draw on
        x (int): Entity X coordinate
        y (int): Entity Y coordinate
        size (int): Entity size
        color (tuple): Entity color
    """
    for _ in range(12):
        piece_x = x + random.randint(0, size)
        piece_y = y + random.randint(0, size)
        piece_size = random.randint(4, 10)
        pygame.draw.rect(surface, color, (piece_x, piece_y, piece_size, piece_size))


def draw_button(
    surface,
    text,
    x,
    y,
    width,
    height,
    button_color=LIGHT_GRAY,
    text_color=BLACK,
    border_color=BLACK,
):
    """
    Draw a button and return its rectangle for collision detection.

    Args:
        surface (pygame.Surface): Surface to draw on
        text (str): Button text
        x (int): X coordinate
        y (int): Y coordinate
        width (int): Button width
        height (int): Button height
        button_color (tuple): Background color of the button
        text_color (tuple): Color of the text
        border_color (tuple): Color of the border

    Returns:
        pygame.Rect: Button rectangle
    """
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, button_color, button_rect)
    pygame.draw.rect(surface, border_color, button_rect, 2)

    font_btn = pygame.font.SysFont(None, UI_BUTTON_FONT_SIZE)
    text_surface = font_btn.render(text, True, text_color)
    text_x = x + (width - text_surface.get_width()) // 2
    text_y = y + (height - text_surface.get_height()) // 2
    surface.blit(text_surface, (text_x, text_y))

    return button_rect


def generate_random_platforms():
    """
    Generate a list of random platforms for the map, ensuring no overlap
    and at least 2 blocks vertical separation.

    Returns:
        list: List of pygame.Rect objects representing platforms
    """
    platforms = []
    attempts = 0
    min_vertical_gap = 2 * BLOCK_SIZE
    max_attempts = PLATFORM_COUNT * 30

    while len(platforms) < PLATFORM_COUNT and attempts < max_attempts:
        width = random.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH)
        x = random.randint(0, WINDOW_WIDTH - width)
        y = random.randint(80, WINDOW_HEIGHT - 120)
        new_platform = pygame.Rect(x, y, width, PLATFORM_HEIGHT)

        # Check for overlaps and minimum vertical gap
        valid_platform = True
        for existing in platforms:
            if (
                new_platform.colliderect(existing)
                or abs(new_platform.top - existing.top) < min_vertical_gap
            ):
                valid_platform = False
                break

        if valid_platform:
            platforms.append(new_platform)

        attempts += 1

    # If we couldn't generate enough platforms, add some at the bottom
    while len(platforms) < PLATFORM_COUNT:
        width = random.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH)
        x = random.randint(0, WINDOW_WIDTH - width)
        y = WINDOW_HEIGHT - PLATFORM_HEIGHT - 10
        new_platform = pygame.Rect(x, y, width, PLATFORM_HEIGHT)

        # Check for overlaps
        valid_platform = True
        for existing in platforms:
            if (
                new_platform.colliderect(existing)
                or abs(new_platform.top - existing.top) < min_vertical_gap
            ):
                valid_platform = False
                break

        if valid_platform:
            platforms.append(new_platform)
        else:
            break  # Avoid infinite loop

    return platforms


def draw_weapon_info(surface, player, x_offset, y_offset):
    """
    Draw weapon information and ammo count for a player.

    Args:
        surface (pygame.Surface): Surface to draw on
        player: Player object
        x_offset (int): X offset from player position
        y_offset (int): Y offset from player position
    """
    font_reload = pygame.font.SysFont(None, UI_RELOAD_FONT_SIZE)

    # Draw weapon type
    weapon_text = font_reload.render("Weapon: Blaster", True, WHITE)
    surface.blit(weapon_text, (player.x + x_offset, player.y + y_offset - 60))

    # Draw reloading status or ammo count
    if player.reloading:
        reload_text = font_reload.render("Reloading...", True, DARK_RED)
        surface.blit(reload_text, (player.x + x_offset, player.y + y_offset - 32))
    else:
        mag_text = font_reload.render(f"Ammo: {player.magazine}", True, WHITE)
        surface.blit(mag_text, (player.x + x_offset, player.y + y_offset - 32))
