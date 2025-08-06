import math
from clashroyalebuildabot import Cards
from clashroyalebuildabot.actions.generic.action import Action


class MinipekkaAction(Action):
    CARD = Cards.MINIPEKKA

    def calculate_score(self, state):
        """
        Mini P.E.K.K.A as defensive tank killer with secondary bridge option
        Priority: Defense > Bridge Attack
        """
        
        # DEFENSIVE MODE: Tank killer against expensive enemy units
        high_value_enemies_nearby = 0
        close_threats = 0
        
        for enemy in state.enemies:
            # Mini P.E.K.K.A cannot attack air units
            if hasattr(enemy.unit, 'is_air') and enemy.unit.is_air:
                continue

            distance = math.hypot(
                enemy.position.tile_x - self.tile_x,
                enemy.position.tile_y - self.tile_y,
            )
            
            # Check for high-value targets (tanks, expensive units)
            if hasattr(enemy.unit, 'cost') and enemy.unit.cost >= 4:
                if distance <= 5 and enemy.position.tile_y < 16:  # On our side
                    high_value_enemies_nearby += 2  # High priority for tank killing
                elif distance <= 3:  # Very close threat
                    close_threats += 1
        
        # URGENT DEFENSE: Deploy against tanks/expensive units on our side
        if high_value_enemies_nearby > 0:
            # Check if we're in a good defensive position
            defensive_tiles = {(8, 9), (9, 9), (7, 10), (10, 10), (8, 10), (9, 10)}
            if (self.tile_x, self.tile_y) in defensive_tiles:
                return [2.5]  # Very high priority - tank killer role
            return [1.8]  # High priority even if not perfectly positioned
        
        # CLOSE COMBAT: Any enemy very close
        if close_threats > 0:
            return [1.5]
        
        # BRIDGE ATTACK MODE: Only when no defensive needs and good elixir
        bridge_tiles = {(8, 15), (9, 15)}
        if (self.tile_x, self.tile_y) in bridge_tiles:
            if state.numbers.elixir.number >= 7:  # Ensure we have elixir for defense after
                # Check if enemy tower is damaged (prioritize weaker tower)
                left_enemy_hp = state.numbers.left_enemy_princess_hp.number
                right_enemy_hp = state.numbers.right_enemy_princess_hp.number
                
                if self.tile_x == 8 and left_enemy_hp < right_enemy_hp:
                    return [1.0]  # Attack weaker left tower
                elif self.tile_x == 9 and right_enemy_hp < left_enemy_hp:
                    return [1.0]  # Attack weaker right tower
                elif min(left_enemy_hp, right_enemy_hp) < 2000:  # Any tower low
                    return [0.8]  # Opportunistic attack
        
        return [0]  # Don't play if no good defensive or offensive opportunity
