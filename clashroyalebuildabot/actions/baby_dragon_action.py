import math

from clashroyalebuildabot import Cards
from clashroyalebuildabot.actions.generic.action import Action


class BabyDragonAction(Action):
    CARD = Cards.BABY_DRAGON

    def calculate_score(self, state):
        # More aggressive - play Baby Dragon against enemies in wider range
        for det in state.enemies:
            distance = math.hypot(
                det.position.tile_x - self.tile_x,
                det.position.tile_y - self.tile_y,
            )
            # Expanded range - play against enemies 3-8 tiles away
            if 3 < distance < 8:
                return [1]
            if distance < 3:
                return [0]
        # Play proactively when we have high elixir (air support)
        if state.numbers.elixir.number >= 8:
            return [0.6]
        return [0]
