import os
import pygame
from pygame.locals import *
from creature import Creature
from random import sample, choices, randrange
from math import trunc
import neat
import visualize


def visualizer(config_file,checkpoint_paths):
    # Set up sim
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Natural Selection Simulation')

    window_height: int = 600
    window_width: int = 600
    
    global font, screen, generation
    font = pygame.font.SysFont('impact',20)
    generation = 0
    screen = pygame.display.set_mode((window_width,window_height),pygame.SCALED)

    run(config_file,checkpoint_paths)

def evaluate_genomes(genomes, config):
    # Part of the config file
    n_creatures: int = 300

    global font, screen, generation
    generation += 1

    grid_size: int = 60
    square_size: int = 10
    frames_per_sec: int = 30

    frame_rate: pygame.time.Clock = pygame.time.Clock()
    # Set up sim elements
    all_creatures: pygame.sprite.Group = pygame.sprite.Group()

    current_positions:list[tuple[int,int]] = []


    for genome_id, genome in genomes:
        genome.fitness = 0 # start fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        new_position = (randrange(grid_size),randrange(grid_size))
        while new_position in current_positions:
            new_position = (randrange(grid_size),randrange(grid_size))
        current_positions.append(new_position)

        all_creatures.add(Creature(new_position[0],new_position[1],radius=trunc(square_size/2), net=net,genome=genome))

    # Initialize game loop
    game_loop = True
    max_game_steps = 100
    game_steps = 0
    while game_loop and game_steps <= max_game_steps:
        game_steps += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        # Execute movement
        current_positions:list[tuple[int,int]] = []
        for element in all_creatures:
            current_positions.append((element.x_loc,element.y_loc))

        # TODO: update fitness
        for element in all_creatures:
            # In the video, he uses each output as a probability input for the choice
            output = element.net.activate((element.x_loc, element.y_loc))
            if sum(output) > 0:
                choices(element.move_options,weights=output)[0](grid_size,current_positions)

            element.genome.fitness = fitness_check(element.x_loc,element.y_loc, grid_size)

        # Draw elements to the screen
        screen.fill('white')

        for element in all_creatures:
            element.draw(screen,square_size)
        
        generation_label = font.render(f'Gen: {generation}',1,'black')
        screen.blit(generation_label, (10,10))

        pygame.display.flip()
        frame_rate.tick(frames_per_sec)


def fitness_check(x_loc:int, y_loc:int, grid_size:int) -> int:
    if x_loc > grid_size/2:
        return 1
    return 0

def run(config_file,checkpoint_paths) -> None:
    delte_checkpoints(checkpoint_paths)

    config = neat.Config(neat.DefaultGenome,
                         neat.DefaultReproduction,
                         neat.DefaultSpeciesSet,
                         neat.DefaultStagnation,
                         config_file)
    
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1,filename_prefix='neat_checkpoints/neat-checkpoint-'))

    winner = p.run(evaluate_genomes, 50)

    node_names = {-1:'X Position',-2:'Y Position',0:'Move Up',1:'Move Down',2:'Move Left',3:'Move Right',4:'Move Random'}
    visualize.draw_net(config, winner, True, node_names=node_names, filename='plots/net')
    visualize.plot_stats(stats,ylog=False,view=True, filename='plots/avg_fitness')
    visualize.plot_species(stats,view=True, filename='plots/speciation')

def delte_checkpoints(checkpoint_paths):
    for file in checkpoint_paths:
        os.remove(file)

if __name__=="__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    checkpoint_paths = os.path.join(local_dir,'neat_checkpoints')
    visualizer(config_path, checkpoint_paths)
