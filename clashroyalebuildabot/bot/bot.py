import random
import threading
import time

import keyboard
from loguru import logger

from clashroyalebuildabot.constants import ALL_TILES
from clashroyalebuildabot.constants import ALLY_TILES
from clashroyalebuildabot.constants import DISPLAY_CARD_DELTA_X
from clashroyalebuildabot.constants import DISPLAY_CARD_HEIGHT
from clashroyalebuildabot.constants import DISPLAY_CARD_INIT_X
from clashroyalebuildabot.constants import DISPLAY_CARD_WIDTH
from clashroyalebuildabot.constants import DISPLAY_CARD_Y
from clashroyalebuildabot.constants import DISPLAY_HEIGHT
from clashroyalebuildabot.constants import LEFT_PRINCESS_TILES
from clashroyalebuildabot.constants import RIGHT_PRINCESS_TILES
from clashroyalebuildabot.constants import TILE_HEIGHT
from clashroyalebuildabot.constants import TILE_INIT_X
from clashroyalebuildabot.constants import TILE_INIT_Y
from clashroyalebuildabot.constants import TILE_WIDTH
from clashroyalebuildabot.detectors.detector import Detector
from clashroyalebuildabot.emulator.emulator import Emulator
from clashroyalebuildabot.namespaces import Screens
from clashroyalebuildabot.ai.mcts import run_mcts
from clashroyalebuildabot.visualizer import Visualizer
from error_handling import WikifiedError

pause_event = threading.Event()
pause_event.set()
is_paused_logged = False
is_resumed_logged = True


