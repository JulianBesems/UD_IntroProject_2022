# https://www.pygame.org/news
import pygame
import random

from WallE import *


# initialise the game window
pygame.init()
pygame.display.set_caption('Instruct Wall-E')

# usefull tool to get the monitor size:
print(pygame.display.Info())

# Define Game parameters
# screen size
screen_width = 1080
screen_height = 720
screen_centre = [screen_width/2, screen_height/2]
buffer = int(screen_height/100)
ps = int(buffer/10)

# set the game surface
screen = pygame.display.set_mode((screen_width, screen_height))

# extra surfacse overlayed for curser and photo interaction
walle_surface = pygame.surface.Surface((screen_width, screen_height), pygame.SRCALPHA, 32)
box_surface = pygame.surface.Surface((screen_width, screen_height), pygame.SRCALPHA, 32)
background = pygame.surface.Surface((screen_width, screen_height), pygame.SRCALPHA, 32)
menu_surface = pygame.surface.Surface((screen_width, screen_height), pygame.SRCALPHA, 32)

# a clock to keep track of the game progress
clock = pygame.time.Clock()

# Any commands that draw the initial state of the game
screen.fill(pygame.Color('white'))

# Create game board
# 0 is empty, 1 is a wall, 2 is a box
board = []
cell = screen_width/40
for i in range(int(screen_width/cell-2)):
    row = []
    for j in range(int(screen_height/cell-2)):
        row.append(0)
    board.append(row)

# Load images
walle_image = pygame.image.load('Resources/Wall_E.png')
walle_image = pygame.transform.scale(walle_image, (cell, cell))

broken_image = pygame.image.load('Resources/Wall_E_broken.png')
broken_image = pygame.transform.scale(broken_image, (cell, cell))

box_image = pygame.image.load('Resources/box.png')
box_image = pygame.transform.scale(box_image, (cell, cell))

walk_bf_image = pygame.image.load('Resources/walkToWallAndBack.png')
walk_bf_image = pygame.transform.scale(walk_bf_image, (screen_width*0.5, screen_height*0.1))

walk_around_image = pygame.image.load('Resources/WalkAroundObstacle.png')
walk_around_image = pygame.transform.scale(walk_around_image, (screen_width*0.5, screen_height*0.1))

walk_lap_image = pygame.image.load('Resources/walkALap.png')
walk_lap_image = pygame.transform.scale(walk_lap_image, (screen_width*0.5, screen_height*0.1))

findbox_image = pygame.image.load('Resources/findTheBox.png')
findbox_image = pygame.transform.scale(findbox_image, (screen_width*0.5, screen_height*0.1))

swapbox_image = pygame.image.load('Resources/swapAllBoxes.png')
swapbox_image = pygame.transform.scale(swapbox_image, (screen_width*0.5, screen_height*0.1))

wallE = WallE([0,0], board, walle_image)

# Draw basic board
background.fill(pygame.Color('Black'))
pygame.draw.rect(background, (255,255,255), pygame.Rect(cell,cell,len(board)*cell,len(board[0])*cell))
for i in range(len(board)):
    for j in range(len(board[0])):
        posx = i*cell+1.5*cell
        posy = j*cell+1.5*cell
        pygame.draw.circle(background, pygame.Color('grey'), [posx, posy], 2)


# Display the menu buttons
menu_surface.blit(walk_bf_image, [screen_width*0.25, screen_height*0.15])
menu_surface.blit(walk_lap_image, [screen_width*0.25, screen_height*0.3])
menu_surface.blit(findbox_image, [screen_width*0.25, screen_height*0.45])
menu_surface.blit(swapbox_image, [screen_width*0.25, screen_height*0.6])
menu_surface.blit(walk_around_image, [screen_width*0.25, screen_height*0.75])

# Update before the first frame
pygame.display.update()

status = 'select'

# The game loop, in here the behaviour of the game is defined.
# This loop is executed every frame.
while True:
    # wipe mouse surface:
    walle_surface.fill((0,0,0,0))
    box_surface.fill((0,0,0,0))

    mouse = pygame.mouse.get_pos()

    # Get key events to check if something is going on through some form of input.
    events = pygame.event.get()
    for event in events:
        # Check exit through x button window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Go through all key presses, which you can use to controll the game.
        elif event.type == pygame.KEYDOWN:
            # Check exit through esc
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if status == 'select':
             #checks if a mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Select the button that is clicked and set the game status that
                # is tested
                if screen_width*0.25 <= mouse[0] <= screen_width*0.75:
                    if screen_height*0.15 <= mouse[1] <= screen_height*0.25:
                        status = 'walk_back_and_forth'
                    if screen_height*0.3 <= mouse[1] <= screen_height*0.4:
                        status = 'walk_a_lap'
                    if screen_height*0.45 <= mouse[1] <= screen_height*0.55:
                        status = 'find_the_box'
                        xr = random.randint(1,len(board)-1)
                        yr = random.randint(1, len(board[0])-1)
                        board[xr][yr] = 2
                    if screen_height*0.6 <= mouse[1] <= screen_height*0.7:
                        status = 'swap_all_boxes'
                        for i in range(len(board)):
                            for j in range(len(board[0])):
                                r = random.randint(1,2)
                                if r == 1:
                                    board[i][j]=2
                    if screen_height*0.75 <= mouse[1] <= screen_height*0.85:
                        status = 'walk_around_obstacle'
                        rx1 = random.randint(int(0.2*len(board)),int(0.4*len(board)))
                        rx2 = random.randint(int(0.6*len(board)),int(0.8*len(board)))
                        ry1 = random.randint(int(0.2*len(board[0])),int(0.4*len(board[0])))
                        ry2 = random.randint(int(0.6*len(board[0])),int(0.8*len(board[0])))
                        for i in range(rx1, rx2):
                            j = int(0.5*len(board[0]))
                            board[i][j]=1
                            pygame.draw.rect(background, (0,0,0), pygame.Rect(i*cell+cell,j*cell+cell,cell,cell))
                        for j in range(ry1, ry2):
                            i = int(0.5*len(board))
                            board[i][j]=1
                            pygame.draw.rect(background, (0,0,0), pygame.Rect(i*cell+cell,j*cell+cell,cell,cell))
                        wallE.position = [0,int(0.5*len(board[0]))]



    wx = wallE.position[0]
    wy = wallE.position[1]
    posx = (wx+1)*cell
    posy = (wy+1)*cell
    walle_surface.blit(wallE.image, [posx, posy])

    for i in range(len(board)):
        for j in range(len(board[0])):
            posx = i*cell+cell
            posy = j*cell+cell
            if board[i][j] == 2:
                box_surface.blit(box_image, [posx, posy])


    if not wallE.broken:
        wallE.action = False
        if status=='walk_back_and_forth':
            wallE.walk_back_and_forth()
        elif status=='walk_a_lap':
            wallE.walk_a_lap()
        elif status=='find_the_box':
            wallE.find_the_box()
        elif status=='swap_all_boxes':
            wallE.swap_all_boxes()
        elif status=='walk_around_obstacle':
            wallE.walk_around_obstacle()
    else:
        wallE.image = broken_image

    # At the end of the loop update the screen and game time.
    screen.blit(background, [0,0])
    screen.blit(box_surface, [0,0])
    screen.blit(walle_surface, [0,0])
    if status == 'select':
        screen.blit(menu_surface, [0,0])

    pygame.display.update()

    # Edit this value to change the speed of WALL-E
    clock.tick(30)
