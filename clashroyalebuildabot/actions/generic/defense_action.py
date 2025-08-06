from clashroyalebuildabot.actions.generic.action import Action


class DefenseAction(Action):
    """
    If there are enemies on our side,
    play the card in a defensive position
    """

    def calculate_score(self, state):
        # Allow defensive plays in more positions - not just (8,9) and (9,9)
        # Include positions behind towers for better defensive coverage
        defensive_tiles = {(8, 9), (9, 9), (7, 11), (10, 11), (8, 11), (9, 11), (6, 10), (11, 10)}
        if (self.tile_x, self.tile_y) not in defensive_tiles:
            return [0]

        lhs = 0
        rhs = 0
        urgent_threats = 0
        
        for det in state.enemies:
            # This is a generic action for ground-only attackers (Knight, Cannon).
            # It should ignore air units.
            if hasattr(det.unit, 'is_air') and det.unit.is_air:
                continue

            # Don't ignore enemies on enemy side - they could be building push
            if det.position.tile_y > 16:
                continue  # Still ignore enemies too far away

            # Count threats on our side with urgency based on distance
            distance_to_king = abs(det.position.tile_y - 5)
            if distance_to_king <= 6:  # Within 6 tiles of king tower = urgent
                urgent_threats += 2  # Double weight for close threats
            
            if det.position.tile_x >= 9:
                rhs += 1
            else:
                lhs += 1

        # URGENT DEFENSE: If enemies are close to our towers, defend immediately
        if urgent_threats > 0:
            # Play defensive card immediately when under serious threat
            if (lhs > 0 and self.tile_x <= 8) or (rhs > 0 and self.tile_x >= 9):
                return [2.0]  # Very high priority for urgent defense
            return [1.5]  # High priority even if not perfectly positioned

        # NORMAL DEFENSE: Standard defensive logic
        if lhs == rhs == 0:
            if state.numbers.elixir.number >= 7:  # Lowered from 8 for more proactive defense
                return [0.6]  # Increased from 0.4 - more proactive defense
            return [0]

        # Choose correct side to defend
        if lhs >= rhs and self.tile_x == 9:
            return [0]  # Wrong side

        # Standard defensive positioning
        total_threats = lhs + rhs
        if total_threats > 0:
            return [1.2]  # Slightly higher than before for better defensive priority
        
        return [1]
