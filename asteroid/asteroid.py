import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import random
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen): #Draws a white circle onto the screen based on the position and radius of the asteroid
        pygame.draw.circle(screen, "white", self.position, self.radius)

    def update(self, dt): #Moves the asteroid based on its velocity and the framerate
        self.position+=(self.velocity * dt) 

    def split(self): #Based on the size, when an asteroid is hit it will behave differently
        self.kill() #The current asteroid will always be destroid
        if(self.radius <= ASTEROID_MIN_RADIUS): #If the asteroid is less than the min radius, it is considered small and will just delete
            return
        log_event("asteroid_split")
        #If the asteroid is larger than the min radius then it will split into two new asteroids
        angle = random.uniform(20, 50)
        first_vector = self.velocity.rotate(angle) #Vector for the first asteroid to spawn
        second_vector = (self.velocity.rotate(-1*angle)) #Vector for second asteroid to spawn, negated so that it goes in the oposite direction
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        #Intializing the 2 asteroids that will spawn from the position of the old one, with a previously calculated radius
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius) 
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        #We then give the asteroids the previously calculated velocities
        asteroid1.velocity = first_vector
        asteroid2.velocity = second_vector