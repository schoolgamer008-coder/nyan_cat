# nyan_cat

import pygame
import random

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("nyan_cat.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.01)

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("nyan_cat")

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
FPS = 60

stars = []

for i in range(120):

    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)

    depth = random.choice([1, 2, 3])

    if depth == 1:
        speed = 0.2
        size = 1

    elif depth == 2:
        speed = 0.4
        size = 2
        
    else:
        speed = 0.8
        size = 3

    stars.append([x, y, speed, size])

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for star in stars:
        star[0] -= star[2]

        if star[0] < 0:
            star[0] = WIDTH
            star[1] = random.randint(0, HEIGHT)

        pygame.draw.circle(screen, (255, 255, 255), (star[0], star[1]), star[3])

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()