import pygame
from agents import Archer, Warrior

class Game:
    WIDTH = 8
    HEIGHT = 8

    def __init__(self):
        self.grid = [[None for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.players = {1: [], 2: []}  # agents per player
        self.turn = 0

    def is_within_bounds(self, x, y):
        return 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT

    def is_occupied(self, x, y):
        return self.grid[y][x] is not None

    def add_agent(self, agent):
        x, y = agent.position
        if not self.is_occupied(x, y):
            self.grid[y][x] = agent
            self.players[agent.player_id].append(agent)
        else:
            raise ValueError("Position already occupied")

    def move_agent(self, agent, action):
        old_x, old_y = agent.position
        if action[0] == 'move':
            new_x, new_y = action[1]
            if self.is_within_bounds(new_x, new_y) and not self.is_occupied(new_x, new_y):
                self.grid[old_y][old_x] = None
                agent.move(action)
                self.grid[new_y][new_x] = agent
        elif action[0] in ('attack', 'shoot'):
            # Add simple attack logic here if needed
            pass

    def resolve_turn(self, player_actions):
        # player_actions = {player_id: {agent: action, ...}, ...}
        # For now, just move all agents simultaneously
        # More advanced conflict resolution can be added later
        for player_id, actions in player_actions.items():
            for agent, action in actions.items():
                self.move_agent(agent, action)

        self.turn += 1

    def get_game_state(self):
        # Return any info RL agent might need
        return self

    def render(self, screen):
        screen.fill((30,30,30))
        cell_size = 60
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
                color = (200, 200, 200) if (x+y)%2 == 0 else (100, 100, 100)
                pygame.draw.rect(screen, color, rect)
                agent = self.grid[y][x]
                if agent:
                    if isinstance(agent, Archer):
                        pygame.draw.circle(screen, (0, 255, 0), rect.center, cell_size//3)
                    else:  # Warrior
                        pygame.draw.rect(screen, (255, 0, 0), rect.inflate(-cell_size//3, -cell_size//3))
