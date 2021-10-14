import time

import pygame
from pygame.locals import *

import sys
import random

# from pydub import AudioSegment
# AudioSegment.from_mp3("Cultist Base.mp3").export('myogg.ogg', format='ogg')

# settings
WIDTH = 1000  # ширина экрана
HEIGHT = 800  # высота экрана
FPS = 30  # кадры в секунду на основном экране
kol_boll = 20  # количество шаров
score = 0
text_color = (255, 255, 255)
text_size = 24
pause = False
Win = False

background_color = (5, 5, 10)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF)
pygame.display.set_caption("Boll eEe bash")
clock = pygame.time.Clock()

pygame.mixer.music.load("myogg.ogg")
pygame.mixer.music.set_volume(0.1)
backgraung_music = pygame.mixer.music.play(-1)

surface_text = pygame.Surface((200, 50))
font_text = pygame.font.SysFont('Aria', text_size)


class Boll(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((random.randint(10, 30), random.randint(10, 30)))
        self.image.fill((random.randint(70, 255), random.randint(70, 255), random.randint(70, 255)))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint((0 + self.image.get_size()[0]), (WIDTH - self.image.get_size()[0]))
        self.rect.centery = random.randint((0 + self.image.get_size()[1]), (HEIGHT - self.image.get_size()[1]))
        self.angle_move = [random.randint(-5, 5)/10, random.randint(-5, 5)/10]
        self.speed = random.randint(1, 5)

    def update(self):
        global x, y, running_main_win, pause, Win
        # проверка выхода за границы
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.angle_move[1] *= -1
        elif self.rect.top <= 0:
            self.rect.top = 0
            self.angle_move[1] *= -1
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.angle_move[0] *= -1
        elif self.rect.left <= 0:
            self.rect.left = 0
            self.angle_move[0] *= -1

        if score == 0:
            self.speed = random.randint(1, 5)
            self.image.fill((random.randint(70, 255), random.randint(70, 255), random.randint(70, 255)))
            self.rect.centerx = random.randint((0 + self.image.get_size()[0]), (WIDTH - self.image.get_size()[0]))
            self.rect.centery = random.randint((0 + self.image.get_size()[1]), (HEIGHT - self.image.get_size()[1]))

        self.rect.x += self.angle_move[0]*self.speed
        self.rect.y += self.angle_move[1]*self.speed

        if score < 600:
            self.speed += 0.05
        elif 700 < score < 1400:
            self.speed -= 0.1
        elif 1450 < score < 1650:
            self.speed += 0.2
        elif 1700 < score < 2050:
            self.speed += 0.07
            self.image.fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
        elif score == 2050:
            self.angle_move = [random.randint(-5, 5) / 10, random.randint(-5, 5) / 10]
        elif 2054 < score < 2150:
            self.speed += 0.02
            self.image.fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
        elif score == 2150:
            self.angle_move = [random.randint(-5, 5) / 10, random.randint(-5, 5) / 10]
        elif 21054 < score < 2350:
            self.speed += 0.015
        elif score == 2600:
            Win = True

        if self.Mausclick().collidepoint(pygame.mouse.get_pos()):
            pause = True

    def Mausclick(self):
        return self.rect


All_sprites = pygame.sprite.Group()

for i in range(kol_boll):
    boll = Boll()
    All_sprites.add(boll)

running_main_win = True
while running_main_win:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # проверка на нажатие крестика для выхода
            sys.exit()

    if Win:
        print(f"Score: {int(score / 10)}")
        print("Пссс...")
        time.sleep(1)
        print("Пссс...")
        time.sleep(1)
        print("Ты выйграл\n красава")
        running_main_win = False

    score += 1
    render_text = font_text.render(f"score: {int(score/10)}", False, text_color)

    if score % 50 == 0 and not score == 0:
        background_color = (random.randint(5, 20), random.randint(5, 20), random.randint(5, 20))
        text_color = (255, 255, 255)
    elif score % 601 == 0:
        background_color = (random.randint(220, 255), random.randint(220, 255), random.randint(220, 255))
        text_color = (0, 0, 0)

    if pause:
        pause = False
        print(f"Score: {int(score / 10)}")
        score = 0
        time.sleep(1.5)

    # обновление спрайтов
    All_sprites.update()

    # Отрисовка
    screen.fill(background_color)
    screen.blit(render_text, (10, 10))
    All_sprites.draw(screen)
    pygame.display.flip()
