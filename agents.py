from abc import ABC, abstractmethod
import uuid

class Agent(ABC):
    def __init__(self, player_id, position, hp):
        self.player_id = player_id
        self.position = position  # (x, y) tuple
        self.hp = hp
        # Stable unique ID for debugging (persists for the object's lifetime)
        self.uid = f"{self.__class__.__name__}_{uuid.uuid4().hex[:8]}"

    @abstractmethod
    def possible_actions(self, game_state):
        """Return list of possible actions for this agent."""
        pass

    @abstractmethod
    def move(self, action):
        """Update position or state based on action."""
        pass

    def __repr__(self):
        return f"<{self.uid} at {self.position}>"
    
    def on_death(self):
        print(f"[DEBUG] {self.uid} died at {self.position}")
        if self.death_callback:
            self.death_callback(self)

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

    def __init__(self, player_id, position, hp=7):  
        super().__init__(player_id, position, hp=hp)

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
