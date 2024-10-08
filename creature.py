from typing import Union
import pygame
from pygame.locals import *
import neat

class Creature(pygame.sprite.Sprite):
    def __init__(self, x_loc: float, y_loc: float,
                 radius: float = 2, color: Union[str,tuple[int,int,int]]='black') -> None:
        super().__init__()
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.radius = radius
        self.image = pygame.Surface((self.radius*2, self.radius*2), flags=pygame.SRCALPHA)
        self.color = color
        pygame.draw.circle(self.image, self.color, (radius,radius), radius)
        self.move_options = [self.move_up, self.move_down, self.move_left, self.move_right]

    def draw(self, surface,square_size:int):
        surface.blit(self.image,(self.x_loc*square_size,self.y_loc*square_size))

    def move_up(self, grid_size:int, current_positions:list[tuple[int,int]]):
        if self.y_loc == 0:
            return None
        if (self.x_loc, self.y_loc - 1) in current_positions:
            return None
        self.y_loc -= 1

    def move_down(self, grid_size:int, current_positions:list[tuple[int,int]]):
        if self.y_loc == grid_size-1:
            return None
        if (self.x_loc +1, self.y_loc) in current_positions:
            return None
        self.y_loc += 1
    
    def move_left(self, grid_size:int, current_positions:list[tuple[int,int]]):
        if self.x_loc == 0:
            return None
        if (self.x_loc - 1, self.y_loc) in current_positions:
            return None
        self.x_loc -= 1

    def move_right(self, grid_size:int, current_positions:list[tuple[int,int]]):
        if self.x_loc == grid_size-1:
            return None
        if (self.x_loc + 1, self.y_loc) in current_positions:
            return None
        self.x_loc += 1


def eval_genomes(genomes, config):
    pass


def run(config_file) -> None:
    config = neat.Config(neat.DefaultGenome,
                         neat.DefaultReproduction,
                         neat.DefaultSpeciesSet,
                         neat.DefaultSpeciesSet)
    
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)