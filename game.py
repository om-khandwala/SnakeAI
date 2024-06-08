import pygame
import sys
import random
import os
import numpy as np
import math
WIN_WIDTH=200
WIN_HEIGHT=200

class Game:
    def __init__(self):
        self.snake_body = [(50,50),(40,50),(30,50),(20,50)]
        self.snake_position = [50,50]
        self.direction='RIGHT'
        self.speed = 10
        self.eaten=False
        self.score=0
        self.dead=False
        self.poss = set()
        for a in range(0,(WIN_WIDTH//10)):
            for b in range(0,(WIN_HEIGHT//10)):
                if((a*10,b*10) not in self.snake_body):
                    self.poss.add((a*10,b*10))
        self.food_pos = random.choice(tuple(self.poss))


    def move_snake(self,changedir=None):
        self.eaten=False
        if(changedir!=None):
            if(changedir=='UP' and self.direction!='DOWN'):
                self.direction='UP'
            if(changedir=='DOWN' and self.direction!='UP'):
                self.direction='DOWN'
            if(changedir=='LEFT' and self.direction!='RIGHT'):
                self.direction='LEFT'
            if(changedir=='RIGHT' and self.direction!='LEFT'):
                self.direction='RIGHT'

        if(self.direction=='UP'):
            self.snake_position[1]-=10
        if(self.direction=='DOWN'):
            self.snake_position[1]+=10
        if(self.direction=='LEFT'):
            self.snake_position[0]-=10
        if(self.direction=='RIGHT'):
            self.snake_position[0]+=10
        
        self.snake_body.insert(0, tuple(self.snake_position))
        if(self.snake_position[0]==self.food_pos[0] and self.snake_position[1]==self.food_pos[1]):
            self.eaten=True
            self.score+=1
        else:
            self.poss.add(self.snake_body.pop())
        
        if(self.snake_position[0]<0 or self.snake_position[0]>WIN_WIDTH-10):
            self.dead=True
            return self.score,self.snake_body,self.food_pos,self.dead,self.eaten
        if(self.snake_position[1]<0 or self.snake_position[1]>WIN_HEIGHT-10):
            self.dead=True
            return self.score,self.snake_body,self.food_pos,self.dead,self.eaten

        
        for block in self.snake_body[1:]:
            if(self.snake_position[0]==block[0] and self.snake_position[1]==block[1]):
                self.dead=True
                return self.score,self.snake_body,self.food_pos,self.dead,self.eaten
        
        self.poss.remove(tuple(self.snake_position))
        if(self.eaten):
            self.food_pos = random.choice(tuple(self.poss))
        return self.score,self.snake_body,self.food_pos,self.dead,self.eaten
    

    def get_direction(self,output):
        
        out = [0,1,2][output.index(max(output))]
        if(out==1):
            return self.direction
        elif(out==0):
            if(self.direction=='RIGHT'):
                return 'UP'
            elif(self.direction=='UP'):
                return 'LEFT'
            elif(self.direction=='LEFT'):
                return 'DOWN'
            else:
                return 'RIGHT'
        else:
            if(self.direction=='RIGHT'):
                return 'DOWN'
            elif(self.direction=='UP'):
                return 'RIGHT'
            elif(self.direction=='LEFT'):
                return 'UP'
            else:
                return 'LEFT'
        return self.direction
    
    def get_inputs(self):
        # def bresenham(x1, y1, x2, y2):
        #     points = []
        #     dx = abs(x2 - x1)
        #     dy = abs(y2 - y1)
        #     x, y = x1, y1
        #     sx = 1 if x2 > x1 else -1
        #     sy = 1 if y2 > y1 else -1
        #     if dx > dy:
        #         err = dx / 2.0
        #         while abs(x - x2) > 0.5:
        #             points.append((x, y))
        #             err -= dy
        #             if err < 0:
        #                 y += sy
        #                 err += dx
        #             x += sx
        #     else:
        #         err = dy / 2.0
        #         while abs(y - y2) > 0.5:
        #             points.append((x, y))
        #             err -= dx
        #             if err < 0:
        #                 x += sx
        #                 err += dy
        #             y += sy
        #     points.append((x, y))
        #     return np.array(points)
        # def get_body_distance_in_n_directions(n=8, angles=None):
        #     grid_size = WIN_HEIGHT
        #     snake_head_pos = self.snake_position[0], self.snake_position[1]
        #     snake_head_to_body_distances = np.zeros(n)
        #     angle_index = 0
        #     angle = 0
        #     for i in range(n):
        #         if angles is not None:
        #             angle = angles[i]
        #         # make a ray from the snake_data head in the direction of the angle to the end of the grid
        #         vector = math.cos(angle) * grid_size * 2, math.sin(angle) * grid_size * 2
        #         ray = bresenham(snake_head_pos[0], snake_head_pos[1], snake_head_pos[0] + vector[0],
        #                         snake_head_pos[1] + vector[1])
        #         # check if the ray intersects with a body part
        #         has_intersection(angle_index, ray, snake_head_to_body_distances)
        #         angle_index += 1
        #         angle += 2 * math.pi / n
        #     # if 0 in snake_head_to_body_distances:
        #         # print(snake_head_to_body_distances)
        #     return snake_head_to_body_distances
        # def has_intersection(angle_index, ray, snake_head_to_body_distances):
        #     for x, y in ray:
        #         x, y = int(x), int(y)
        #         # check if point is in the grid
        #         if not (0 <= x < WIN_WIDTH and 0 <= y < WIN_HEIGHT):
        #             break

        #         if (x,y) in self.snake_body[1:]:
        #             snake_head_to_body_distances[angle_index] = np.sqrt(
        #                 (x - self.snake_position[0]) ** 2 + (y - self.snake_position[1]) ** 2)
        #             break
        
        wall_distances = [self.snake_position[0],WIN_WIDTH-self.snake_position[1],self.snake_position[1],WIN_HEIGHT-self.snake_position[1]]
        # snake_head_pos = pygame.Vector2(self.snake_position[0], self.snake_position[1])
        # food_pos = pygame.Vector2(self.food_pos[1], self.food_pos[0])
        # snake_head_to_food=snake_head_pos-food_pos
        snake_distance = [-1,-1,-1,0,0]
        if(self.direction=='LEFT'):
            snake_distance[0]=WIN_HEIGHT-self.snake_position[1]
            snake_distance[1]=self.snake_position[0]
            snake_distance[2]=self.snake_position[1]
            for c in self.snake_body[1:]:
                if(c[1]==self.snake_position[1] and c[0]<self.snake_position[0]):
                    snake_distance[1]=min(snake_distance[1],self.snake_position[0]-c[0])
                if(c[0]==self.snake_position[0] and c[1]>self.snake_position[1]):
                    snake_distance[0]=min(snake_distance[0],c[1]-self.snake_position[1])
                if(c[0]==self.snake_position[0] and c[1]<self.snake_position[1]):
                    snake_distance[2]=min(snake_distance[2],self.snake_position[1]-c[1])
            snake_distance[3]=self.snake_position[0]-self.food_pos[0]
            snake_distance[4]=self.snake_position[1]-self.food_pos[1]
        elif(self.direction=='UP'):
            snake_distance[0]=self.snake_position[0]
            snake_distance[1]=self.snake_position[1]
            snake_distance[2]=WIN_WIDTH-self.snake_position[0]
            for c in self.snake_body[1:]:
                if(c[0]==self.snake_position[0] and c[1]<self.snake_position[1]):
                    snake_distance[1]=min(snake_distance[1],self.snake_position[1]-c[1])
                if(c[1]==self.snake_position[1] and c[0]>self.snake_position[0]):
                    snake_distance[0]=min(snake_distance[0],c[0]-self.snake_position[0])
                if(c[1]==self.snake_position[1] and c[0]<self.snake_position[0]):
                    snake_distance[2]=min(snake_distance[2],self.snake_position[0]-c[0])
            snake_distance[3]=self.snake_position[1]-self.food_pos[1]
            snake_distance[4]=self.food_pos[0]-self.snake_position[0]
        elif(self.direction=='RIGHT'):
            snake_distance[0]=self.snake_position[1]
            snake_distance[1]=WIN_WIDTH-self.snake_position[0]
            snake_distance[2]=WIN_HEIGHT-self.snake_position[1]
            for c in self.snake_body[1:]:
                if(c[1]==self.snake_position[1] and c[0]>self.snake_position[0]):
                    snake_distance[1]=min(snake_distance[1],c[0]-self.snake_position[0])
                if(c[0]==self.snake_position[0] and c[1]<self.snake_position[1]):
                    snake_distance[0]=min(snake_distance[0],self.snake_position[1]-c[1])
                if(c[0]==self.snake_position[0] and c[1]>self.snake_position[1]):
                    snake_distance[2]=min(snake_distance[2],c[1]-self.snake_position[1])
            snake_distance[3]=self.food_pos[0]-self.snake_position[0]
            snake_distance[4]=self.food_pos[1]-self.snake_position[1]
        else:
            snake_distance[0]=WIN_WIDTH-self.snake_position[0]
            snake_distance[1]=WIN_HEIGHT-self.snake_position[1]
            snake_distance[2]=self.snake_position[0]
            for c in self.snake_body[1:]:
                if(c[0]==self.snake_position[0] and c[1]>self.snake_position[1]):
                    snake_distance[1]=min(snake_distance[1],c[1]-self.snake_position[1])
                if(c[1]==self.snake_position[1] and c[0]>self.snake_position[0]):
                    snake_distance[0]=min(snake_distance[0],c[0]-self.snake_position[0])
                if(c[1]==self.snake_position[1] and c[0]<self.snake_position[0]):
                    snake_distance[2]=min(snake_distance[2],self.snake_position[0]-c[0])
            snake_distance[3]=self.food_pos[1]-self.snake_position[1]
            snake_distance[4]=self.snake_position[0]-self.food_pos[0]
        
        
        inputs = snake_distance
        # print(inputs)
        return inputs
    
    def render(self,game_window):
        game_window.fill(pygame.Color(0, 0, 0))
        for pos in self.snake_body:
            pygame.draw.rect(game_window, pygame.Color(0, 255, 0), pygame.Rect(pos[0], pos[1], 10, 10))
        
        pygame.draw.rect(game_window, pygame.Color(255, 0, 0), pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))



if(__name__=='__main__'):
    pygame.init()
    pygame.display.set_caption('Snake Game')
    fps=pygame.time.Clock()
    game = Game()
    game_window=pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    while True:
        changedir=None
        for  event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    changedir='UP'
                if event.key == pygame.K_DOWN:
                    changedir='DOWN'
                if event.key == pygame.K_LEFT:
                    changedir='LEFT'
                if event.key == pygame.K_RIGHT:
                    changedir='RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
            if(changedir=='UP' and game.direction=='DOWN'):
                changedir=None
            if(changedir=='DOWN' and game.direction=='UP'):
                changedir=None
            if(changedir=='LEFT' and game.direction=='RIGHT'):
                changedir=None
            if(changedir=='RIGHT' and game.direction=='LEFT'):
                changedir=None
        score,snake_body,food_pos,dead,eaten = game.move_snake(changedir)
        # game.get_inputs()
        if eaten:
            print(score)
        if not dead:
            game.render(game_window)
        else:
            pygame.quit()
            sys.exit()
        
        pygame.display.update()

        fps.tick(game.speed)