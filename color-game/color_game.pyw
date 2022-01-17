import pygame
import random
import sys
pygame.init()
WIDTH = 800  # ширена экрана
HEIGHT = 600  # высота экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Game")
clock = pygame.time.Clock()
FPS = 30
exit_in_menu_int = 0
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
Red = (255, 0, 0)
Orange = (255, 165, 0)
Yellow = (255, 255, 0)
Green = (0, 128, 0)
Blue = (0, 0, 205)
Purple = (128, 0, 128)
DimGrey = (50, 50, 50)
speed = 20
cash = 0
cash_level = 0
level = 0
hp = 10
true_cash = 0


class Text(pygame.sprite.Sprite):
    def __init__(self, text_color, circle_color, text, HP, LEVEL):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.image.fill((50, 50, 50, 200))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        pygame.draw.circle(self.image, (*circle_color, 255), (WIDTH//2, 450), 60)
        self.font = pygame.font.SysFont('Arial', 100)
        render = self.font.render(text, True, text_color)
        self.image.blit(render, (250 , 100))
        # hp
        self.font = pygame.font.SysFont('Arial', 30)
        render = self.font.render("Hp - "+ str(HP), True, WHITE)
        self.image.blit(render, (15, 15))
        # level
        self.font = pygame.font.SysFont('Arial', 30)
        render = self.font.render("Level - "+ str(LEVEL), True, WHITE)
        self.image.blit(render, (650, 15))


def Menu(exit_in_menu_int, clock, screen): # меню
    class Button_game_menu(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((350, 120))
            self.image.fill((34, 139, 34))
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH//2
            self.rect.y = 50
            self.font = pygame.font.SysFont('Arial', 100)
            render = self.font.render("Start", False, (255, 255, 255))
            self.image.blit(render, (100, 10))

        def Mausclick(self):
            return self.rect

    class Button_exit_menu(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((350, 90))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH//2
            self.rect.y = 200
            self.font = pygame.font.SysFont('Arial', 70)
            render = self.font.render("Exit", False, (255, 255, 255))
            self.image.blit(render, (130, 10))

        def Mausclick(self):
            return self.rect

    class Text_menu(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.surface.Surface((800, 300)).convert_alpha()
            self.image.fill((0, 0, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH//2
            self.rect.y = 300
            self.font = pygame.font.SysFont('Arial', 30)
            render = self.font.render("Если цвет надписи соотвецтвует цвету кружка то", True, Green)
            self.image.blit(render, (50, 20))
            render = self.font.render("нажимайте <-, в ином случее ->, и делайте это быстро", True, Green)
            self.image.blit(render, (50, 60))
            render = self.font.render("Счёт: " + str(cash_level), True, Orange)
            self.image.blit(render, (50, 150))


    All_Menu_sprites = pygame.sprite.Group()
    button_1_menu = Button_game_menu()
    button_2_menu = Button_exit_menu()
    text = Text_menu()
    All_Menu_sprites.add(button_1_menu)
    All_Menu_sprites.add(button_2_menu)
    All_Menu_sprites.add(button_2_menu)
    All_Menu_sprites.add(text)

    # цикл главного миню
    Glav_menu_while = True
    while Glav_menu_while:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_1_menu.Mausclick().collidepoint(event.pos):
                    Glav_menu_while = False
                    if exit_in_menu_int > 0:
                        Up_Window(exit_in_menu_int)
                if event.button == 1 and button_2_menu.Mausclick().collidepoint(event.pos):
                    sys.exit()
            if event.type  == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    Glav_menu_while = False
        All_Menu_sprites.update()
        screen.fill(DimGrey)
        All_Menu_sprites.draw(screen)
        pygame.display.flip()


Menu(exit_in_menu_int, clock, screen)
def Up_Window(exit_in_menu_int):
    global player_hunger_int, cash, speed, level, hp, true_cash, cash_level
    if exit_in_menu_int == 0: # если игрок зашол в игру в первые за сэсию то это отслеживается
        exit_in_menu_int = 1
    x_text_color = random.choice((Red, Orange, Yellow, Green, Blue, Purple))
    x_circle_color = random.choice((Red, Orange, Yellow, Green, Blue, Purple, x_text_color, x_text_color, x_text_color, x_text_color, x_text_color, x_text_color))
    x_text = random.choice(("Red", "Orange", "Yellow", "Green", "Blue", "Purple"))
    all_sprites = pygame.sprite.Group()
    textcol = Text(x_text_color, x_circle_color, x_text, hp, level)
    all_sprites.add(textcol)
    running_main_win = True # главный цикл
    # цикл главного экрана
    while running_main_win:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # проверка на нажатие крестика для выхода
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # при нажатии эскейпа выход в главное меню
                    running_main_win = False
                    Menu(exit_in_menu_int, clock, screen)
                if event.key == pygame.K_LEFT:
                    if x_text_color == x_circle_color:
                        cash = 0
                        level += 1
                        true_cash += 1
                        if true_cash == 5:
                            true_cash = 0
                            speed += 10
                    else:
                        cash = 0
                        hp -= 1
                    x_text_color = random.choice((Red, Orange, Yellow, Green, Blue, Purple))
                    x_circle_color = random.choice((Red, Orange, Yellow, Green, Blue, Purple, x_text_color, x_text_color, x_text_color, x_text_color, x_text_color, x_text_color))
                    x_text = random.choice(("Red", "Orange", "Yellow", "Green", "Blue", "Purple"))
                    all_sprites.empty()
                    textcol = Text(x_text_color, x_circle_color, x_text, hp, level)
                    all_sprites.add(textcol)
                if event.key == pygame.K_RIGHT:
                    if x_text_color != x_circle_color:
                        cash = 0
                        level += 1
                        if true_cash == 5:
                            true_cash = 0
                            speed += 10
                    else:
                        cash = 0
                        hp -= 1
                    x_text_color = random.choice((Red, Orange, Yellow, Green, Blue, Purple))
                    x_circle_color = random.choice((Red, Orange, Yellow, Green, Blue, Purple, x_text_color, x_text_color, x_text_color, x_text_color, x_text_color, x_text_color))
                    x_text = random.choice(("Red", "Orange", "Yellow", "Green", "Blue", "Purple"))
                    all_sprites.empty()
                    textcol = Text(x_text_color, x_circle_color, x_text, hp, level)
                    all_sprites.add(textcol)
        cash += speed
        if cash >= 1000:
            cash = 0
            if hp != 0:
                hp -= 1
                x_text_color = random.choice((Red, Orange, Yellow, Green, Blue, Purple))
                x_circle_color = random.choice((Red, Orange, Yellow, Green, Blue, Purple, x_text_color, x_text_color, x_text_color, x_text_color, x_text_color, x_text_color))
                x_text = random.choice(("Red", "Orange", "Yellow", "Green", "Blue", "Purple"))
                all_sprites.empty()
                textcol = Text(x_text_color, x_circle_color, x_text, hp, level)
                all_sprites.add(textcol)
        if hp == 0:
            if level > cash_level:
                cash_level = level
            level = 0
            hp = 10
            speed = 10
            Menu(exit_in_menu_int, clock, screen)
        # обновление спрайтов
        all_sprites.update()
        # Отрисовка
        screen.fill(DimGrey)
        all_sprites.draw(screen)
        pygame.display.flip()
Up_Window(exit_in_menu_int)