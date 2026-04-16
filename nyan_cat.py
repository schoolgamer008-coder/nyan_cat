
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

# PLATFORM

class Platform:
    def __init__(self):
        self.width = random.randint(100, 200)
        self.height = 20
        self.x = -self.width
        self.y = random.randint(100, HEIGHT - 100)
        self.speed = random.uniform(2, 4)

    def update(self):
        self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, (200, 100, 200), (self.x, self.y, self.width, self.height))

    def off_screen(self):
        return self.x > WIDTH

# UI

class UI:
    def draw_start(self):
        screen.blit(font.render("PRESS SPACE TO START", True, (255,255,255)), (WIDTH//2 - 500, HEIGHT//2 - 220))
        screen.blit(font.render("PRESS ESC TO QUIT", True, (255,255,255)), (WIDTH//2 - 500, HEIGHT//2 - 160))

    def draw_gameover(self, score):
        screen.blit(font.render(f"GAME OVER! FINAL SCORE: {score:,}", True, (255,255,255)), (WIDTH//2 - 500, HEIGHT//2 - 220))
        screen.blit(font.render("PRESS SPACE TO RESTART", True, (255,255,255)), (WIDTH//2 - 500, HEIGHT//2 - 160))
        screen.blit(font.render("PRESS ESC TO QUIT", True, (255,255,255)), (WIDTH//2 - 500, HEIGHT//2 - 100))

    def draw_score(self, score):
        screen.blit(font.render(f"NYAN SCORE: {score:,}", True, (255,255,255)), (20, 20))

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

        self.gravity = 0.5
        self.velocity_y = 0

        self.platforms = []
        self.spawn_timer = 0

        # JUMP SYSTEM
        self.jump_count = 0
        self.max_jumps = 2
        self.jump_hold_time = 0
        self.max_jump_hold = 0.5
        self.is_jumping = False

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

                elif self.state == "GAMEOVER":
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        pygame.mixer.music.play(-1)
                        self.state = "PLAYING"
                    if event.key == pygame.K_ESCAPE:
                        return False
        return True

    def reset_game(self):
        self.cat_x = WIDTH // 2
        self.cat_y = HEIGHT // 2
        self.velocity_y = 0
        self.platforms = []
        self.spawn_timer = 0
        self.start_ticks = pygame.time.get_ticks()
        self.jump_count = 0

    def update(self):
        if self.state == "PLAYING":
            self.stars.update()

            seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
            self.score = int((seconds ** 1.1) * 10)

            dt = clock.get_time() / 1000
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.cat_x -= self.cat_speed
            if keys[pygame.K_d]:
                self.cat_x += self.cat_speed

            # JUMP
            if keys[pygame.K_w]:
                if not self.is_jumping and self.jump_count < self.max_jumps:
                    self.velocity_y = -10
                    self.is_jumping = True
                    self.jump_hold_time = 0
                    self.jump_count += 1

            if self.is_jumping:
                self.jump_hold_time += dt
                if self.jump_hold_time < self.max_jump_hold:
                    self.velocity_y -= 0.3

            if not keys[pygame.K_w]:
                self.is_jumping = False

            # gravity
            self.velocity_y += self.gravity
            self.cat_y += self.velocity_y

            # spawn platform
            self.spawn_timer += 1
            if self.spawn_timer > 60:
                self.platforms.append(Platform())
                self.spawn_timer = 0

            # update platform
            for platform in self.platforms:
                platform.update()

            # collision
            cat_rect = pygame.Rect(self.cat_x, self.cat_y, icon.get_width(), icon.get_height())
            for platform in self.platforms:
                plat_rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)
                if cat_rect.colliderect(plat_rect) and self.velocity_y > 0:
                    self.cat_y = platform.y - icon.get_height()
                    self.velocity_y = 0
                    self.jump_count = 0

            # remove old
            self.platforms = [p for p in self.platforms if not p.off_screen()]

            # bounds
            self.cat_x = max(0, min(WIDTH - icon.get_width(), self.cat_x))

            if self.cat_y >= HEIGHT - icon.get_height():
                self.jump_count = 0

            if self.cat_y > HEIGHT:
                pygame.mixer.music.stop()
                self.state = "GAMEOVER"

    def draw(self):
        self.background.draw()

        if self.state == "PLAYING":
            self.stars.draw()

            for platform in self.platforms:
                platform.draw()

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
