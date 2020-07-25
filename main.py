import random
import sys
import pygame
from pygame.locals import *

# Global variables
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'Images/bird.png'
BACKGROUND = 'Images/background.png'
PIPE = 'Images/pipe.png'

# Function for Showing welcome screen
def welcomeScreen():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_KP_ENTER:
                mainGame()
            else:
                SCREEN.blit(GAME_SPRITES['message'], (0, 0))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

# Function for main game
def mainGame():
    score = 0
    playerx = (SCREENWIDTH / 5)
    playery = (SCREENHEIGHT / 2)
    basex = 0

    # Creating Two pipes for bliting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMinVelY = -8
    playerMaxVelY = 10
    playerAccY = 1
    playerFlapAccv = -8  # Velocity during flapping
    playerFlapped = False

    while True:

        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        # if player collides with pipe
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            welcomeScreen()

        # Score checking
        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1

                # GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # Move pipes to the left

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add new pipe when the first pipe is crossing leftmost part of screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # If pipe is out of the screen remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # let's blit our sprites
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0

        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset, SCREENHEIGHT * 0.12))
            xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# Function for Bird collision
def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x'])+30 < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x'])+30 < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

# Function for Generating random coordinates for pipe
def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    pipex = SCREENWIDTH + 10
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1},  # upper pipe
        {'x': pipex, 'y': y2}  # lower pipe
    ]
    return pipe


if __name__ == '__main__':

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Created By Ajay')
    gameIcon = pygame.image.load('Images/icon.png')
    pygame.display.set_icon(gameIcon)

    # Images for game
    GAME_SPRITES['numbers'] = (
        pygame.image.load('Images/zero.png').convert_alpha(),
        pygame.image.load('Images/one.png').convert_alpha(),
        pygame.image.load('Images/two.png').convert_alpha(),
        pygame.image.load('Images/three.png').convert_alpha(),
        pygame.image.load('Images/four.png').convert_alpha(),
        pygame.image.load('Images/five.png').convert_alpha(),
        pygame.image.load('Images/six.png').convert_alpha(),
        pygame.image.load('Images/seven.png').convert_alpha(),
        pygame.image.load('Images/eight.png').convert_alpha(),
        pygame.image.load('Images/nine.png').convert_alpha(),
    )
    GAME_SPRITES['message'] = pygame.image.load('Images/welcome.jpg').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('Images/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # Sound effects for game
    GAME_SOUNDS['die'] = pygame.mixer.Sound('Sound/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('Sound/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('Sound/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('Sound/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('Sound/wing.wav')

    while True:
        welcomeScreen()
        mainGame()
