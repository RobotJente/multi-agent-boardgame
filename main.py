# %%
from random import choice as randchoice

import pygame

from agents import Archer, Warrior
from game import Game
from rl_algorithms import PolicyIteration


def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 480))
    clock = pygame.time.Clock()
    game = Game()

    # Setup players with one archer and one warrior each

    # Player 1 pieces 
    a1 = Archer(1, (0, 0))
    w1 = Warrior(1, (1, 0))
    
    # Player 2 pieces
    a2 = Archer(2, (7, 7))
    w2 = Warrior(2, (6, 7))

    for agent in [a1, w1, a2, w2]:
        game.add_agent(agent)

    rl_alg = PolicyIteration()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        action = randchoice(a1.possible_actions(game) + w1.possible_actions(game))
        game.resolve_turn(action)

        action = randchoice(a2.possible_actions(game) + w2.possible_actions(game))
        game.resolve_turn(action)

        game.render(screen)
        pygame.display.flip()
        clock.tick(2)  # slow down for visualization

    pygame.quit()

if __name__ == '__main__':
    main()

# %%
