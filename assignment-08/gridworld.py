from gym import spaces
import numpy as np
import pygame
import math 
import time 
import sys 

class GridWorld: 

    # Arrows 
    ARROWS = [
            pygame.image.load('resources/up_arrow.jpg'), 
            pygame.image.load('resources/down_arrow.jpg'), 
            pygame.image.load('resources/left_arrow.jpg'),
            pygame.image.load('resources/right_arrow.jpg')
    ]

    # Colors 
    WHITE = (255, 255, 255)
    RED   = (255,   0,   0)
    GREEN = (  0, 255,   0)
    BLACK = (  0,   0,   0)
    LIGHT_RED = (255, 115, 129) 

    # Player positiion
    PLAYER_POSITION = [0, 0]

    # Actions 
    UP    = 0
    DOWN  = 1 
    LEFT  = 2 
    RIGHT = 3


    def __init__(self, WINDOW_SIZE, RECTANGLE_COUNT, GRID_GAP):

        # Initializes parameters 
        self.DISPLAY = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.ROW_COUNT = self.COL_COUNT = int(math.sqrt(RECTANGLE_COUNT)) 
        self.OBSTACLE_POSITION = [self.ROW_COUNT - 4, self.COL_COUNT - 2]
        self.GOAL_POSITION = [self.ROW_COUNT - 2, self.COL_COUNT - 2]
        self.RECTANGLE_SIZE = int(WINDOW_SIZE / self.COL_COUNT) 
        self.RECTANGLE_COUNT = RECTANGLE_COUNT
        self.MAX_MOVES = RECTANGLE_COUNT;
        self.moves = 0; 
        self.GRID_GAP = GRID_GAP

        # Resizes the arrows 
        for i in range(len(self.ARROWS)): 
            self.ARROWS[i] = pygame.transform.scale(self.ARROWS[i], (self.RECTANGLE_SIZE - self.GRID_GAP, self.RECTANGLE_SIZE - self.GRID_GAP))

        # Fills the display (background) as black
        self.DISPLAY.fill(self.BLACK)

        # Sets up the observation and action space 
        high = np.array([self.ROW_COUNT -1, self.COL_COUNT - 1], dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)
        self.action_space = spaces.Discrete(4)
        
    
    def reset(self):
        self.PLAYER_POSITION = [0, 0]
        self.moves = 0
        return self.PLAYER_POSITION

   
    def render(self, q_table):
        pygame.init()
        self.drawGrid(q_table)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        pygame.time.delay(1000)
        
    
    def drawGrid(self, q_table):
        for row in range(self.ROW_COUNT):
            for col in range(self.COL_COUNT):

                # Draws the arrows 
                action = np.argmax(q_table[(row, col)])
                self.DISPLAY.blit(self.ARROWS[action], (col * self.RECTANGLE_SIZE, row * self.RECTANGLE_SIZE))

                rectangle = pygame.Rect(col * self.RECTANGLE_SIZE, row * self.RECTANGLE_SIZE,
                                        self.RECTANGLE_SIZE - self.GRID_GAP, self.RECTANGLE_SIZE - self.GRID_GAP)
                
                # Draws the players, goal and obstacle 
                if [row, col] == self.PLAYER_POSITION: 
                    pygame.draw.rect(self.DISPLAY, self.RED, rectangle)
                elif [row, col] == self.GOAL_POSITION:
                    pygame.draw.rect(self.DISPLAY, self.GREEN, rectangle)
                elif [row, col] == self.OBSTACLE_POSITION: 
                    pygame.draw.rect(self.DISPLAY, self.BLACK, rectangle)

    
    def step(self, action):
        self.moves += 1

        newPos = self.PLAYER_POSITION.copy()
        oldPos = self.PLAYER_POSITION.copy()

        done = False 

        # Moves the player 
        if action == self.UP:    newPos[0] = self.PLAYER_POSITION[0] - 1
        if action == self.DOWN:  newPos[0] = self.PLAYER_POSITION[0] + 1
        if action == self.LEFT:  newPos[1] = self.PLAYER_POSITION[1] - 1
        if action == self.RIGHT: newPos[1] = self.PLAYER_POSITION[1] + 1

        # Checks if new position is valid         
        if 0 <= newPos[0] < self.ROW_COUNT and 0 <= newPos[1] < self.COL_COUNT:
            self.PLAYER_POSITION = newPos

        if self.PLAYER_POSITION == self.GOAL_POSITION: reward = 10.0; done = True 
        elif self.PLAYER_POSITION == self.OBSTACLE_POSITION: reward = -10.0; done = True
        else: reward = -1.0

        if self.moves >= self.MAX_MOVES: done = True

        return self.PLAYER_POSITION, reward, done, {}