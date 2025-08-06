import math

from clashroyalebuildabot import Cards
from clashroyalebuildabot.actions.generic.action import Action


class MusketeerAction(Action):
    CARD = Cards.MUSKETEER

    def calculate_score(self, state):
        """
        Musketeer prioritizes air defense and long-range support
        Priority: Air Defense > Ground Defense > Support Attack
        """
        
        air_threats = 0
        ground_threats_close = 0
        enemies_in_range = 0
        urgent_defense_needed = False
        
        for det in state.enemies:
            distance = math.hypot(
                det.position.tile_x - self.tile_x,
                det.position.tile_y - self.tile_y,
            )
            
            # AIR DEFENSE: Highest priority - flying units
            if hasattr(det.unit, 'is_air') and det.unit.is_air:
                if distance <= 6:  # Musketeer range
                    air_threats += 2  # High priority for air defense
                    if det.position.tile_y < 14:  # Air unit threatening our side
                        urgent_defense_needed = True
            
            # GROUND DEFENSE: Close enemies on our side
            elif det.position.tile_y < 16:  # On our side
                if distance <= 5:
                    ground_threats_close += 1
                    if det.position.tile_y < 10:  # Very close to our towers
                        urgent_defense_needed = True
            
            # GENERAL TARGET: Any enemy in Musketeer's effective range
            if 3 <= distance <= 7:  # Musketeer's optimal range
                enemies_in_range += 1
        
        # URGENT AIR DEFENSE: Must deal with flying threats immediately
        if air_threats > 0 and urgent_defense_needed:
            # Prioritize defensive/support positions for air defense
            defensive_tiles = {(8, 9), (9, 9), (7, 10), (10, 10), (8, 10), (9, 10), (8, 11), (9, 11)}
            if (self.tile_x, self.tile_y) in defensive_tiles:
                return [3.0]  # Maximum priority for air defense
            return [2.5]  # High priority even if not ideally positioned
        
        # STANDARD AIR DEFENSE: Flying units in range
        if air_threats > 0:
            return [2.0]
        
        # CLOSE GROUND DEFENSE: Enemies threatening our towers
        if ground_threats_close > 0 and urgent_defense_needed:
            defensive_tiles = {(8, 9), (9, 9), (7, 10), (10, 10), (8, 10), (9, 10)}
            if (self.tile_x, self.tile_y) in defensive_tiles:
                return [1.8]
            return [1.5]
        
        # SUPPORT FIRE: Enemies in range but not urgent threat
        if enemies_in_range > 0:
            # Check if position gives good coverage
            support_tiles = {(8, 9), (9, 9), (7, 10), (10, 10), (8, 12), (9, 12)}
            if (self.tile_x, self.tile_y) in support_tiles:
                return [1.2]
            return [0.8]
        
        # PROACTIVE PLACEMENT: High elixir and good position
        if state.numbers.elixir.number >= 7:
            support_tiles = {(8, 9), (9, 9), (8, 10), (9, 10)}
            if (self.tile_x, self.tile_y) in support_tiles:
                return [0.6]  # Proactive defense positioning
        
        return [0]
