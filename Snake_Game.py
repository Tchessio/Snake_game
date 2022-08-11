# import
import pygame
import numpy as np
import random

pygame.init()

# Basic data
SCREEN_W = 500
SCREEN_H = 500
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (24, 0, 255)
FOOD_COLOR = (255, 17, 0)
BLOCK_SIZE = 20
SPEED = 80
DIRECTION = "D"
FONT = pygame.font.Font("arial.ttf", 20)
GAME = 0

# set up the screen, clock and points
screen = pygame.display.set_mode([SCREEN_W, SCREEN_H])


# set up snake
class Snake:
    # snake is the np array. It starts with 3 elements located on the top/left corner
    body = np.array([[0, 0], [0, 1], [0, 2]])
    head = body[-1]
    direction = DIRECTION
    length = 3


# set up food. The first food starts with a fixed position. TODO randomise it
class Food:
    x = 0
    y = 6


# snake movement
def move(x, y):
    if Snake.direction == "D":
        new_head = [x, y + 1]
        Snake.body = np.append(Snake.body, [new_head], axis=0)
    elif Snake.direction == "U":
        new_head = [x, y - 1]
        Snake.body = np.append(Snake.body, [new_head], axis=0)
    elif Snake.direction == "R":
        new_head = [x + 1, y]
        Snake.body = np.append(Snake.body, [new_head], axis=0)
    elif Snake.direction == "L":
        new_head = [x - 1, y]
        Snake.body = np.append(Snake.body, [new_head], axis=0)

    Snake.head = Snake.body[-1]
    if not eat_food():
        Snake.body = np.delete(Snake.body, 0, axis=0)


# function rand_food
def rand_food():
    Food.x = random.randint(0, int(SCREEN_W / BLOCK_SIZE - 1))
    Food.y = random.randint(0, int(SCREEN_H / BLOCK_SIZE - 1))
    for block in Snake.body:
        if Food.x == block[0] and Food.y == block[1]:
            rand_food()


# function eat food
def eat_food():
    if Snake.head[0] == Food.x and Snake.head[1] == Food.y:
        Snake.length += 1
        rand_food()
        return True
    else:
        return False


# check if the snake dies
def check_collision():
    # check if snake crashes with the border
    if Snake.head[0] < 0 or Snake.head[1] < 0 or Snake.head[0] > SCREEN_W / BLOCK_SIZE - 1 or \
            Snake.head[1] > SCREEN_H / BLOCK_SIZE - 1:
        reset()
    # check if snake eats himself
    for block in Snake.body[0:Snake.length - 1]:
        if block[0] == Snake.head[0] and block[1] == Snake.head[1]:
            reset()


def reset():
    
    # print points
    global GAME
    GAME += 1
    print("Game " + str(GAME) + ". You have earned " + str(Snake.length) + " points")
    
    
# reset the game
    Snake.body = np.array([[0, 0], [0, 1], [0, 2]])
    Snake.head = Snake.body[-1]
    Snake.direction = "D"
    Snake.length = 3
    rand_food()


# run the game
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check for user input TODO on esc button exits the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and not Snake.direction == "U":
                Snake.direction = "D"
            elif event.key == pygame.K_UP and not Snake.direction == "D":
                Snake.direction = "U"
            elif event.key == pygame.K_RIGHT and not Snake.direction == "L":
                Snake.direction = "R"
            elif event.key == pygame.K_LEFT and not Snake.direction == "R":
                Snake.direction = "L"
    # fill the background
    screen.fill(BACKGROUND_COLOR)

    # draw a snake
    for block in Snake.body:
        x = block[0]
        y = block[1]
        pygame.draw.rect(screen, SNAKE_COLOR, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # draw a food
    pygame.draw.rect(screen, FOOD_COLOR, (Food.x * BLOCK_SIZE, Food.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # move the snake
    move(Snake.head[0], Snake.head[1])

    # check if the food was eaten
    eat_food()

    # check for the collision
    check_collision()

    # status
    #    s_loc = font.render(str(Snake.body), False, (255, 255, 255))
    #    f_x = font.render(str(Food.x), False, (255, 255, 255))
    #    f_y = font.render(str(Food.y), False, (255, 255, 255))
    #    screen.blit(s_loc, (0, 0))
    #    screen.blit(f_x, (0, 50))
    #    screen.blit(f_y, (0, 100))

    pygame.time.wait(SPEED)
    pygame.display.flip()

pygame.quit()