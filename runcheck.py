from game import *
import neat
import os
from ai import *
import pygame
import visualize

DIR = './checkpoint'
CONFIG = 'config'

def runCheckpoints(dirname, config_file,checkpoint=None):
    files = [f for f in os.listdir(dirname)]
    if(checkpoint):
        files = checkpoint
    return [(f, run(config_file,f,1,False,True)) for f in files ]

def neuralnet(winner,config):
    return neat.nn.FeedForwardNetwork.create(winner, config)

def runwinner(config,filename='winner.pkl'):
    with open(filename,"rb") as f:
        winner = pickle.load(f)
        return [("best",(neuralnet(winner,config),winner))]


def main(config_file,gui=True,graphs=False,winner=False):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_file)
    nets = []
    if(winner):
        nets = runwinner(config)
    else:
        winners = runCheckpoints(DIR,config_file)
        nets = [(f,(neuralnet(winner,config),winner)) for f,winner in winners]

    fps = pygame.time.Clock()
    for f, net in nets:
        if(gui):
            game = Game()
            # dot = draw_net(net[1],net[2],view=True,node_names=node_name,filename=f'{f}.gv')
            screen = pygame.display.set_mode((game.win_width,game.win_height))
            pygame.display.set_caption(f)
            game.render(screen)
            food_timer=0
            while not game.dead:
                pygame.event.pump()
                inputs = game.get_inputs()
                output = net[0].activate(inputs)
                food_timer+=1
                if(food_timer > game.food_timer*len(game.snake_body)):
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

        if(graphs):
            node_name = {0:"left",1:"front",2:"right",-1:"left wall dist",-2:"front wall dist",-3:"right wall dist",-4:"left snake dist",-5:"front snake dist",-6:"right snake dist",-7:"food y",-8:"food x"}
            dot = visualize.draw_net(config,net[1],True,filename=f)





if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    main(CONFIG,winner=False)
    pygame.quit()