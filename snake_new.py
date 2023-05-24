import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

font = pygame.font.Font('BreeSerif-Regular.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
GREEN1 = (0, 100, 0)
GREEN2 = (0, 201, 0)

BLOCK_SIZE = 20

class SnakeGame:
    def __init__(self, w=800, h=600):
        self.w = w
        self.h = h
        # initial display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # initial game state
        self.directions = [Direction.RIGHT, Direction.LEFT]
        self.heads = [
            Point(self.w / 4, self.h / 2),
            Point(3 * self.w / 4, self.h / 2)
        ]
        self.snakes = [
            [self.heads[0],
             Point(self.heads[0].x - BLOCK_SIZE, self.heads[0].y),
             Point(self.heads[0].x - (2 * BLOCK_SIZE), self.heads[0].y)],
            [self.heads[1],
             Point(self.heads[1].x + BLOCK_SIZE, self.heads[1].y),
             Point(self.heads[1].x + (2 * BLOCK_SIZE), self.heads[1].y)]
        ]
        
        self.quit_button = False
        self.alive = [True, True]
        self.scores = [0, 0]
        self.SPEED = 8
        self.food = None
        self.place_food()

    def place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)

        if self.food in self.snakes[0] or self.food in self.snakes[1]:
            self.place_food()

    def play_step(self):
        # Collect the user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_button = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.quit_button = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.directions[1] != Direction.RIGHT:
                    self.directions[1] = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.directions[1] != Direction.LEFT:
                    self.directions[1] = Direction.RIGHT
                elif event.key == pygame.K_UP and self.directions[1] != Direction.DOWN:
                    self.directions[1] = Direction.UP
                elif event.key == pygame.K_DOWN and self.directions[1] != Direction.UP:
                    self.directions[1] = Direction.DOWN
                elif event.key == pygame.K_a and self.directions[0] != Direction.RIGHT:
                    self.directions[0] = Direction.LEFT
                elif event.key == pygame.K_d and self.directions[0] != Direction.LEFT:
                    self.directions[0] = Direction.RIGHT
                elif event.key == pygame.K_w and self.directions[0] != Direction.DOWN:
                    self.directions[0] = Direction.UP
                elif event.key == pygame.K_s and self.directions[0] != Direction.UP:
                    self.directions[0] = Direction.DOWN
        
        # Move the snakes
        for snake_index in range(2):
            if self.alive[snake_index] != False:
                self.move(snake_index, self.directions[snake_index])
                self.snakes[snake_index].insert(0, self.heads[snake_index])

        # Check if game over
        game_over = False
        for snake_index in range(2):
            if self.is_collision(snake_index):
                game_over = True
                return game_over, self.scores

        # Place new food or just move
        for snake_index in range(2):
            if self.heads[snake_index] == self.food:
                self.scores[snake_index] += 1
                if self.SPEED < 20:  # Check if speed is less than 15
                    self.SPEED += 1
                self.place_food()
            else:
                if self.snakes[snake_index]:  # Check if the snake list is not empty
                    self.snakes[snake_index].pop()

        # Update the pygame UI and clock
        self.update_ui(game_over)
        self.clock.tick(self.SPEED)

        # Return game over and scores
        game_over = False
        return game_over, self.scores

    def update_ui(self,game_over):
        self.display.fill(BLACK)
        for snake_index in range(2):
            if snake_index == 0:
                for pt in self.snakes[snake_index]:
                    pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
            elif snake_index == 1:
                for pt in self.snakes[snake_index]:
                    pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.display, GREEN2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Player " + str(1) + " Score: " + str(self.scores[0]), True, WHITE)
        self.display.blit(text, [10, 0])

        text = font.render("Player " + str(2) + " Score: " + str(self.scores[1]), True, WHITE)
        self.display.blit(text, [self.w - 200, 0])

        winner_text = ""
        if game_over:
                if self.scores[0] > self.scores[1]:
                    winner_text = "Player 1 wins!"
                elif self.scores[1] > self.scores[0]:
                    winner_text = "Player 2 wins!"
                else:
                    winner_text = "It's a tie!"

        winner_render = font.render(winner_text, True, WHITE)
        self.display.blit(winner_render, [self.w/2 - 50, self.h/2 - 50])

        quit_text = font.render("Press Q to Quit", True, WHITE)
        self.display.blit(quit_text, [self.w - 190, self.h- 50])

        retry_text = font.render("Press R to retry", True, WHITE)
        self.display.blit(retry_text, [10, self.h - 50])

        pygame.display.flip()


    def move(self, snake_index, direction):
        x = self.heads[snake_index].x
        y = self.heads[snake_index].y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.heads[snake_index] = Point(x, y)

    def is_collision(self, snake_index):
        if (
            self.heads[0].x > self.w - BLOCK_SIZE or
            self.heads[0].x < 0 or
            self.heads[0].y > self.h - BLOCK_SIZE or
            self.heads[0].y < 0
            ):
            self.alive[0] = False
            if self.alive[1] == False:
                if self.alive[0] == False:
                    return True
        if (
            self.heads[1].x > self.w - BLOCK_SIZE or
            self.heads[1].x < 0 or
            self.heads[1].y > self.h - BLOCK_SIZE or
            self.heads[1].y < 0
            ):
            self.alive[1] = False
            if self.alive[1] == False:
                if self.alive[0] == False:
                    return True

        if self.heads[0] in self.snakes[1][1:] or self.heads[0] == self.heads[1]:
            self.alive[0] = False
            #self.alive[1] = False
            if self.alive[1] == False:
                if self.alive[0] == False:
                    return True
        if self.heads[1] in self.snakes[0][1:] or self.heads[1] == self.heads[0]:
            self.alive[1] = False
            #self.alive[0] = False
            if self.alive[1] == False:
                if self.alive[0] == False:
                    return True

    
        return False

if __name__ == '__main__':
    game = SnakeGame()

    # Game loop
    game_over = False
    scores = [0, 0]
    retry = False

    # Game loop
    while not game.quit_button:
        while not game_over and not game.quit_button:
            game_over, scores = game.play_step()
            game.update_ui(game_over)

        if game_over:
            game.update_ui(game_over)
            retry = False

        pygame.display.flip()

        while game_over and not retry and not game.quit_button:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.quit_button = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game.quit_button = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        retry = True
                        game_over = False
                        scores = [0, 0]
                        game = SnakeGame()
                        break

    pygame.quit()
