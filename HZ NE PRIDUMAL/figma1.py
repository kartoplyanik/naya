import pygame
import math
import random
import os

# Ініціалізуємо Pygame
pygame.init()

# Налаштування екрану
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Rotate and Shoot towards Cursor')

font = pygame.font.Font(None, 36)

score = 0

high_score = 0

lives = 3



# Налаштування кольорів
white = (255, 255, 255)
black = (0, 0, 0)

# Завантаження зображення для персонажа
player_image_original = pygame.image.load('hero.png')  
player_image = pygame.transform.scale(player_image_original, (100, 100))
player_rect = player_image.get_rect(center=(screen_width // 2, screen_height // 2))


# Налаштування для кулі
bullet_image = pygame.Surface((10, 10))
bullet_image.fill(black)

# Список куль
bullets = []

enemies = []

speed = 0
enemy_image_original = pygame.image.load('frag1.png.png')
enemy_image = pygame.transform.scale(enemy_image_original, (75, 75))
level = 1
def create_enemy():
    side = random.randint(1,4)
    if side == 1:
        x = random.randint(0, screen_width - 50)
        y = -50

    if side == 2:
        x = screen_width + 50
        y = random.randint(0, screen_height - 50)

    if side == 3:
        x = random.randint(0, screen_width - 50)
        y = screen_height + 50

    if side == 4:  
        x = screen_width - 50
        y = random.randint(0, screen_height - 50)
    
    
    angle = math.atan2(player_rect.centery - y,player_rect.centerx - x)
    speed  = 2
    dx = math.cos(angle) * speed
    dy = math.sin(angle) * speed

    enemies.append([x, y, dx, dy])



# Основний цикл гри
running = True
clock = pygame.time.Clock()
check = True

spawner_timer = 0
spawner_delay = 60

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Ліва кнопка миші
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Обчислення напрямку пострілу
                angle = math.atan2(mouse_y - player_rect.centery, mouse_x - player_rect.centerx)
                bullet_dx = math.cos(angle) * 10
                bullet_dy = math.sin(angle) * 10
                bullets.append([player_rect.centerx, player_rect.centery, bullet_dx, bullet_dy])

    spawner_timer += 1
    if spawner_timer >= spawner_delay:
        create_enemy()
        spawner_timer = 0

    for e in enemies:
        e[0] += e[2]
        e[1] += e[3]

    enemies_remove = []
    for bullet in bullets:
        buller_rect = pygame.Rect(bullet[0], bullet[1], bullet_image.get_width(), bullet_image.get_height())
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_image.get_width(), enemy_image.get_height())
                
            if buller_rect.colliderect(enemy_rect):
                enemies_remove.append(enemy)
                bullets.remove(bullet)
                score +=  1         
                if score % 10 == 0 and check == True:
                    level += 1
                    speed += 1
                    spawner_delay -= 5
                    check = False
            
                
                if score > high_score:
                    high_score = score
 
                break
            if player_rect.colliderect(enemy_rect):
                lives -= 1
                enemies_remove.append(enemy)

    for e in enemies_remove:
        enemies.remove(e)

    if score % 11 == 0:
        check = True

    if lives <= 0:
        running = False    

    text = font.render(f"Рахунок: {score}", True, (255,0,0))
    text2 = font.render(f"Мій Рахунок: {high_score}", True, (255,0,0))
    text3 = font.render(f"Рівень: {level}", True, (255,0,0))
    text4 = font.render(f"Життя: {lives}", True, (255,0,0))

    # Отримуємо позицію курсора
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Обчислюємо кут повороту
    angle = math.degrees(math.atan2(mouse_y - player_rect.centery, mouse_x - player_rect.centerx)) - 90

    # Оновлюємо кулі
    for bullet in bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

    # Очищуємо екран
    screen.fill(white)

    # Повертаємо персонажа та малюємо його на екрані
    rotated_image = pygame.transform.rotate(player_image, -angle)
    new_rect = rotated_image.get_rect(center=player_rect.center)
    screen.blit(rotated_image, new_rect.topleft)

    # Малюємо кулі
    for bullet in bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))

    
    for e in enemies:
        screen.blit(enemy_image, (e[0], e[1]))
    screen.blit(text2,(10,50))
    screen.blit(text,(10,10))
    screen.blit(text3,(10,100))
    screen.blit(text4,(10,150))
    

    with open ("score.txt", "w") as file:
        file.write(str(high_score))

    # Оновлюємо екран
    pygame.display.flip()
    clock.tick(60)

# Закриваємо Pygame
pygame.quit()