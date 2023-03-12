import pygame
import random
from os import listdir
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()
FPS = pygame.time.Clock()
pygame.display.set_caption('БандероГусь')

screen = width, height = 1200, 600

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
font = pygame.font.SysFont('verdana', 30)

main_surface = pygame.display.set_mode(screen)
IMGS_PATH = 'Бандерогусак для анімації (goose)'
ball_img = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]

ball = ball_img[0]
ball_rect = ball.get_rect()
ball_speed = 5


def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), [150, 30])
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(3, 6)
    return [enemy, enemy_rect, enemy_speed]


def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), [100, 100])
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonus_speed = random.randint(2, 5)
    return [bonus, bonus_rect, bonus_speed]


bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgx = 0
bgx2 = bg.get_width()
bg_speed = 3

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 2500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3500)
CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

img_index = 0
score = 0
enemyes = []
bonuses = []

is_working = True
while is_working:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY:
            enemyes.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(ball_img):
                img_index = 0
            ball = ball_img[img_index]

    pressed_keys = pygame.key.get_pressed()

    # main_surface.fill(BLACK)
    # main_surface.blit(bg, [0, 0])
    bgx -= bg_speed
    bgx2 -= bg_speed
    if bgx < -bg.get_width():
        bgx = bg.get_width()
    if bgx2 < -bg.get_width():
        bgx2 = bg.get_width()
    main_surface.blit(bg, (bgx, 0))
    main_surface.blit(bg, (bgx2, 0))
    main_surface.blit(ball, ball_rect)
    main_surface.blit(font.render(str(score), True, BLACK), (width - 30, 0))
    for enemy in enemyes:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])
        if enemy[1].right < 0:
            enemyes.pop(enemyes.index(enemy))
        if enemy[1].bottom > height or enemy[1].top < 0:
            enemyes.pop(enemyes.index(enemy))
        if ball_rect.colliderect(enemy[1]):
            is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        if bonus[1].bottom > height:
            bonuses.pop(bonuses.index(bonus))
        if bonus[1].left < 0 or bonus[1].right > width:
            bonuses.pop(bonuses.index(bonus))
        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1

    if pressed_keys[K_DOWN] and not ball_rect.bottom >= height:
        ball_rect = ball_rect.move(0, ball_speed)
    if pressed_keys[K_UP] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move(0, -ball_speed)
    if pressed_keys[K_RIGHT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed, 0)
    if pressed_keys[K_LEFT] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move(-ball_speed, 0)

    pygame.display.flip()
