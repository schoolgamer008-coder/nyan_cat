# nyan_cat

import pygame
import random

pygame.init()
pygame.mixer.init()

font = pygame.font.SysFont("timesnewroman", 36, bold=True)

pygame.mixer.music.load("nyan_cat.mp3")
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
        speed = 0.1
        size = 1

    elif depth == 2:
        speed = 0.2
        size = 2
        
    else:
        speed = 0.4
        size = 3

    stars.append([x, y, speed, size])

running = True
game_state = "START"
score = 0
start_ticks = 0

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == "START":

                if event.key == pygame.K_SPACE:
                    game_state = "PLAYING"
                    start_ticks = pygame.time.get_ticks()
                    pygame.mixer.music.play(-1)

                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif game_state == "PLAYING":

                # kle pride funkcija --> def character
                if event.key == pygame.K_ESCAPE:
                    game_state = "START"
                    pygame.mixer.music.stop()

                elif event.key == pygame.K_g: #ker še ni collisionov, da lahko sploh pridem tja
                    game_state = "GAMEOVER"
                    pygame.mixer.music.stop()

            elif game_state == "GAMEOVER":

                if event.key == pygame.K_SPACE:
                    game_state = "PLAYING"
                    start_ticks = pygame.time.get_ticks()
                    pygame.mixer.music.play(-1)

                elif event.key == pygame.K_ESCAPE:
                    running = False

    screen.fill((15, 12, 41)) #deep space barva

    if game_state == "START":
        start_msg = font.render("PRESS SPACE TO START", True, (255, 255, 255))
        exit_msg = font.render("PRESS ESC TO QUIT", True, (255, 255, 255))
        screen.blit(start_msg, (WIDTH//2 - 500, HEIGHT//2 - 220))
        screen.blit(exit_msg, (WIDTH//2 - 500, HEIGHT//2 - 160))

    elif game_state == "PLAYING":

        for star in stars:
            star[0] -= star[2]

            if star[0] < 0:
                star[0] = WIDTH
                star[1] = random.randint(0, HEIGHT)

            pygame.draw.circle(screen, (255, 255, 255), (star[0], star[1]), star[3])

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        score = int((seconds ** 1.1) * 10)

        score_surface = font.render(f"NYAN SCORE: {score:,}", True, (255, 255, 255))
        screen.blit(score_surface, (20, 20))
        
    elif game_state == "GAMEOVER":
        msg = font.render(f"GAME OVER! FINAL SCORE: {score:,}", True, (255, 255, 255))
        restart_msg = font.render("PRESS SPACE TO RESTART", True, (255, 255, 255))
        exit_msg = font.render("PRESS ESC TO QUIT", True, (255, 255, 255))
        screen.blit(msg, (WIDTH//2 - 500, HEIGHT//2 - 220))
        screen.blit(restart_msg, (WIDTH//2 - 500, HEIGHT//2 - 160))
        screen.blit(exit_msg, (WIDTH//2 - 500, HEIGHT//2 - 100))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()