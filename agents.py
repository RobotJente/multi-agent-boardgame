# %%
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Tuple

import numpy as np
from numpy.typing import NDArray

# Logic needed for type hints that would result in circular imports
if TYPE_CHECKING:
    from game import Game


class Agent(ABC):
    legal_moves: List[NDArray]  # list of (x,y) values relative to position where piece can move
    legal_attacks: List[NDArray]    # list of (x,y) values relative to position where piece can attack
    player_id: int

    def __init__(self, player_id: int, position: Tuple):
        self.player_id: int = player_id
        self.position: NDArray = np.array(position)  # (x, y) tuple

    # For now, this doesn't need to be abstract because it's the same for all classes? 
    def possible_actions(self, game_state: Game) -> List[Tuple]:
        """Return list of possible actions for this agent."""
        actions = []

        # First we iterate through the moves
        for dxy in self.legal_moves:
            target_square = self.position + dxy

            if game_state.is_within_bounds(*target_square) and not game_state.is_occupied(*target_square):
                actions.append(('move', target_square, self))

        # Then we iterate through the attacks
        for dxy in self.legal_attacks:
            target_square = self.position + dxy

            # TODO check if there's an enemy in the square
            if game_state.is_within_bounds(*target_square) and game_state.is_occupied(*target_square) and (game_state.get_occupied(*target_square).player_id != self.player_id):
                actions.append(('attack', target_square, self))

        return actions

    # TODO FIX: NOT CALLED FOR NOW, HANDLED IN GAME 
    def act(self, game_state: Game, action: Tuple):
        if action[0] == 'move': self.position = action[1]
        elif action[0] == 'attack': game_state.get_occupied(*action[1]).take_damage(1)

    def move(self, new_pos: NDArray):
        # Update the position?
        print(new_pos)
        self.position = np.array(new_pos)

class Archer(Agent):
    legal_moves: List[NDArray] = [np.array(x) for x in [(1,0), (-1,0), (0,1), (0,-1)]]
    legal_attacks: List[NDArray] = [np.array(x) for x in [(2,0), (-2,0), (0,2), (0,-2)]]

class Warrior(Agent):
    legal_moves: List[NDArray] = [np.array(x) for x in [(1,0), (-1,0), (0,1), (0,-1)]]
    legal_attacks: List[NDArray] = [np.array(x) for x in [(1,0), (-1,0), (0,1), (0,-1)]]