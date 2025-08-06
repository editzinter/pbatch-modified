import math
import random
import time
from copy import deepcopy

from clashroyalebuildabot.namespaces.units import UnitDetection, Position
from clashroyalebuildabot.namespaces.numbers import NumberDetection
from clashroyalebuildabot.namespaces.state import State


class MCTSNode:
    def __init__(self, game_state, parent=None, action=None):
        self.game_state = game_state
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.value = 0.0
        self.untried_actions = None

    def get_untried_actions(self, all_possible_actions):
        if self.untried_actions is None:
            self.untried_actions = all_possible_actions
        return self.untried_actions

    def select_child(self, exploration_weight=1.41):
        """Select a child node using the UCB1 formula."""
        best_child = max(self.children,
                         key=lambda c: (c.value / c.visits) + exploration_weight * math.sqrt(
                             2 * math.log(self.visits) / c.visits))
        return best_child

    def expand(self, action, new_state):
        """Expand the tree with a new child node."""
        child = MCTSNode(new_state, parent=self, action=action)
        self.untried_actions.remove(action)
        self.children.append(child)
        return child

    def update(self, result):
        """Backpropagate the simulation result."""
        self.visits += 1
        self.value += result


def get_card_from_action(state, action):
    return state.cards[action.index + 1]


def simulate_action(state, action):
    """Create a hypothetical future state after an action."""
    card = get_card_from_action(state, action)

    # 1. Create new elixir state (decrease elixir)
    new_elixir = NumberDetection(
        bbox=state.numbers.elixir.bbox,
        number=max(0, state.numbers.elixir.number - card.cost)
    )

    # 2. Create new numbers object with updated elixir
    new_numbers = state.numbers.__class__(
        left_enemy_princess_hp=state.numbers.left_enemy_princess_hp,
        right_enemy_princess_hp=state.numbers.right_enemy_princess_hp,
        left_ally_princess_hp=state.numbers.left_ally_princess_hp,
        right_ally_princess_hp=state.numbers.right_ally_princess_hp,
        elixir=new_elixir
    )

    # 3. Add new units to the board (approximation)
    new_allies = list(state.allies)  # Copy existing allies
    for unit_template in card.units:
        # This is a simplified simulation. A more advanced version would
        # predict movement and combat.
        new_unit_pos = Position(bbox=(0, 0, 0, 0), conf=1.0, tile_x=action.tile_x, tile_y=action.tile_y)
        new_unit = UnitDetection(unit_template, new_unit_pos)
        new_allies.append(new_unit)

    # 4. Create new state with updated values
    new_state = State(
        allies=new_allies,
        enemies=list(state.enemies),  # Copy enemies
        numbers=new_numbers,
        cards=state.cards,
        ready=state.ready,
        screen=state.screen
    )

    return new_state


def heuristic_evaluation(state):
    """
    V4: Final version with extreme defensive focus.
    """
    score = 0.0

    # 1. TOWER HEALTH & Desperate Defense Mode
    my_left_hp = state.numbers.left_ally_princess_hp.number
    my_right_hp = state.numbers.right_ally_princess_hp.number
    enemy_left_hp = state.numbers.left_enemy_princess_hp.number
    enemy_right_hp = state.numbers.right_enemy_princess_hp.number

    desperate_defense = my_left_hp == 0 or my_right_hp == 0

    my_total_hp = my_left_hp + my_right_hp
    enemy_total_hp = enemy_left_hp + enemy_right_hp

    score += (my_total_hp - enemy_total_hp) * 300

    if my_left_hp == 0:
        score -= 10000
    if my_right_hp == 0:
        score -= 10000

    # 2. ADVANCED THREAT ASSESSMENT & EXTREME OFFENSIVE PENALTY
    enemy_on_our_side = False
    enemy_push_value = 0
    for enemy in state.enemies:
        if enemy.position.tile_y < 16:
            enemy_on_our_side = True
            threat_multiplier = (16 - enemy.position.tile_y)
            enemy_cost = getattr(enemy.unit, 'cost', 3)
            score -= enemy_cost * threat_multiplier * 250
            enemy_push_value += enemy_cost

    # Extreme penalty for playing troops on opponent's side while defending
    if enemy_on_our_side:
        for ally in state.allies:
            if ally.position.tile_y > 16:
                score -= 20000

    # 3. DEFENSIVE URGENCY & ELIXIR MANAGEMENT
    current_elixir = state.numbers.elixir.number

    if desperate_defense:
        score -= 20000
        for ally in state.allies:
            if ally.position.tile_y > 16:
                score -= 10000
    elif enemy_on_our_side:
        score -= 5000
        score += current_elixir * 250
    else:
        if current_elixir == 10:
            score -= 2000
        elif current_elixir >= 8:
            score += 500

    # 4. COUNTER-PUSHING & OFFENSIVE STRATEGY
    defensive_troops_value = 0
    for ally in state.allies:
        if ally.position.tile_y <= 16:
            defensive_troops_value += getattr(ally.unit, 'cost', 0)

    if not desperate_defense and not enemy_on_our_side and defensive_troops_value > 5:
        score += defensive_troops_value * 200

    # 5. POSITIONAL INTELLIGENCE & KING TOWER ACTIVATION
    king_activation_tiles = {(7, 5), (10, 5)}
    for ally in state.allies:
        if (ally.position.tile_x, ally.position.tile_y) in king_activation_tiles and enemy_on_our_side:
            score += 500

    return score


def run_mcts(bot_instance, time_limit_ms=300):
    """Run the MCTS algorithm to find the best action."""
    try:
        start_time = time.time()
        root = MCTSNode(bot_instance.state)
        all_actions = bot_instance.get_actions()

        if not all_actions:
            return None

        root.get_untried_actions(all_actions)
        iterations = 0

        while (time.time() - start_time) * 1000 < time_limit_ms:
            node = root

            # 1. Selection
            while not node.untried_actions and node.children:
                node = node.select_child()

            # 2. Expansion
            if node.untried_actions:
                action = random.choice(node.untried_actions)
                try:
                    new_state = simulate_action(node.game_state, action)
                    node = node.expand(action, new_state)
                except Exception:
                    # If simulation fails, skip this action
                    node.untried_actions.remove(action)
                    continue

            # 3. Simulation (Rollout)
            # A simple rollout: evaluate the state after the first move.
            # A more complex simulation would continue for a few more random moves.
            try:
                rollout_state = deepcopy(node.game_state)
                result = heuristic_evaluation(rollout_state)
            except Exception:
                # If evaluation fails, use neutral result
                result = 0.0

            # 4. Backpropagation
            while node is not None:
                node.update(result)
                node = node.parent

            iterations += 1

        # After time is up, choose the best move based on the simulations
        if not root.children:
            return random.choice(all_actions) if all_actions else None

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child.action

    except Exception:
        # If MCTS completely fails, fall back to random action
        all_actions = bot_instance.get_actions()
        return random.choice(all_actions) if all_actions else None
