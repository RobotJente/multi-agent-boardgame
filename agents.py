from abc import ABC, abstractmethod

class Agent(ABC):
    def __init__(self, player_id, position):
        self.player_id = player_id
        self.position = position  # (x, y) tuple

    @abstractmethod
    def possible_actions(self, game_state):
        """Return list of possible actions for this agent."""
        pass

    @abstractmethod
    def move(self, action):
        """Update position or state based on action."""
        pass

class Archer(Agent):
    def possible_actions(self, game_state):
        # Example: can move one cell in any direction or shoot (dummy action)
        actions = []
        x, y = self.position
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if game_state.is_within_bounds(nx, ny) and not game_state.is_occupied(nx, ny):
                actions.append(('move', (nx, ny)))
        actions.append(('shoot', None))
        return actions

    def move(self, action):
        if action[0] == 'move':
            self.position = action[1]
        # shooting handled elsewhere

class Warrior(Agent):
    def possible_actions(self, game_state):
        # Moves two cells orthogonally or attacks adjacent cell
        actions = []
        x, y = self.position
        directions = [(2,0), (-2,0), (0,2), (0,-2)]
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if game_state.is_within_bounds(nx, ny) and not game_state.is_occupied(nx, ny):
                actions.append(('move', (nx, ny)))
        # Attack adjacent squares
        adjacent = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in adjacent:
            nx, ny = x+dx, y+dy
            if game_state.is_within_bounds(nx, ny):
                actions.append(('attack', (nx, ny)))
        return actions

    def move(self, action):
        if action[0] == 'move':
            self.position = action[1]
        # attacks handled elsewhere
