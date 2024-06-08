import neat
import pygame
import random
from game import Game
import multiprocessing
import time

WIN_WIDTH=200
WIN_HEIGHT=200
FOOD_TIMER_MAX = 20 * 1.414
OPP_DIRR = {
    'UP': 'DOWN',
    'DOWN': 'UP',
    'LEFT': 'RIGHT',
    'RIGHT': 'LEFT'
}
CORE_COUNT = multiprocessing.cpu_count()-4
CHECKPOINT=False


def eval_genome(genome,config):
    # for genome_id, genome in genomes:
    fitness_list=[]
    for _ in range(10):
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        game = Game()
        fitness=0
        food_timer=0;
        distance_to_food=0
        last_direction='RIGHT'
        last_distance_to_food=0
        while not game.dead:
            inputs = game.get_inputs()
            output = net.activate(inputs)
            direction=game.get_direction(output)
            if(inputs[1]==10 and direction!=last_direction):
                fitness+=50
            game.move_snake(direction)

            last_direction=direction
            food_timer+=1
            if(game.dead):
                break
            if(food_timer > FOOD_TIMER_MAX*len(game.snake_body)):
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

def eval_genomes(genomes,config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        game = Game()
        fitness=0
        food_timer=0;
        distance_to_food=0
        last_direction='RIGHT'
        last_distance_to_food=0
        while not game.dead:
            inputs = game.get_inputs()
            output = net.activate(inputs)
            direction=game.get_direction(output)
            if(inputs[1]==10 and direction!=last_direction):
                fitness+=30
            game.move_snake(direction)
            # game.render(game_window)
            # fps.tick(game.speed)
            last_direction=direction
            food_timer+=1
            if(game.dead):
                break
            if(food_timer > FOOD_TIMER_MAX*len(game.snake_body)):
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
        genome.fitness=fitness
        # fitness_list.append(fitness)
    # return sum(fitness_list)/len(fitness_list)

def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_file)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(100,filename_prefix="checkpoint/neat-checkpoint-"))
    pe = neat.ParallelEvaluator(CORE_COUNT,eval_genome)
    winner = population.run(pe.evaluate, 1000)
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    config_path = "config"
    run(config_path)