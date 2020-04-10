# Snake Game
# Written by Andrew Eldridge
# 4/9/2020

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# global variables
width = 0
rows = 0
s = None
food = None


class Snake:
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Square(pos)
        self.body.append(self.head)
        self.x_dir = 0
        self.y_dir = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT] and self.x_dir != 1:
                    self.x_dir = -1
                    self.y_dir = 0
                    self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
                elif keys[pygame.K_RIGHT] and self.x_dir != -1:
                    self.x_dir = 1
                    self.y_dir = 0
                    self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
                elif keys[pygame.K_UP] and self.y_dir != 1:
                    self.x_dir = 0
                    self.y_dir = -1
                    self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
                elif keys[pygame.K_DOWN] and self.y_dir != -1:
                    self.x_dir = 0
                    self.y_dir = 1
                    self.turns[self.head.pos[:]] = [self.x_dir, self.y_dir]
        for i, c in enumerate(self.body):
            pos = c.pos[:]
            if pos in self.turns:
                turn = self.turns[pos]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(pos)
            else:
                if c.x_dir == -1 and c.pos[0] <= 0:
                    c.pos = (rows-1, c.pos[1])  # moving from left border to right border
                if c.x_dir == 1 and c.pos[0] >= rows-1:
                    c.pos = (0, c.pos[1])  # moving from right border to left border
                if c.y_dir == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], rows-1)  # moving from top border to bottom border
                if c.y_dir == 1 and c.pos[1] >= rows-1:
                    c.pos = (c.pos[0], 0)  # moving from bottom border to top border
                else:
                    c.move(c.x_dir, c.y_dir)

    def reset(self, pos):
        self.head = Square(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.x_dir = 0
        self.y_dir = 1

    def add_square(self):
        tail = self.body[-1]
        x, y = tail.x_dir, tail.y_dir
        if x == 1 and y == 0:
            self.body.append(Square((tail.pos[0]-1, tail.pos[1])))  # snake is moving right, append tail left
        elif x == -1 and y == 0:
            self.body.append(Square((tail.pos[0]+1, tail.pos[1])))  # snake is moving left, append tail right
        elif x == 0 and y == 1:
            self.body.append(Square((tail.pos[0], tail.pos[1]-1)))  # snake is moving down, append tail top
        elif x == 0 and y == -1:
            self.body.append(Square((tail.pos[0], tail.pos[1]+1)))  # snake is moving up, append tail bottom
        self.body[-1].x_dir = x
        self.body[-1].y_dir = y

    def draw(self, win):
        for _, c in enumerate(self.body):
            c.draw(win)


class Square:
    def __init__(self, start, color=(255, 0, 0)):
        self.pos = start
        self.x_dir = 1
        self.y_dir = 0
        self.color = color

    def move(self, x_dir, y_dir):
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.pos = (self.pos[0] + self.x_dir, self.pos[1] + self.y_dir)

    def draw(self, win):
        grid_offset = width // rows
        pygame.draw.rect(win, self.color, (self.pos[0]*grid_offset+1, self.pos[1]*grid_offset+1, grid_offset-1, grid_offset-1))


def draw_grid(win):
    space_between = width // rows
    x = y = 0
    for _ in range(rows):
        x += space_between
        y += space_between
        pygame.draw.line(win, (255, 255, 255), (x, 0), (x, width))  # draw vertical grid lines
        pygame.draw.line(win, (255, 255, 255), (0, y), (width, y))  # draw horizontal grid lines


def redraw_window(win):
    win.fill((0, 0, 0))
    s.draw(win)
    food.draw(win)
    draw_grid(win)
    pygame.display.update()


def generate_food():
    pos = s.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), pos))) > 0:
            continue
        else:
            break
    return x, y


def main():
    global width, rows, s, food
    width = height = 500
    win = pygame.display.set_mode((width, height))
    rows = 20
    s = Snake((255, 0, 0), (10, 10))
    food = Square(generate_food(), color=(0, 255, 0))

    flag = True
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(30)
        clock.tick(10)
        s.move()
        if s.body[0].pos == food.pos:
            s.add_square()
            food = Square(generate_food(), color=(0, 255, 0))
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                s.reset((10, 10))
                break
        redraw_window(win)


main()
