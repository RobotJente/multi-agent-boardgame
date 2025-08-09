# %%
import pygame
from game import Game
from agents import Archer, Warrior
from rl_algorithms import PolicyIteration

def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 480))
    clock = pygame.time.Clock()
    game = Game()

    # Setup players with one archer and one warrior each
    a1 = Archer(1, (0, 0))
    w1 = Warrior(1, (1, 0))
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

        # Dummy player actions for now (just first possible action)
        player_actions = {
            1: {a1: a1.possible_actions(game)[0], w1: w1.possible_actions(game)[0]},
            2: {a2: a2.possible_actions(game)[0], w2: w2.possible_actions(game)[0]},
        }
        game.players[1][0].take_damage(1)
        game.resolve_turn(player_actions)
        game.render(screen)
        pygame.display.flip()
        clock.tick(2)  # slow down for visualization

    pygame.quit()

if __name__ == '__main__':
    main()

# %%
