import pygame
from pygame.locals import *
from creature import Creature
from random import sample, choice, randrange


def visualizer():
    # Set up sim
    pygame.init()

    window_height: int = 600
    window_width: int = 600
    frames_per_sec: int = 30

    grid_size: int = 120
    square_size: int = 5

    n_creatures: int = 300

    frame_rate: pygame.time.Clock = pygame.time.Clock()
    screen = pygame.display.set_mode((window_width,window_height),pygame.SCALED)
    pygame.display.set_caption('Natural Selection Simulation')



    # Set up sim elements
    all_creatures: pygame.sprite.Group = pygame.sprite.Group()

    current_positions:list[tuple[int,int]] = []
    if n_creatures > 0:
        for i in range(n_creatures):
            new_position = (randrange(grid_size),randrange(grid_size))
            while new_position in current_positions:
                new_position = (randrange(grid_size),randrange(grid_size))
            current_positions.append(new_position)

            all_creatures.add(Creature(new_position[0],new_position[1]))

    # Initialize game loop
    game_loop = True
    while game_loop:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        # Execute movement
        current_positions:list[tuple[int,int]] = []
        for element in all_creatures:
            current_positions.append((element.x_loc,element.y_loc))

        for element in all_creatures:
            choice(element.move_options)(grid_size,current_positions)

        # Draw elements to the screen
        screen.fill('white')

        for element in all_creatures:
            element.draw(screen,square_size)

        pygame.display.flip()
        frame_rate.tick(frames_per_sec)


if __name__=="__main__":
    visualizer()