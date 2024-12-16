# Imports
import pygame
import numpy as np
from fluid_particles import Particle

# FPS in milliseconds
TIME_DELAY = 10

# Point features
POINT_RADIUS = 5

# RGB values
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

pygame.init()

# Simulation window
monitorSize = pygame.display.Info()
w, h = (monitorSize.current_w // 3) * 2, (monitorSize.current_h // 3) * 2
screen = pygame.display.set_mode([w, h])

# Particle objects
fluid_dots = []

runState = True                                 # Program running state (running or not)

while runState:
    
    # Checking for all input events
    for event in pygame.event.get():
        
        # User pressing close window button
        if event.type == pygame.QUIT:
            runState = False                    # Terminating program
        
        # Inputting new fluid dots
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # Getting coordinate of click
            x, y = pygame.mouse.get_pos()
            
            # Adding each splash of particle objects to array of particles
            for dx in range(-200, 200, 3*POINT_RADIUS):
                for dy in range(-30, 30, 3*POINT_RADIUS):
                    
                    # Creating a rectangular arrangement of particles to spawn initially
                    fluid_dots.append(Particle(TIME_DELAY, np.array([w - POINT_RADIUS, h - POINT_RADIUS]), np.array([x-dx, y-dy]), 1, POINT_RADIUS))

    screen.fill(BLACK)                          # Resetting background to black for each frame
    
    # Drawing all fluid particles
    if(fluid_dots != []):
        for dot in fluid_dots:
            
            # Drawing each particle object in frame for each interval of time
            pygame.draw.circle(screen, BLUE, dot.updateParticles(), POINT_RADIUS)
    
    pygame.display.flip()                       # Updating the simulation window with new drawings
    
    pygame.time.delay(TIME_DELAY)               # Setting frames per second according to TIME_DELAY