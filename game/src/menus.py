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
        # Clear any lingering events to prevent stuck state
        pygame.event.clear()

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

    def show_single_player_character_selection(self):
        """
        Display dedicated single player character selection page.
        Uses A/D keys to navigate between characters and Enter to confirm.

        Returns:
            dict: Character selections {'player1': 'jedi'/'sith', 'ai': 'sith'/'jedi'}
        """
        font_title = pygame.font.SysFont(None, 48)
        font_subtitle = pygame.font.SysFont(None, 32)
        font_instruction = pygame.font.SysFont(None, 24)

        # Import sprite manager to show character previews
        from sprite_system import sprite_manager

        selected_character = "jedi"  # Default selection

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.KEYDOWN:
                    # A key selects Jedi
                    if event.key == pygame.K_a:
                        selected_character = "jedi"
                    # D key selects Sith
                    elif event.key == pygame.K_d:
                        selected_character = "sith"
                    # Enter confirms selection
                    elif event.key == pygame.K_RETURN:
                        ai_character = (
                            "sith" if selected_character == "jedi" else "jedi"
                        )
                        return {"player1": selected_character, "ai": ai_character}
                    # Escape to go back
                    elif event.key == pygame.K_ESCAPE:
                        return None

            self.screen.fill((20, 20, 40))  # Dark space background

            # Title
            title_text = font_title.render("Choose Your Destiny", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
            self.screen.blit(title_text, title_rect)

            # Subtitle
            subtitle_text = font_subtitle.render(
                f"Difficulty: {self.game_engine.difficulty}", True, (200, 200, 200)
            )
            subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
            self.screen.blit(subtitle_text, subtitle_rect)

            # Character previews with larger sprites
            jedi_sprite = sprite_manager.get_character_sprite("jedi", 120)
            sith_sprite = sprite_manager.get_character_sprite("sith", 120)

            # Jedi side (left)
            jedi_x = WINDOW_WIDTH // 4
            jedi_y = 180

            # Highlight selected character with white border
            if selected_character == "jedi":
                # Draw white highlight border
                pygame.draw.rect(
                    self.screen,
                    (255, 255, 255),
                    (jedi_x - 70, jedi_y - 10, 140, 160),
                    4,
                )

            self.screen.blit(jedi_sprite, (jedi_x - 60, jedi_y))

            jedi_title = font_subtitle.render("JEDI", True, (100, 150, 255))
            jedi_title_rect = jedi_title.get_rect(center=(jedi_x, jedi_y + 180))
            self.screen.blit(jedi_title, jedi_title_rect)

            jedi_desc = font_instruction.render(
                "• Blue Lightsaber", True, (150, 150, 255)
            )
            self.screen.blit(jedi_desc, (jedi_x - 60, jedi_y + 200))
            jedi_desc2 = font_instruction.render(
                "• Light Side of the Force", True, (150, 150, 255)
            )
            self.screen.blit(jedi_desc2, (jedi_x - 60, jedi_y + 220))

            # Sith side (right)
            sith_x = 3 * WINDOW_WIDTH // 4
            sith_y = 180

            # Highlight selected character with white border
            if selected_character == "sith":
                # Draw white highlight border
                pygame.draw.rect(
                    self.screen,
                    (255, 255, 255),
                    (sith_x - 70, sith_y - 10, 140, 160),
                    4,
                )

            self.screen.blit(sith_sprite, (sith_x - 60, sith_y))

            sith_title = font_subtitle.render("SITH", True, (255, 100, 100))
            sith_title_rect = sith_title.get_rect(center=(sith_x, sith_y + 180))
            self.screen.blit(sith_title, sith_title_rect)

            sith_desc = font_instruction.render(
                "• Red Lightsaber", True, (255, 150, 150)
            )
            self.screen.blit(sith_desc, (sith_x - 60, sith_y + 200))
            sith_desc2 = font_instruction.render(
                "• Dark Side of the Force", True, (255, 150, 150)
            )
            self.screen.blit(sith_desc2, (sith_x - 60, sith_y + 220))

            # Current selection indicator
            selection_text = font_subtitle.render(
                f"Selected: {selected_character.upper()}", True, (255, 255, 100)
            )
            selection_rect = selection_text.get_rect(center=(WINDOW_WIDTH // 2, 480))
            self.screen.blit(selection_text, selection_rect)

            # Instructions
            instruction1 = font_instruction.render(
                "Use A and D keys to select your character", True, (200, 200, 200)
            )
            instruction1_rect = instruction1.get_rect(center=(WINDOW_WIDTH // 2, 520))
            self.screen.blit(instruction1, instruction1_rect)

            instruction2 = font_instruction.render(
                "Press ENTER to confirm selection", True, (255, 255, 100)
            )
            instruction2_rect = instruction2.get_rect(center=(WINDOW_WIDTH // 2, 545))
            self.screen.blit(instruction2, instruction2_rect)

            instruction3 = font_instruction.render(
                "Press ESCAPE to go back", True, (180, 180, 180)
            )
            instruction3_rect = instruction3.get_rect(center=(WINDOW_WIDTH // 2, 570))
            self.screen.blit(instruction3, instruction3_rect)

            # Use game engine's scaling display method
            if self.game_engine:
                self.game_engine._display_menu_with_scaling()
            else:
                pygame.display.flip()

    def show_character_selection(self, mode="single"):
        """
        Display Star Wars character selection screen.

        Args:
            mode (str): 'single' for single player, 'two' for two player

        Returns:
            dict: Character selections {'player1': 'jedi'/'sith', 'player2': 'jedi'/'sith'}
        """
        font_title = pygame.font.SysFont(None, 48)
        font_subtitle = pygame.font.SysFont(None, 32)
        font_instruction = pygame.font.SysFont(None, 24)

        # Import sprite manager to show character previews
        from sprite_system import sprite_manager

        if mode == "single":
            # Single player mode - choose your character, AI gets opposite
            selected_character = None

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return None

                    if event.type == pygame.KEYDOWN:
                        # A key selects Jedi
                        if event.key == pygame.K_a:
                            return {"player1": "jedi", "ai": "sith"}
                        # D key selects Sith
                        elif event.key == pygame.K_d:
                            return {"player1": "sith", "ai": "jedi"}

                self.screen.fill((20, 20, 40))  # Dark space background

                # Title
                title_text = font_title.render(
                    "Choose Your Destiny", True, (255, 255, 255)
                )
                title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
                self.screen.blit(title_text, title_rect)

                # Subtitle
                subtitle_text = font_subtitle.render(
                    "Single Player Mode", True, (200, 200, 200)
                )
                subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 140))
                self.screen.blit(subtitle_text, subtitle_rect)

                # Character previews
                jedi_sprite = sprite_manager.get_character_sprite("jedi", 80)
                sith_sprite = sprite_manager.get_character_sprite("sith", 80)

                # Jedi side (left)
                jedi_x = WINDOW_WIDTH // 4
                self.screen.blit(jedi_sprite, (jedi_x - 40, 200))

                jedi_title = font_subtitle.render("JEDI", True, (100, 150, 255))
                jedi_title_rect = jedi_title.get_rect(center=(jedi_x, 300))
                self.screen.blit(jedi_title, jedi_title_rect)

                jedi_desc = font_instruction.render(
                    "• Blue Lightsaber", True, (150, 150, 255)
                )
                self.screen.blit(jedi_desc, (jedi_x - 60, 320))
                jedi_desc2 = font_instruction.render(
                    "• Light Side", True, (150, 150, 255)
                )
                self.screen.blit(jedi_desc2, (jedi_x - 60, 340))

                # Sith side (right)
                sith_x = 3 * WINDOW_WIDTH // 4
                self.screen.blit(sith_sprite, (sith_x - 40, 200))

                sith_title = font_subtitle.render("SITH", True, (255, 100, 100))
                sith_title_rect = sith_title.get_rect(center=(sith_x, 300))
                self.screen.blit(sith_title, sith_title_rect)

                sith_desc = font_instruction.render(
                    "• Red Lightsaber", True, (255, 150, 150)
                )
                self.screen.blit(sith_desc, (sith_x - 60, 320))
                sith_desc2 = font_instruction.render(
                    "• Dark Side", True, (255, 150, 150)
                )
                self.screen.blit(sith_desc2, (sith_x - 60, 340))

                # Instructions
                instruction = font_instruction.render(
                    "Press A for Jedi or D for Sith. AI will be your opponent.",
                    True,
                    (200, 200, 200),
                )
                instruction_rect = instruction.get_rect(
                    center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 80)
                )
                self.screen.blit(instruction, instruction_rect)

                # Key hints
                key_hint = font_instruction.render(
                    "A = Jedi (Blue Lightsaber)    D = Sith (Red Lightsaber)",
                    True,
                    (255, 255, 100),
                )
                key_hint_rect = key_hint.get_rect(
                    center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
                )
                self.screen.blit(key_hint, key_hint_rect)

                pygame.display.flip()

        else:  # Two player mode
            # Clear any lingering events to prevent stuck state
            pygame.event.clear()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return None

                    if event.type == pygame.KEYDOWN:
                        # Escape key to go back
                        if event.key == pygame.K_ESCAPE:
                            return None

                        # Player 1 uses WASD - automatically assigns opposite character to Player 2
                        if event.key == pygame.K_a:  # Choose Jedi
                            return {
                                "player1": "jedi",
                                "player2": "sith",
                            }
                        elif event.key == pygame.K_d:  # Choose Sith
                            return {
                                "player1": "sith",
                                "player2": "jedi",
                            }

                self.screen.fill((20, 20, 40))  # Dark space background

                # Title
                title_text = font_title.render(
                    "Choose Your Destinies", True, (255, 255, 255)
                )
                title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
                self.screen.blit(title_text, title_rect)

                # Subtitle
                subtitle_text = font_subtitle.render(
                    "Two Player Mode", True, (200, 200, 200)
                )
                subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
                self.screen.blit(subtitle_text, subtitle_rect)

                # Character previews
                jedi_sprite = sprite_manager.get_character_sprite("jedi", 60)
                sith_sprite = sprite_manager.get_character_sprite("sith", 60)

                # Jedi side (left)
                jedi_x = WINDOW_WIDTH // 4
                self.screen.blit(jedi_sprite, (jedi_x - 30, 180))

                jedi_title = font_subtitle.render("JEDI", True, (100, 150, 255))
                jedi_title_rect = jedi_title.get_rect(center=(jedi_x, 260))
                self.screen.blit(jedi_title, jedi_title_rect)

                # Sith side (right)
                sith_x = 3 * WINDOW_WIDTH // 4
                self.screen.blit(sith_sprite, (sith_x - 30, 180))

                sith_title = font_subtitle.render("SITH", True, (255, 100, 100))
                sith_title_rect = sith_title.get_rect(center=(sith_x, 260))
                self.screen.blit(sith_title, sith_title_rect)

                # Player status indicators - simplified for automatic assignment
                player1_text = font_subtitle.render(
                    "Player 1: Choose with A (Jedi) or D (Sith)",
                    True,
                    (255, 255, 0),
                )
                player1_rect = player1_text.get_rect(center=(WINDOW_WIDTH // 2, 320))
                self.screen.blit(player1_text, player1_rect)

                # Player 2 auto-assignment message
                player2_text = font_subtitle.render(
                    "Player 2: Will automatically get the opposite character",
                    True,
                    (200, 200, 200),
                )
                player2_rect = player2_text.get_rect(center=(WINDOW_WIDTH // 2, 360))
                self.screen.blit(player2_text, player2_rect)

                # Rules
                rule_text = font_instruction.render(
                    "Player 1 chooses, Player 2 gets the opposite automatically!",
                    True,
                    (200, 200, 200),
                )
                rule_rect = rule_text.get_rect(
                    center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)
                )
                self.screen.blit(rule_text, rule_rect)

                # Use game engine's scaling display method
                if self.game_engine:
                    self.game_engine._display_menu_with_scaling()
                else:
                    pygame.display.flip()

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

        # Clear any lingering events to prevent stuck state
        pygame.event.clear()

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
