# Imports
import numpy as np

# Acceleration due to gravity in cm/s2
GRAVITY = 980


# Class for liquid particles
class Particle:
    
    def __init__(self, time_interval, wallposns, posn, mass=0.1, radius=3, RoI_weight=0.5, RoI_bias=2):
        self.mass = mass
        self.posn = posn                        # Position of particle
        self.velocity_u = np.array([0.0, 0.0])  # Initial Velocity of particle
        self.velocity_v = np.array([0.0, 0.0])  # Final Velocity of particle at a time step
        self.radius = radius                    # Radius of particle
        self.RoI_w = RoI_weight                 # Factor for calculating Radius of Influence graph's width (distance of influence)
        self.RoI_b = RoI_bias                   # Factor for calculating Radius of Influence graph's height (power of influence)
        self.forces = np.array([0.0, 0.0])      # Forces acting on particle at an instant
        
        # Defining wall boundary
        self.wall = wallposns
        
        # Intervals of time for calculation (converting from ms to s)
        self.t = time_interval / 1000
        
    '''
    # Calculating Radius of Influence
    def _calculateRoI(self, dist):
        
        # Equation for calculating Radius of Influence:
        # RoI Force = -(w * x^2) + b
        RoI = (-self.RoI_w) * (dist ** 2) + self.RoI_b
        
        return np.array([0, np.round((self.t * RoI), decimals=2)])
    '''
    
    # Calculating gravitational force on particle
    def _calculateGravity(self):
        
        # Calculating force due to force of gravity in y direction (m * g)
        grav = self.mass * GRAVITY
        
        return np.array([0, np.round(grav, decimals=2)])            # +ve to go down in pygame
    
    
    # Calculating force due to elastic collision with walls
    def _checkWallCollisions(self):
        if (self.posn[0] >= self.wall[0]):
            self.posn[0] = self.wall[0]
        
        elif (self.posn[1] >= self.wall[1]):
            self.posn[1] = self.wall[1]
        
        elif (self.posn[0] < 0):
            self.posn[0] = 0
        
        elif (self.posn[1] < 0):
            self.posn[1] = 0

        return
    
    
    # Calculating total forces acting on particle
    def _calculateForces(self):
        
        # Resetting forces calculation for this iteration
        self.forces = 0
        
        # Applying force of gravity
        self.forces = np.add(self.forces, self._calculateGravity())
        
        return
    
    
    # Calculating new velocity at each interval (after forces calculation)
    def _calculateVelocity(self):
        
        # Updating new initial velocity
        self.velocity_u = self.velocity_v
        
        # Updating new final velocity at t
        acc = np.divide(self.forces, self.mass)                 # Acceleration due to all forces at t
        self.velocity_v = np.add(self.velocity_u, acc * self.t)
        
        return
    
    
    # Calculating new positions at each interval (after velocity calculation)
    def _calculatePosn(self):
        
        # Acceleration due to all forces at t
        acc = np.divide(self.forces, self.mass)
        
        # Calculating new position using S = u*t + (1/2)*g*t^2
        self.posn = np.add(self.posn, np.round(np.add((self.velocity_u * self.t), (0.5 * acc * pow(self.t, 2))), decimals=0))
        
        # Ensuring particle doesn't clip through walls
        self._checkWallCollisions()
        
        return
        
    
    # Returning positon of particle
    def updateParticles(self):
        self._calculateForces()
        self._calculateVelocity()
        self._calculatePosn()
        
        return self.posn