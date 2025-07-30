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
            easy_rect = draw_button(
                self.screen,
                "Easy",
                (WINDOW_WIDTH - 440) // 2,
                WINDOW_HEIGHT // 2 - 20,
                100,
                32,
            )
            medium_rect = draw_button(
                self.screen,
                "Medium",
                (WINDOW_WIDTH - 120) // 2,
                WINDOW_HEIGHT // 2 - 20,
                100,
                32,
            )
            hard_rect = draw_button(
                self.screen,
                "Hard",
                (WINDOW_WIDTH + 200) // 2,
                WINDOW_HEIGHT // 2 - 20,
                100,
                32,
            )
            master_rect = draw_button(
                self.screen,
                "Master",
                (WINDOW_WIDTH + 520) // 2,
                WINDOW_HEIGHT // 2 - 20,
                100,
                32,
            )

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if easy_rect.collidepoint(mouse_pos):
                        return "Easy"
                    if medium_rect.collidepoint(mouse_pos):
                        return "Medium"
                    if hard_rect.collidepoint(mouse_pos):
                        return "Hard"
                    if master_rect.collidepoint(mouse_pos):
                        return "Master"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None

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
