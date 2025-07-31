"""
Game Menus

This module handles all game menus including the start menu,
difficulty selection, and game over screen.
"""

import pygame
from config import *
from utils import draw_button


class MenuManager:
    """Manages all game menus and user interface screens."""

    def __init__(self, screen):
        """Initialize the menu manager."""
        self.screen = screen

    def show_start_and_difficulty_menu(self):
        """
        Show the start menu and difficulty selection.

        Returns:
            tuple: (two_player_mode, difficulty)
        """
        while True:
            self.screen.fill(WHITE)

            # Draw start menu buttons
            start_button_rect = draw_button(
                self.screen,
                "Start",
                (WINDOW_WIDTH - 160) // 2,
                WINDOW_HEIGHT // 2 - 60,
                160,
                40,
            )
            two_player_button_rect = draw_button(
                self.screen,
                "2 Player",
                (WINDOW_WIDTH - 160) // 2,
                WINDOW_HEIGHT // 2 + 10,
                160,
                40,
            )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if start_button_rect.collidepoint(mouse_pos):
                        # Show difficulty selection for single player
                        difficulty = self._show_difficulty_selection()
                        if difficulty:
                            return False, difficulty

                    if two_player_button_rect.collidepoint(mouse_pos):
                        return True, None

    def _show_difficulty_selection(self):
        """
        Show difficulty selection screen.

        Returns:
            str: Selected difficulty level or None if cancelled
        """
        while True:
            self.screen.fill(WHITE)

            # Title
            font_diff = pygame.font.SysFont(None, UI_LABEL_FONT_SIZE)
            diff_text = font_diff.render("Select Difficulty", True, BLACK)
            self.screen.blit(
                diff_text,
                ((WINDOW_WIDTH - diff_text.get_width()) // 2, WINDOW_HEIGHT // 2 - 60),
            )

            # Difficulty buttons
            difficulties = ["Easy", "Medium", "Hard", "Master"]
            button_width = 160
            button_height = 60
            button_spacing = 32
            buttons = self.draw_difficulty_menu(
                self.screen,
                font_diff,
                difficulties,
                button_width,
                button_height,
                button_spacing,
            )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for button_rect, difficulty in buttons:
                        if button_rect.collidepoint(mouse_pos):
                            return difficulty

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None

    def draw_difficulty_menu(
        self, screen, font, difficulties, button_width, button_height, button_spacing
    ):
        """
        Draws the difficulty selection menu, centering the buttons horizontally.
        """
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        num_buttons = len(difficulties)
        total_width = num_buttons * button_width + (num_buttons - 1) * button_spacing
        start_x = (screen_width - total_width) // 2
        y = screen_height // 2 - button_height // 2

        buttons = []
        for i, difficulty in enumerate(difficulties):
            x = start_x + i * (button_width + button_spacing)
            rect = pygame.Rect(x, y, button_width, button_height)
            buttons.append((rect, difficulty))
            # Draw button background
            pygame.draw.rect(screen, (180, 180, 180), rect)
            # Draw button label
            label = font.render(difficulty, True, (0, 0, 0))
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)
        return buttons

    def show_game_over(self, winner_title):
        """
        Display the game over screen and handle restart.

        Args:
            winner_title (str): Title of the winner

        Returns:
            bool: True if restart clicked, False if quit clicked
        """
        font_over = pygame.font.SysFont(None, 48)

        while True:
            self.screen.fill(WHITE)

            # Game over title
            over_text = font_over.render(
                f"Game Over! Winner: {winner_title}", True, BLACK
            )
            self.screen.blit(
                over_text,
                ((WINDOW_WIDTH - over_text.get_width()) // 2, WINDOW_HEIGHT // 2 - 80),
            )

            # Buttons
            restart_rect = draw_button(
                self.screen,
                "Restart",
                (WINDOW_WIDTH - 160) // 2,
                WINDOW_HEIGHT // 2,
                160,
                40,
            )
            quit_rect = draw_button(
                self.screen,
                "Quit",
                (WINDOW_WIDTH - 160) // 2,
                WINDOW_HEIGHT // 2 + 60,
                160,
                40,
            )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if restart_rect.collidepoint(mouse_pos):
                        return True
                    if quit_rect.collidepoint(mouse_pos):
                        return False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return False
                        return False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return False
