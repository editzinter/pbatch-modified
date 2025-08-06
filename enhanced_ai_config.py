#!/usr/bin/env python3
"""
Enhanced AI Configuration for Maximum Performance
Optimized parameters for better gameplay and decision making
"""

import math
from clashroyalebuildabot.namespaces.units import UnitDetection, Position
from clashroyalebuildabot.namespaces.numbers import NumberDetection
from clashroyalebuildabot.namespaces.state import State


def enhanced_heuristic_evaluation(state):
    """
    Advanced heuristic evaluation with more sophisticated scoring
    """
    score = 0.0

    # 1. TOWER HEALTH - Critical importance
    my_left_hp = state.numbers.left_ally_princess_hp.number
    my_right_hp = state.numbers.right_ally_princess_hp.number
    enemy_left_hp = state.numbers.left_enemy_princess_hp.number
    enemy_right_hp = state.numbers.right_enemy_princess_hp.number
    
    my_total_hp = my_left_hp + my_right_hp
    enemy_total_hp = enemy_left_hp + enemy_right_hp
    
    # Tower health difference (massive weight)
    score += (my_total_hp - enemy_total_hp) * 1500
    
    # Bonus for keeping both towers alive
    if my_left_hp > 0 and my_right_hp > 0:
        score += 500
    
    # Penalty for destroyed towers
    if my_left_hp == 0:
        score -= 2000
    if my_right_hp == 0:
        score -= 2000

    # 2. IMMEDIATE THREAT ASSESSMENT
    critical_threats = 0
    moderate_threats = 0
    enemy_push_strength = 0
    
    for enemy in state.enemies:
        distance_to_king = abs(enemy.position.tile_y - 5)
        
        # Critical threats (very close to towers)
        if enemy.position.tile_y < 12 and distance_to_king <= 4:
            threat_level = 5 - distance_to_king  # Closer = higher threat
            critical_threats += threat_level
            score -= 1200 * threat_level  # Massive penalty for close threats
            
        # Moderate threats (on our side)
        elif enemy.position.tile_y < 16:
            moderate_threats += 1
            score -= 400
            
        # Enemy push assessment
        if hasattr(enemy.unit, 'cost'):
            if enemy.position.tile_y < 16:  # Enemy on our side
                enemy_push_strength += enemy.unit.cost

    # 3. DEFENSIVE URGENCY MULTIPLIER
    if critical_threats > 0:
        # Emergency defense mode - heavily prioritize defensive actions
        score -= critical_threats * 800
        # Penalty for having offensive units when defending
        for ally in state.allies:
            if ally.position.tile_y > 16:
                score -= 300  # Don't attack while defending
                
    elif moderate_threats > 0:
        # Standard defense mode
        score -= moderate_threats * 200

    # 4. ELIXIR MANAGEMENT (context-dependent)
    current_elixir = state.numbers.elixir.number
    
    if critical_threats > 0:
        # During defense, having elixir is crucial
        score += min(current_elixir, 8) * 150
    elif moderate_threats > 0:
        # During moderate defense, save some elixir
        score += min(current_elixir, 6) * 100
    else:
        # When safe, elixir can be used for offense
        if current_elixir >= 8:
            score += 200  # Bonus for efficient elixir use
        score += current_elixir * 40

    # 5. BOARD CONTROL AND POSITIONING
    ally_board_value = 0
    enemy_board_value = 0
    ally_offensive_power = 0
    ally_defensive_power = 0
    
    for ally in state.allies:
        if hasattr(ally.unit, 'cost'):
            ally_board_value += ally.unit.cost
            
            # Offensive positioning bonus (only when not defending)
            if ally.position.tile_y > 16 and critical_threats == 0:
                ally_offensive_power += ally.unit.cost
                score += 120  # Bonus for good offensive positioning
                
            # Defensive positioning bonus
            elif ally.position.tile_y <= 16:
                ally_defensive_power += ally.unit.cost
                if moderate_threats > 0 or critical_threats > 0:
                    score += 100  # Bonus for defensive positioning when needed
    
    for enemy in state.enemies:
        if hasattr(enemy.unit, 'cost'):
            enemy_board_value += enemy.unit.cost
    
    # Board presence advantage
    score += (ally_board_value - enemy_board_value) * 80

    # 6. STRATEGIC POSITIONING BONUSES
    # Reward troops in optimal defensive positions
    defensive_tiles = {(8, 9), (9, 9), (7, 10), (10, 10), (8, 10), (9, 10)}
    for ally in state.allies:
        if (ally.position.tile_x, ally.position.tile_y) in defensive_tiles:
            if moderate_threats > 0 or critical_threats > 0:
                score += 150  # Bonus for good defensive positioning
            else:
                score += 50   # Small bonus even when not defending

    # 7. SPELL VALUE CALCULATION
    # Bonus for having spells available during pushes
    if enemy_push_strength >= 8:  # Big enemy push
        score += current_elixir * 20  # Extra value for spells

    return score


def enhanced_mcts_selection(node, exploration_weight=1.2):
    """
    Enhanced UCB1 formula with better exploration/exploitation balance
    """
    if not node.children:
        return None
        
    best_child = max(
        node.children,
        key=lambda c: (
            (c.value / c.visits) + 
            exploration_weight * math.sqrt(2 * math.log(node.visits) / c.visits) +
            0.1 * math.sqrt(c.visits)  # Small bonus for well-explored paths
        )
    )
    return best_child


def enhanced_action_filtering(actions, state):
    """
    Filter actions to remove obviously bad moves before MCTS
    """
    if not actions:
        return actions
    
    filtered_actions = []
    current_elixir = state.numbers.elixir.number
    
    # Check for immediate threats
    immediate_threats = sum(1 for enemy in state.enemies 
                          if enemy.position.tile_y < 12)
    
    for action in actions:
        # Always allow cheap defensive cards during threats
        if immediate_threats > 0:
            card = state.cards[action.index + 1]
            if hasattr(card, 'cost') and card.cost <= 4:
                # Prioritize defensive positions
                defensive_tiles = {(8, 9), (9, 9), (7, 10), (10, 10)}
                if (action.tile_x, action.tile_y) in defensive_tiles:
                    filtered_actions.append(action)
                    continue
        
        # Don't play expensive cards with low elixir during threats
        if immediate_threats > 0:
            card = state.cards[action.index + 1]
            if hasattr(card, 'cost') and card.cost >= 5 and current_elixir < 7:
                continue  # Skip expensive cards during defense
        
        # Don't attack enemy side when we have threats on our side
        if immediate_threats > 0 and action.tile_y > 16:
            continue  # Skip offensive moves during defense
            
        filtered_actions.append(action)
    
    return filtered_actions if filtered_actions else actions


# Configuration for enhanced AI
ENHANCED_AI_CONFIG = {
    'heuristic_function': enhanced_heuristic_evaluation,
    'selection_function': enhanced_mcts_selection,
    'action_filter': enhanced_action_filtering,
    'mcts_time_limit': 250,  # Balanced performance
    'exploration_weight': 1.2,
    'simulation_depth': 3,
    'confidence_threshold': 0.15,  # Lower for better detection
}
