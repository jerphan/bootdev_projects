import pygame
from constants import SHOT_RADIUS
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen): #Draws a white circle onto the screen based on the position and radius of the shot
        pygame.draw.circle(screen, "white", self.position, self.radius)

    def update(self, dt): # Moves the shot based on its velocity and the framerate
        self.position+=(self.velocity * dt)