# Lab 11: Project Handoff
You may now consider creating a branch of your respository to work on the project. 


## Lab Task 1: Create a Class Diagram of the lab11 folder
Consider each file a package for the UML diagram.
Submit the class diagram by the end of the lab session to assignment 'Lab 11: Project Handoff (Task 1)'.

## Lab Task 2: Complete the pygame_ai_player.py file
Complete the pygame_ai_player.py file with the two classes scaffolded out for you.
Make sure that the game runs through the agent_environment.py file fully autonomously.
You can just use some hard coded actions for the agent to take at this point. 
Submit the code by the end of the week to assignment 'Lab 11: Project Handoff (Task 2)'.

> Code created in this lab was created with help from ChatGPT. \n
> The prompt used was:
>     Create a code to move a sprite across a pygame window with a given start location and end location with a constant speed. 
> The response was:
```
import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Sprite Movement")

# Set up the sprite
SPRITE_WIDTH = 50
SPRITE_HEIGHT = 50
sprite = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT))
sprite.fill((255, 0, 0)) # red color

# Set up the start and end positions
start_pos = (100, 100)
end_pos = (500, 400)

# Calculate the distance and direction between the two positions
distance = math.sqrt((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2)
direction = ((end_pos[0] - start_pos[0]) / distance, (end_pos[1] - start_pos[1]) / distance)

# Set up the sprite's initial position and speed
sprite_pos = start_pos
speed = 5

# Start the game loop
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the sprite
    sprite_pos = (sprite_pos[0] + direction[0] * speed, sprite_pos[1] + direction[1] * speed)

    # Check if the sprite has reached the end position
    if math.sqrt((sprite_pos[0] - end_pos[0]) ** 2 + (sprite_pos[1] - end_pos[1]) ** 2) < speed:
        sprite_pos = end_pos
        running = False

    # Draw the sprite and the background
    window.fill((255, 255, 255)) # white background
    window.blit(sprite, sprite_pos)

    # Update the display and tick the clock
    pygame.display.update()
    clock.tick(60) # limit to 60 frames per second

# Quit Pygame
pygame.quit()
```
