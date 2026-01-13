import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import *
from logger import log_event
import sys
from shot import Shot

def main():
    #Groups to be called upon later
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    #Defining the containers for each object class
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)
    #Generating an asteroid field that will constantly create asteroids and move them across the screen
    asteroid_field = AsteroidField()
    #Intializing imported pygame modules and screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #Printing to the console the pygame version used, and the screen intial resolution
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    #Initializing the clock for the game, variable that will later be used to define the frame rate, and player 
    game_clock=pygame.time.Clock()
    dt=0
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    #Infinite loop that wil continue unti the player is detected to collide with an asteroid
    while(1):
        log_state()
        #If the window is closed, the game will end
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        #For each member of the drawable group, we draw them
        for draws in drawable:
            draws.draw(screen)
        #We update all of the updateable group member's positions sat the same time
        updatable.update(dt)
        #This loops over each asteroid to see if they collide with anything
        for asteroid in asteroids:
            if(player.collides_with(asteroid)): #If an asteroid hits the player, the program will end itself and print Game Over! to the console
                log_event("player_hit")
                print("Game Over!")
                sys.exit()
            for shot in shots: #Checks to see if any shots collide with any asteroids, where the asteroid will either delete or split
                if (shot.collides_with(asteroid)):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
        #Updates the screen display in one frame 
        pygame.display.flip()
        #Updating the dt variable
        dt=game_clock.tick(60)/1000
    

if __name__ == "__main__":
    main()
