# Python - Snake Game

Technology used: *python, pygame, etc*

## Abstract

Simple snake game created with python and its pygame library. 

## Code

Game code uses classes to define direction, position of the snake parts and status of the game.
To get to know the pygame library and get used to the "if" logic implementation I used no imported images to create "snake look".

Unitests are used to check the correct implementation of changing game status:
- changing direction
- posiibility of changing direction
- crossing the screen border/appearing on the other side
- eating the food - snake growth
- collision - game over

There is an option to pause the game with "p" key and continue with "space" bar which is show on the pause screen.
After snake death it is possible to start a new game or quit.
