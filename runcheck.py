from game import *
import neat
import os
from ai import *
import pygame

WINDOW = (200, 200)
SIZE = (500, 500)
STEP = 20

DIR = './checkpoint'
CONFIG = 'config'

def run2(checkPoint, config_file):
  # Load configuration.
  config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

  # Load configuration.
  p = neat.Checkpointer.restore_checkpoint(checkPoint)

  # Add a stdout reporter to show progress in the terminal.
  p.add_reporter(neat.StdOutReporter(True))

  # Run generations.
  winner = p.run(eval_genomes, 1)
  return neat.nn.FeedForwardNetwork.create(winner, config)

def runCheckpoints(dirname, config_file):
  files = [f for f in os.listdir(dirname)]
  return [(f, run2(f'{dirname}/{f}', config_file)) for f in files ]

def main():
    nets = runCheckpoints(DIR, CONFIG)
    fps = pygame.time.Clock()
    for f, net in nets:
        game = Game()
        screen = pygame.display.set_mode(WINDOW)
        game.render(screen)
        food_timer=0
        while not game.dead:
            pygame.event.pump()
            inputs = game.get_inputs()
            output = net.activate(inputs)
            food_timer+=1
            if(food_timer > FOOD_TIMER_MAX*len(game.snake_body)):
                # genome.fitness=fitness
                break
            if(game.eaten):
                food_timer=0
            direction=game.get_direction(output)
            # print(direction)
            game.move_snake(direction)
            game.render(screen)
            pygame.display.update()
            fps.tick(game.speed)
        
        # print("LOAD ", f)
        # game.render(screen)






if __name__ == "__main__":
  # Initialize pygame
  pygame.init()
  main()
  pygame.quit()