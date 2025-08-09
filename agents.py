# %%
from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Tuple
from uuid import UUID

import numpy as np
from numpy.typing import NDArray

# Logic needed for type hints that would result in circular imports
if TYPE_CHECKING:
    from game import Game

class Agent(ABC):
    legal_moves: List[NDArray]  # list of (x,y) values relative to position where piece can move
    legal_attacks: List[NDArray]    # list of (x,y) values relative to position where piece can attack
    player_id: int
    hp: int
    uid: UUID

    # Assigned in game, called by agent instance on death if not none
    death_callback = None

    def __init__(self, player_id, position, hp):
        self.player_id: int = player_id
        self.position: NDArray = np.array(position)  # (x, y) tuple
        self.hp = hp

        # Stable unique ID for debugging (persists for the object's lifetime)
        self.uid = f"{self.__class__.__name__}_{uuid.uuid4().hex[:8]}"

    def __repr__(self):
        return f"<{self.uid} at {self.position}>"


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

    def move(self, new_pos: NDArray):
        self.position = np.array(new_pos)
    
    def on_death(self):
        print(f"[DEBUG] {self.uid} died at {self.position}")
        if self.death_callback: self.death_callback(self)

    def take_damage(self, amount):
        if self.hp <= 0:
            print('already dead!')
            return  # Already dead
        self.hp -= amount
        print(f'{repr(self)} lost {amount} hp and now has {self.hp} hp')
        if self.hp <= 0:
            self.on_death()



class Archer(Agent):
    def __init__(self, player_id, position, hp=3):  
        super().__init__(player_id, position, hp=hp)

    legal_moves: List[NDArray] = [np.array(x) for x in [(1,0), (-1,0), (0,1), (0,-1)]]
    legal_attacks: List[NDArray] = [np.array(x) for x in [(2,0), (-2,0), (0,2), (0,-2)]]

class Warrior(Agent):
    def __init__(self, player_id, position, hp=7):  
        super().__init__(player_id, position, hp=hp)

    legal_moves: List[NDArray] = [np.array(x) for x in [(1,0), (-1,0), (0,1), (0,-1)]]
    legal_attacks: List[NDArray] = [np.array(x) for x in [(1,0), (-1,0), (0,1), (0,-1)]]