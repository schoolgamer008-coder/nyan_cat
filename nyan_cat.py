import pygame
import random
import math

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("nyan_cat")

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

font = pygame.font.SysFont("timesnewroman", 36, bold=True)
clock = pygame.time.Clock()

pygame.mixer.music.load("nyan_cat.mp3")
pygame.mixer.music.set_volume(0.1)

# BACKGROUND

class Background:
    def draw(self):
        t = pygame.time.get_ticks() * 0.002
        r = 15 + int(4 * math.sin(t))
        g = 12 + int(4 * math.sin(t + 2))
        b = 41 + int(4 * math.sin(t + 4))
        screen.fill((r, g, b))

# STAR FIELD

class StarField:
    def __init__(self, amount=120):
        self.stars = []
        for _ in range(amount):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            depth = random.choice([1, 2, 3])

            if depth == 1:
                speed, size = 0.1, 1
            elif depth == 2:
                speed, size = 0.2, 2
            else:
                speed, size = 0.4, 3

            drift = random.uniform(-0.15, 0.15)
            self.stars.append([x, y, speed, size, drift])

    def update(self):
        for star in self.stars:
            star[0] -= star[2]
            star[1] += star[4]

            if star[0] < 0:
                star[0] = WIDTH
                star[1] = random.randint(0, HEIGHT)

            if star[1] < 0 or star[1] > HEIGHT:
                star[4] *= -1

    def draw(self):
        for star in self.stars:
            pygame.draw.circle(screen, (255, 255, 255), (int(star[0]), int(star[1])), star[3])

# UI

class UI:
    def draw_start(self):
        start_msg = font.render("PRESS SPACE TO START", True, (255, 255, 255))
        exit_msg = font.render("PRESS ESC TO QUIT", True, (255, 255, 255))
        screen.blit(start_msg, (WIDTH//2 - 500, HEIGHT//2 - 220))
        screen.blit(exit_msg, (WIDTH//2 - 500, HEIGHT//2 - 160))

    def draw_gameover(self, score):
        msg = font.render(f"GAME OVER! FINAL SCORE: {score:,}", True, (255, 255, 255))
        restart_msg = font.render("PRESS SPACE TO RESTART", True, (255, 255, 255))
        exit_msg = font.render("PRESS ESC TO QUIT", True, (255, 255, 255))
        screen.blit(msg, (WIDTH//2 - 500, HEIGHT//2 - 220))
        screen.blit(restart_msg, (WIDTH//2 - 500, HEIGHT//2 - 160))
        screen.blit(exit_msg, (WIDTH//2 - 500, HEIGHT//2 - 100))

    def draw_score(self, score):
        score_surface = font.render(f"NYAN SCORE: {score:,}", True, (255, 255, 255))
        screen.blit(score_surface, (20, 20))

# GAME

class Game:
    def __init__(self):
        self.state = "START"
        self.start_ticks = 0
        self.score = 0

        self.background = Background()
        self.stars = StarField()
        self.ui = UI()

        self.cat_x = WIDTH // 2
        self.cat_y = HEIGHT // 2
        self.cat_speed = 5

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.state == "START":
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.play(-1)
                        self.state = "PLAYING"
                        self.start_ticks = pygame.time.get_ticks()
                    if event.key == pygame.K_ESCAPE:
                        return False

                elif self.state == "PLAYING":
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        self.state = "START"
                    if event.key == pygame.K_g:
                        pygame.mixer.music.stop()
                        self.state = "GAMEOVER"

                elif self.state == "GAMEOVER":
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.play(-1)
                        self.state = "PLAYING"
                        self.start_ticks = pygame.time.get_ticks()
                    if event.key == pygame.K_ESCAPE:
                        return False
        return True

    def update(self):
        if self.state == "PLAYING":
            self.stars.update()
            seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
            self.score = int((seconds ** 1.1) * 10)

        if pygame.key.get_pressed()[pygame.K_a]:
            self.cat_x -= self.cat_speed
        if pygame.key.get_pressed()[pygame.K_w]:
            for _ in range(19):  # jump
                    self.cat_y -= self.cat_speed*0.1
        if pygame.key.get_pressed()[pygame.K_d]:
            self.cat_x += self.cat_speed
# da ne gre dol zekrana
        self.cat_x = max(0, min(WIDTH - icon.get_width(), self.cat_x))
        self.cat_y = max(0, min(HEIGHT - icon.get_height(), self.cat_y))

    def draw(self):
        self.background.draw()

        if self.state == "PLAYING":
            self.stars.draw()
            self.ui.draw_score(self.score)

        elif self.state == "START":
            self.ui.draw_start()

        elif self.state == "GAMEOVER":
            self.ui.draw_gameover(self.score)
        screen.blit(icon, (self.cat_x, self.cat_y))

# MAIN LOOP

game = Game()
running = True

while running:
    running = game.handle_events()
    game.update()
    game.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
