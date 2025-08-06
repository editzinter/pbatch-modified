from clashroyalebuildabot import Cards
from clashroyalebuildabot.actions.generic.action import Action


class ArchersAction(Action):
    CARD = Cards.ARCHERS

    def calculate_score(self, state):
        # More aggressive - play Archers when we have 3+ elixir, not just at 10
        score = [0.7] if state.numbers.elixir.number >= 3 else [0]
        for det in state.enemies:
            lhs = det.position.tile_x <= 8 and self.tile_x == 7
            rhs = det.position.tile_x > 8 and self.tile_x == 10
            if self.tile_y < det.position.tile_y <= 14 and (lhs or rhs):
                score = [1, self.tile_y - det.position.tile_y]
        return score
