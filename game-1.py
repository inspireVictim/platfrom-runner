import pygame
import random

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("game-1")
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
fon = pygame.image.load('images/bg.png')

background = pygame.image.load('images/ground.jpg')
walk_right = [
    pygame.image.load('images/move_character/right/1.png'),
    pygame.image.load('images/move_character/right/2.png'),
    pygame.image.load('images/move_character/right/3.png'),
    pygame.image.load('images/move_character/right/4.png'),
]

walk_left = [
    pygame.image.load('images/move_character/left/1.png'),
    pygame.image.load('images/move_character/left/2.png'),
    pygame.image.load('images/move_character/left/3.png'),
    pygame.image.load('images/move_character/left/4.png'),
]

jump_anim = [
    pygame.image.load('images/move_character/jump/1.png'),
    pygame.image.load('images/move_character/jump/1.png')
]

player_anim_count = 0
bg_x = 0
bg_music = pygame.mixer.Sound('sounds/background.mp3')
walking_sound = pygame.mixer.Sound('sounds/walk.mp3')
coin_sound = pygame.mixer.Sound('sounds/collect.mp3')  # Звук при сборе монеты
sound_lvl = 3
bg_sound_lvl = 0.05
walking_sound.set_volume(sound_lvl)
bg_music.play()
player_y = 265
is_jumping = False
jump_count = 8

last_direction = "right"
is_walking = False  # Флаг, чтобы отслеживать проигрывание звука

hitbox = pygame.Surface((40, 50))

bg_music.set_volume(bg_sound_lvl)

# Добавление класса Coin
class Coin:
    def __init__(self, x, y):
        self.image = pygame.image.load('images/bonus.jpg')
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def move(self, speed, direction):
        # Монеты двигаются в противоположном направлении от фона
        if direction == "right":
            self.rect.x -= speed
        elif direction == "left":
            self.rect.x += speed

# Генерация монет
coins = [Coin(random.randint(850, 1200), random.randint(200, 280)) for _ in range(5)]
score = 0
font = pygame.font.Font(None, 36)  # Шрифт для счёта

bg_music.set_volume(bg_sound_lvl)

running = True
while running:

    screen.blit(fon, (0, 0))

    screen.blit(background, (bg_x, 310))
    screen.blit(background, (bg_x + 800, 310))
    screen.blit(background, (bg_x - 800, 310))

    keys = pygame.key.get_pressed()
    moving = False

    screen.blit(hitbox, (380, player_y))

    # Отображение монет и их движения
    for coin in coins[:]:  # Перебираем копию списка монет (чтобы безопасно удалять)
        coin.move(2, last_direction)  # Двигаем монету в противоположном направлении от фона
        coin.draw(screen)

        # Проверка на столкновение с персонажем
        if coin.rect.colliderect(pygame.Rect(380, player_y, 40, 50)):
            coins.remove(coin)  # Удаляем монету
            score += 1  # Увеличиваем счёт
            coin_sound.play()  # Проигрываем звук при сборе монеты

    # Отображение счёта
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # Движение вправо
        bg_x -= 2
        if bg_x <= -618:
            bg_x = 0
        screen.blit(walk_right[player_anim_count], (380, player_y))
        last_direction = "right"
        moving = True

    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:  # Движение влево
        bg_x += 2
        if bg_x >= 618:
            bg_x = 0
        screen.blit(walk_left[player_anim_count], (380, player_y))
        last_direction = "left"
        moving = True

    # Проигрываем звук, если началось движение
    if moving:
        if not is_walking:  # Если звук ещё не играет
            walking_sound.play(-1)  # -1 означает "играть в бесконечном цикле"
            is_walking = True
        player_anim_count += 1
        if player_anim_count >= len(walk_right):
            player_anim_count = 0
    else:
        if is_walking:  #выключаем звук
            walking_sound.stop()
            is_walking = False

        # Отображаем персонажа в покое
        if last_direction == "right":
            screen.blit(walk_right[0], (380, player_y))
        else:
            screen.blit(walk_left[0], (380, player_y))

    if not is_jumping:  # Если не в прыжке, проверяем нажатие пробела
        if keys[pygame.K_SPACE]:
            is_jumping = True
    else:  # Если персонаж в прыжке
        if jump_count >= -8:
            player_y -= (jump_count * abs(jump_count)) * 0.5  # Эффект параболы
            jump_count -= 1
        else:  # Завершаем прыжок
            jump_count = 8
            is_jumping = False

    pygame.display.update()

    for event in pygame.event.get():        #Закрытие игры
        if event.type == pygame.QUIT:
            running = False

    clock.tick(10)

pygame.quit()