class Bot:
    is_paused_logged = False
    is_resumed_logged = True

    def __init__(self, actions, config):
        self.actions = actions
        self.auto_start = config["bot"]["auto_start_game"]
        self.end_of_game_clicked = False
        self.should_run = True

        cards = [action.CARD for action in actions]
        if len(cards) != 8:
            raise WikifiedError(
                "005", f"Must provide 8 cards but {len(cards)} was given"
            )
        self.cards_to_actions = dict(zip(cards, actions))

        self.visualizer = Visualizer(**config["visuals"])
        self.emulator = Emulator(**config["adb"])
        self.detector = Detector(cards=cards)
        self.state = None
        self.play_action_delay = config.get("ingame", {}).get("play_action", 1)

        # End-game screen handling coordinates (720x1280 resolution)
        self.battle_button_xy = (357.8, 984.2)  # Battle button on lobby screen
        self.primary_ok_button_xy = (360.0, 1157.9)  # Primary OK button (bottom center)
        self.secondary_ok_button_xy = (242.1, 1164.0)  # Secondary OK button (bottom right)

        # End-game handling state
        self.unknown_screen_attempts = 0
        self.max_unknown_screen_attempts = 4
        self.last_unknown_screen_time = 0
        
        # Battle timeout tracking
        self.last_battle_click_time = 0
        self.battle_timeout = 30  # 30 seconds timeout for battle start

        keyboard_thread = threading.Thread(
            target=self._handle_keyboard_shortcut, daemon=True
        )
        keyboard_thread.start()

        if config["bot"]["load_deck"]:
            skip_deck_copy = config["bot"].get("skip_deck_copy", False)
            self.emulator.load_deck(cards, skip_prompt=skip_deck_copy)

    @staticmethod
    def _log_and_wait(prefix, delay):
        suffix = ""
        if delay > 1:
            suffix = "s"
        message = f"{prefix}. Waiting for {delay} second{suffix}."
        logger.info(message)
        time.sleep(delay)

    @staticmethod
    def _handle_keyboard_shortcut():
        while True:
            keyboard.wait("ctrl+p")
            Bot.pause_or_resume()

    @staticmethod
    def pause_or_resume():
        if pause_event.is_set():
            logger.info("Bot paused.")
            pause_event.clear()
            Bot.is_paused_logged = True
            Bot.is_resumed_logged = False
        else:
            logger.info("Bot resumed.")
            pause_event.set()
            Bot.is_resumed_logged = True
            Bot.is_paused_logged = False

    @staticmethod
    def _get_nearest_tile(x, y):
        tile_x = round(((x - TILE_INIT_X) / TILE_WIDTH) - 0.5)
        tile_y = round(
            ((DISPLAY_HEIGHT - TILE_INIT_Y - y) / TILE_HEIGHT) - 0.5
        )
        return tile_x, tile_y

    @staticmethod
    def _get_tile_centre(tile_x, tile_y):
        x = TILE_INIT_X + (tile_x + 0.5) * TILE_WIDTH
        y = DISPLAY_HEIGHT - TILE_INIT_Y - (tile_y + 0.5) * TILE_HEIGHT
        return x, y

    @staticmethod
    def _get_card_centre(card_n):
        x = (
            DISPLAY_CARD_INIT_X
            + DISPLAY_CARD_WIDTH / 2
            + card_n * DISPLAY_CARD_DELTA_X
        )
        y = DISPLAY_CARD_Y + DISPLAY_CARD_HEIGHT / 2
        return x, y

    def _get_valid_tiles(self):
        tiles = ALLY_TILES
        if self.state.numbers.left_enemy_princess_hp.number == 0:
            tiles += LEFT_PRINCESS_TILES
        if self.state.numbers.right_enemy_princess_hp.number == 0:
            tiles += RIGHT_PRINCESS_TILES
        return tiles

    def get_actions(self):
        if not self.state:
            return []
        valid_tiles = self._get_valid_tiles()
        actions = []
        for i in self.state.ready:
            card = self.state.cards[i + 1]
            if self.state.numbers.elixir.number < card.cost:
                continue

            tiles = ALL_TILES if card.target_anywhere else valid_tiles
            card_actions = [
                self.cards_to_actions[card](i, x, y) for (x, y) in tiles
            ]
            actions.extend(card_actions)

        return actions

    def set_state(self):
        screenshot = self.emulator.take_screenshot()
        self.state = self.detector.run(screenshot)
        self.visualizer.run(screenshot, self.state)

    def play_action(self, action):
        card_centre = self._get_card_centre(action.index)
        tile_centre = self._get_tile_centre(action.tile_x, action.tile_y)
        self.emulator.click(*card_centre)
        self.emulator.click(*tile_centre)

    def _handle_play_pause_in_step(self):
        if not pause_event.is_set():
            if not Bot.is_paused_logged:
                logger.info("Bot paused.")
                Bot.is_paused_logged = True
            time.sleep(0.1)
            return
        if not Bot.is_resumed_logged:
            logger.info("Bot resumed.")
            Bot.is_resumed_logged = True

    def step(self):
        self._handle_play_pause_in_step()
        old_screen = self.state.screen if self.state else None
        self.set_state()
        new_screen = self.state.screen
        if new_screen != old_screen:
            logger.info(f"New screen state: {new_screen}")

        # Check for battle timeout (if we clicked battle but never entered game)
        if self.last_battle_click_time > 0 and new_screen not in [Screens.IN_GAME, Screens.LOBBY]:
            time_since_battle = time.time() - self.last_battle_click_time
            if time_since_battle > self.battle_timeout:
                logger.error(f"❌ BATTLE TIMEOUT - no game after {self.battle_timeout} seconds!")
                logger.info("🔄 Restarting Clash Royale due to battle timeout...")
                self._restart_clash_royale()
                self.last_battle_click_time = 0  # Reset timeout
                return

        # Reset battle timeout when we successfully enter game
        if new_screen == Screens.IN_GAME and self.last_battle_click_time > 0:
            self.last_battle_click_time = 0  # Reset timeout since we're now in game

        if new_screen == Screens.UNKNOWN:
            # Handle unknown screen as potential end-game screen
            self._handle_unknown_screen()
            return

        if new_screen == Screens.END_OF_GAME:
            if not self.end_of_game_clicked:
                self.emulator.click(*self.state.screen.click_xy)
                self.end_of_game_clicked = True
                self._log_and_wait("Clicked END_OF_GAME screen", 2)
            return

        # Reset end-game handling state when we're in a known screen
        self.end_of_game_clicked = False
        self.unknown_screen_attempts = 0

        if self.auto_start and new_screen == Screens.LOBBY:
            # Use our specific battle button coordinates
            self.emulator.click(*self.battle_button_xy)
            self.last_battle_click_time = time.time()  # Track when we clicked battle
            self.end_of_game_clicked = False
            self._log_and_wait("Starting game from lobby", 2)
            return

        self._handle_game_step()

    def _handle_game_step(self):
        """
        This is the new AI core. It uses MCTS to decide the best move.
        """
        logger.debug("Running MCTS to find best action...")

        try:
            best_action = run_mcts(self, time_limit_ms=200)  # Increased for better AI quality
        except Exception as e:
            logger.warning(f"MCTS failed: {e}, falling back to original scoring")
            # Fallback to original scoring system
            best_action = self._get_best_action_fallback()

        if best_action is None:
            self._log_and_wait(
                "No good actions available", self.play_action_delay
            )
            return

        self.play_action(best_action)
        self._log_and_wait(
            f"Playing {best_action} (chosen by MCTS)",
            self.play_action_delay,
        )

    def _get_best_action_fallback(self):
        """Fallback to original scoring system if MCTS fails"""
        actions = self.get_actions()
        if not actions:
            return None

        random.shuffle(actions)
        best_score = [0]
        best_action = None
        for action in actions:
            try:
                score = action.calculate_score(self.state)
                if score > best_score:
                    best_action = action
                    best_score = score
            except Exception:
                continue

        return best_action if best_score[0] > 0 else None

    def _restart_clash_royale(self):
        """Restart Clash Royale game using ADB commands"""
        try:
            logger.info("🔄 Stopping Clash Royale...")
            self.emulator.stop_game()
            time.sleep(3)  # Wait for game to stop
            
            logger.info("🚀 Starting Clash Royale...")
            self.emulator.start_game()
            time.sleep(10)  # Wait for game to load
            logger.info("✅ Clash Royale restarted successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to restart Clash Royale: {e}")

    def _handle_unknown_screen(self):
        """
        Handle unknown screen as potential end-game screen with robust retry logic.
        Uses the specific coordinates and retry mechanism you provided.
        """
        current_time = time.time()

        # Reset attempts if it's been a while since last unknown screen
        if current_time - self.last_unknown_screen_time > 10:
            self.unknown_screen_attempts = 0

        self.last_unknown_screen_time = current_time

        if self.unknown_screen_attempts == 0:
            # First attempt: Try primary OK button (bottom center)
            logger.info("Unknown screen detected - trying primary OK button (bottom center)")
            self.emulator.click(*self.primary_ok_button_xy)
            self.unknown_screen_attempts += 1
            self._log_and_wait("Clicked primary OK button, waiting for screen change", 5)

        elif self.unknown_screen_attempts == 1:
            # Second attempt: Try primary OK button again
            logger.info("Still unknown screen - trying primary OK button again")
            self.emulator.click(*self.primary_ok_button_xy)
            self.unknown_screen_attempts += 1
            self._log_and_wait("Clicked primary OK button again, waiting for screen change", 5)

        elif self.unknown_screen_attempts == 2:
            # Third attempt: Try secondary OK button (bottom right)
            logger.info("Still unknown screen - trying secondary OK button (bottom right)")
            self.emulator.click(*self.secondary_ok_button_xy)
            self.unknown_screen_attempts += 1
            self._log_and_wait("Clicked secondary OK button, waiting for screen change", 5)

        elif self.unknown_screen_attempts == 3:
            # Fourth attempt: Try secondary OK button again
            logger.info("Still unknown screen - trying secondary OK button again")
            self.emulator.click(*self.secondary_ok_button_xy)
            self.unknown_screen_attempts += 1
            self._log_and_wait("Clicked secondary OK button again, waiting for screen change", 5)

        elif self.unknown_screen_attempts == 4:
            # Fifth attempt: Try secondary OK button one more time
            logger.info("Still unknown screen - trying secondary OK button third time")
            self.emulator.click(*self.secondary_ok_button_xy)
            self.unknown_screen_attempts += 1
            self._log_and_wait("Clicked secondary OK button third time, waiting for screen change", 5)

        else:
            # If all attempts failed, restart the game automatically
            logger.error("All OK button attempts failed - RESTARTING CLASH ROYALE")
            self._restart_clash_royale()
            self.unknown_screen_attempts = 0
            self._log_and_wait("Game restarted, waiting for app to load", 10)

    def run(self):
        try:
            while self.should_run:
                if not pause_event.is_set():
                    time.sleep(0.1)
                    continue

                self.step()
            logger.info("Thanks for using CRBAB, see you next time!")
        except KeyboardInterrupt:
            logger.info("Thanks for using CRBAB, see you next time!")

    def stop(self):
        self.should_run = False
