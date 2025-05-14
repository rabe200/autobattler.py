# main.py

import pygame
from animation_files import AnimationFiles
from animation_idle import IdleAnimation

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Idle Animation with Dynamic Loading")

# Load all animations from the 'animations' folder
animation_files = AnimationFiles('animations')

# Initialize the idle animation
idle_animation = IdleAnimation(animation_files, 'frog1-spritesheet')
idle_animation2 = IdleAnimation(animation_files, 'frog-warrior')
idle_animation3 = IdleAnimation(animation_files, 'cat-spear')
idle_animation4 = IdleAnimation(animation_files, 'fatzo')

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and draw the idle animation
    idle_animation.update()
    idle_animation2.update()
    idle_animation3.update()
    idle_animation4.update()
    screen.fill((255, 0, 50))
    idle_animation.draw(screen, (200, 300))
    idle_animation2.draw(screen, (300, 300))
    idle_animation3.draw(screen, (400, 300))
    idle_animation4.draw(screen, (500, 300))

    pygame.display.flip()

pygame.quit()
