import math, pygame
from math import pi

# This is the walle class
class WallE:
    def turn(self, angle):
        x = self.direction[0]
        y = self.direction[1]
        self.direction = [int(x*math.cos(angle)-y*math.sin(angle)),
                            int(x*math.sin(angle)+y*math.cos(angle))]
        self.image = self.imageDict[str(self.direction)]

    def turn_right(self):
        self.turn(0.5*pi)

    def turn_left(self):
        self.turn(-0.5*pi)

    def check_on_box(self):
        if self.board[self.position[0]][self.position[1]] == 2:
            return True
        else:
            return False

    def check_wall(self):
        x = self.position[0] + self.direction[0]
        y = self.position[1] + self.direction[1]
        if -1 < x < len(self.board) and -1 < y < len(self.board[0]):
            if self.board[x][y]==1:
                return True
            return False
        else:
            return True

    def pick_up_box(self):
        if self.board[self.position[0]][self.position[1]] == 2:
            self.board[self.position[0]][self.position[1]] = 0
        else:
            self.broken = True

    def drop_box(self):
        if self.board[self.position[0]][self.position[1]] == 0:
            self.board[self.position[0]][self.position[1]] = 2
        else:
            self.broken = True

    #Requires an action
    def move(self):
        if not self.action:
            self.position[0] += self.direction[0]
            self.position[1] += self.direction[1]
            if -1 < self.position[0] < len(self.board) and -1 < self.position[1] < len(self.board[0]):
                if self.board[self.position[0]][self.position[1]]==1:
                    self.broken = true
            else:
                self.broken = True
            self.action = True
        else:
            self.broken = True

    def __init__(self, position, board, image):
        self.position = position
        self.board = board
        self.direction = [1,0]
        self.image = image
        il = pygame.transform.flip(self.image, True, False)
        ir = pygame.transform.rotate(self.image, 0)
        id = pygame.transform.rotate(self.image, -90)
        iu = pygame.transform.rotate(self.image, 90)
        self.imageDict = {'[1, 0]':ir, '[-1, 0]':il, '[0, 1]':id, '[0, -1]':iu}
        self.action = False
        self.broken = False

        #-----------------------------------------------------------------------
        # Declare variables you need here (Please formulate these variables
        # in ALL CAPS to avoid clashes with existing variable!!!)
        # and make sure they are at this indent level

        self.TURNS = 0
        self.DIRECTION = 0
        self.FINISHED = False
        self.WALKING_TO_OBSTACLE = True

    # Declare any help functions here (also use all caps for these!!)
    # and make sure they are at this indent level

    def CHECK_ON_WALL(self):
        self.turn_right()
        onwall = self.check_wall()
        self.turn_left()
        return onwall

# These are the functions you have to fill in
    def walk_back_and_forth(self):
        if not self.check_wall():
            self.move()
        elif self.TURNS<2:
            self.turn_left()
            self.TURNS+=1

    def walk_a_lap(self):
        if not self.TURNS == 4:
            if not self.check_wall():
                self.move()
            else:
                self.turn_right()
                self.TURNS+=1

    def find_the_box(self):
        if not self.FINISHED:
            if self.check_on_box():
                self.pick_up_box()
                self.FINISHED = True
            elif not self.check_wall():
                self.move()
            elif self.DIRECTION == 0:
                self.turn_right()
                self.move()
                self.turn_right()
                self.DIRECTION = 1
            else:
                self.turn_left()
                self.move()
                self.turn_left()
                self.DIRECTION = 0

    def swap_all_boxes(self):
        if not self.FINISHED:
            if self.check_on_box():
                self.pick_up_box()
            else:
                self.drop_box()
            if not self.check_wall():
                self.move()
            elif self.DIRECTION == 0:
                self.turn_right()
                if not self.check_wall():
                    self.move()
                else:
                    self.FINISHED = True
                self.turn_right()
                self.DIRECTION = 1
            else:
                self.turn_left()
                if not self.check_wall():
                    self.move()
                else:
                    self.FINISHED = True
                self.turn_left()
                self.DIRECTION = 0

    def walk_around_obstacle(self):
        if self.WALKING_TO_OBSTACLE:
            if not self.check_wall():
                self.move()
            else:
                if not self.FINISHED:
                    self.WALKING_TO_OBSTACLE = False
                    self.drop_box()
                    self.turn_left()
                    self.move()
        else:
            if self.check_on_box():
                self.turn_left()
                self.WALKING_TO_OBSTACLE = True
                self.FINISHED = True
            elif self.check_wall():
                self.turn_left()
            elif self.CHECK_ON_WALL():
                self.move()
            else:
                self.turn_right()
                self.move()
