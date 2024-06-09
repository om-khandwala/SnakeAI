import neat
import pygame
from game import Game
import multiprocessing
import visualize
import pickle

CORE_COUNT = multiprocessing.cpu_count()-4


def eval_genome(genome,config):
    # for genome_id, genome in genomes:
    fitness_list=[]
    for _ in range(10):
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        game = Game()
        fitness=0
        food_timer=0
        distance_to_food=0
        last_direction='RIGHT'
        last_distance_to_food=0
        while not game.dead:
            inputs = game.get_inputs()
            output = net.activate(inputs)
            direction=game.get_direction(output)
            out = [0,1,2][output.index(max(output))]
            # if((inputs[3]==10 and out!=0) or (inputs[4]==10 and out!=1) or (inputs[5]==10 and out!=2)):
            #     fitness+=40
            game.move_snake(direction)

            last_direction=direction
            food_timer+=1
            if(game.dead):
                break
            if(food_timer > game.food_timer*len(game.snake_body)):
                fitness-=100
                break
            else:
                snake_head_pos = pygame.Vector2(game.snake_position[0],game.snake_position[1])
                food_pos = pygame.Vector2(game.food_pos[0],game.food_pos[1])
                snake_head_pos = food_pos - snake_head_pos
                distance_to_food = snake_head_pos.length()
                if(distance_to_food < last_distance_to_food):
                    fitness+=1
                else:
                    fitness-=1
                last_distance_to_food = distance_to_food
                fitness+=0.1
                if(game.eaten):
                    fitness+=100
                    food_timer=0
        fitness_list.append(fitness)
    return sum(fitness_list)/len(fitness_list)


def run(config_file,checkpoint=None,generations=1000,plot=False,savewinner=False):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_file)
    
    #creating population
    population = neat.Population(config)
    if(checkpoint):
        population = neat.Checkpointer.restore_checkpoint(f'./checkpoint/{checkpoint}')
    
    # neat reporters
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(100,filename_prefix="checkpoint/"))

    # parallel evolution
    pe = neat.ParallelEvaluator(CORE_COUNT,eval_genome)
    winner = population.run(pe.evaluate, generations)
    
    #plot functions
    if(plot):
        node_name = {0:"left",1:"front",2:"right",-1:"left wall dist",-2:"front wall dist",-3:"right wall dist",-4:"left snake dist",-5:"front snake dist",-6:"right snake dist",-7:"food y",-8:"food x"}
        visualize.plot_stats(stats, ylog=False, view=True,filename="winner_stats.svg")
        visualize.plot_species(stats, view=True,filename="winner_species.svg")
        visualize.draw_net(config,winner,True,node_names=node_name,filename="winner_net.svg")
    
    #saving the winner
    if(savewinner):
        with open ("winner.pkl", "wb") as f:
            pickle.dump(winner, f)
    
    return winner

if __name__ == '__main__':
    config_path = "config"
    run(config_path,savewinner=True)