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

    def __init__(self, screen, game_engine=None):
        """Initialize the menu manager."""
        self.screen = screen
        self.game_engine = game_engine

    def _transform_mouse_pos(self, mouse_pos):
        """Transform mouse coordinates for fullscreen scaling."""
        if self.game_engine and self.game_engine.fullscreen:
            mouse_x, mouse_y = mouse_pos
            # Transform from screen coordinates to game surface coordinates
            scaled_mouse_x = int(
                (mouse_x - self.game_engine.offset_x) / self.game_engine.scale_factor
            )
            scaled_mouse_y = int(
                (mouse_y - self.game_engine.offset_y) / self.game_engine.scale_factor
            )
            # Clamp to game surface bounds
            scaled_mouse_x = max(0, min(WINDOW_WIDTH, scaled_mouse_x))
            scaled_mouse_y = max(0, min(WINDOW_HEIGHT, scaled_mouse_y))
            return (scaled_mouse_x, scaled_mouse_y)
        return mouse_pos

    def show_start_and_difficulty_menu(self):
        """
        Show the enhanced start menu and difficulty selection.

        Returns:
            tuple: (two_player_mode, difficulty)
        """
        while True:
            self.screen.fill(WHITE)

            # Game title
            title_font = pygame.font.SysFont(None, 48)
            title_text = title_font.render("2D Platform Shooter", True, BLACK)
            self.screen.blit(
                title_text, ((WINDOW_WIDTH - title_text.get_width()) // 2, 50)
            )

            # Subtitle with enhancement info
            subtitle_font = pygame.font.SysFont(None, 24)
            subtitle_text = subtitle_font.render(
                "Enhanced with Visual Effects!", True, DARK_GRAY
            )
            self.screen.blit(
                subtitle_text, ((WINDOW_WIDTH - subtitle_text.get_width()) // 2, 90)
            )

            # Draw start menu buttons with enhanced styling
            start_button_rect = draw_button(
                self.screen,
                "Single Player",
                (WINDOW_WIDTH - 160) // 2,
                WINDOW_HEIGHT // 2 - 60,
                160,
                40,
                button_color=LIGHT_GREEN,
                text_color=BLACK,
            )
            two_player_button_rect = draw_button(
                self.screen,
                "2 Player Mode",
                (WINDOW_WIDTH - 160) // 2,
                WINDOW_HEIGHT // 2 + 10,
                160,
                40,
                button_color=LIGHT_GRAY,
                text_color=BLACK,
            )

            # Instructions at bottom
            instruction_font = pygame.font.SysFont(None, 20)
            instructions = [
                "Controls:",
                "Single Player: WASD + Space + Mouse",
                "2 Player: WASD+E vs Arrows+Numpad0",
                "Press R during game for quick rematch!",
                "Press F11 for fullscreen toggle",
            ]

            for i, instruction in enumerate(instructions):
                color = BLACK if i == 0 else GRAY
                inst_text = instruction_font.render(instruction, True, color)
                self.screen.blit(inst_text, (10, WINDOW_HEIGHT - 120 + i * 22))

            # Use game engine's scaling display method
            if self.game_engine:
                self.game_engine._display_menu_with_scaling()
            else:
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11 and self.game_engine:
                        # Toggle fullscreen from menu
                        self.game_engine.toggle_fullscreen()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = self._transform_mouse_pos(pygame.mouse.get_pos())

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

            # Use game engine's scaling display method
            if self.game_engine:
                self.game_engine._display_menu_with_scaling()
            else:
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = self._transform_mouse_pos(pygame.mouse.get_pos())
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
        Display the game over screen with three options.

        Args:
            winner_title (str): Title of the winner

        Returns:
            str: 'rematch' for same battle, 'home' for home screen, 'quit' to exit
        """
        font_over = pygame.font.SysFont(None, 48)
        font_subtitle = pygame.font.SysFont(None, 24)

        while True:
            self.screen.fill(WHITE)

            # Game over title
            over_text = font_over.render(
                f"Game Over! Winner: {winner_title}", True, BLACK
            )
            self.screen.blit(
                over_text,
                ((WINDOW_WIDTH - over_text.get_width()) // 2, WINDOW_HEIGHT // 2 - 100),
            )

            # Subtitle
            subtitle_text = font_subtitle.render(
                "Choose your next action:", True, DARK_GRAY
            )
            self.screen.blit(
                subtitle_text,
                (
                    (WINDOW_WIDTH - subtitle_text.get_width()) // 2,
                    WINDOW_HEIGHT // 2 - 60,
                ),
            )

            # Three buttons with enhanced styling
            rematch_rect = draw_button(
                self.screen,
                "Rematch",
                (WINDOW_WIDTH - 160) // 2,
                WINDOW_HEIGHT // 2 - 20,
                160,
                40,
                button_color=LIGHT_GREEN,
                text_color=BLACK,
            )

            home_rect = draw_button(
                self.screen,
                "Home Screen",
                (WINDOW_WIDTH - 160) // 2,
                WINDOW_HEIGHT // 2 + 30,
                160,
                40,
                button_color=LIGHT_GRAY,
                text_color=BLACK,
            )

            quit_rect = draw_button(
                self.screen,
                "Quit Game",
                (WINDOW_WIDTH - 160) // 2,
                WINDOW_HEIGHT // 2 + 80,
                160,
                40,
                button_color=DARK_RED,
                text_color=WHITE,
            )

            # Draw hotkey hints
            hint_font = pygame.font.SysFont(None, 20)
            hints = [
                "Press R for Rematch",
                "Press H for Home Screen",
                "Press Q or ESC to Quit",
                "Press F11 for Fullscreen",
            ]

            for i, hint in enumerate(hints):
                hint_text = hint_font.render(hint, True, GRAY)
                self.screen.blit(hint_text, (10, WINDOW_HEIGHT - 100 + i * 22))

            # Use game engine's scaling display method
            if self.game_engine:
                self.game_engine._display_menu_with_scaling()
            else:
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = self._transform_mouse_pos(pygame.mouse.get_pos())

                    if rematch_rect.collidepoint(mouse_pos):
                        return "rematch"
                    if home_rect.collidepoint(mouse_pos):
                        return "home"
                    if quit_rect.collidepoint(mouse_pos):
                        return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "rematch"
                    if event.key == pygame.K_h:
                        return "home"
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return "quit"
                    if event.key == pygame.K_F11 and self.game_engine:
                        # Toggle fullscreen from game over menu
                        self.game_engine.toggle_fullscreen()
