# Example file showing a circle moving on screen
import pygame
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
LENGTH = 100
dt = 0
BALL_SPEED = 5
PI = math.acos(-1.0)
radius = 10

player1_pos = pygame.Vector2(100, screen.get_height() / 2)
player2_pos = pygame.Vector2(screen.get_width() - 100, screen.get_height() / 2)
player1_velocity = pygame.Vector2(0 , 0)
player2_velocity = pygame.Vector2(0 , 0)
ball_pos = pygame.Vector2(player1_pos[0] + 10 , player1_pos[1])
ball_velocity = pygame.Vector2(0 , 0)
ball_launched = False

def detect_colision(pos1 , pos2 , posball):

    a = pos1.distance_to(posball)
    b = pos2.distance_to(posball)
    
    if(posball.y < pos1.y or posball.y > pos2.y):
        return min(a , b) < radius / 2
    
    c = pos1.distance_to(pos2)

    beta = math.acos( (a*a + c*c - b*b) / (2*a*c) )
    alpha = PI - beta

    h = a * math.sin(alpha)

    return min(a , min(b , h)) < radius/2

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.line(screen, "white", pygame.Vector2(player1_pos[0] , player1_pos[1] - LENGTH/2) ,  pygame.Vector2(player1_pos[0] , player1_pos[1] + LENGTH/2) , 10)
    pygame.draw.line(screen, "white", pygame.Vector2(player2_pos[0] , player2_pos[1] - LENGTH/2) ,  pygame.Vector2(player2_pos[0] , player2_pos[1] + LENGTH/2) , 10)
    pygame.draw.circle(screen , "white" , ball_pos , radius)

    keys = pygame.key.get_pressed()
    if(keys[pygame.K_SPACE] and ball_launched == False):
        ball_launched = True
        ball_velocity = pygame.Vector2(500 * dt , 0) + player1_velocity

    if keys[pygame.K_w] and player1_pos.y - 41 > 0:
        player1_velocity.y = -500 * dt

    if keys[pygame.K_s] and player1_pos.y + 41 < screen.get_height():
        player1_velocity.y = 500 * dt
    
    if keys[pygame.K_w] == False and keys[pygame.K_s] == False :
        player1_velocity.y = 0
    
    if keys[pygame.K_UP] and player2_pos.y - 41 > 0:
        player2_velocity.y = -500 * dt

    if keys[pygame.K_DOWN] and player2_pos.y + 41 < screen.get_height():
        player2_velocity.y = 500 * dt
    
    if keys[pygame.K_DOWN] == False and keys[pygame.K_UP] == False :
        player2_velocity.y = 0

    if(detect_colision(pygame.Vector2(player1_pos[0] , player1_pos[1] - LENGTH/2) ,  pygame.Vector2(player1_pos[0] , player1_pos[1] + LENGTH/2) , ball_pos)):
        ball_velocity.x *= -1
        ball_velocity += player1_velocity
    if(detect_colision(pygame.Vector2(player2_pos[0] , player2_pos[1] - LENGTH/2) ,  pygame.Vector2(player2_pos[0] , player2_pos[1] + LENGTH/2) , ball_pos)):
        ball_velocity.x *= -1
        ball_velocity += player2_velocity
    if (ball_pos.y <= radius or screen.get_height() - ball_pos.y <= radius):
        ball_velocity.y *= -1

    player1_pos += player1_velocity 
    player2_pos += player2_velocity 
    if(ball_launched == False):
        ball_pos += player1_velocity
    else: 
        ball_pos += ball_velocity

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()