import pygame
import random
import os
import time

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Evasión con Niveles y Vidas")
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fuente
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# Ruta absoluta a la carpeta del script
base_path = os.path.dirname(__file__)

# ====== Cargar imágenes ======
player_size = 50
player_img = pygame.image.load(os.path.join(base_path, "player.png"))
player_img = pygame.transform.scale(player_img, (player_size, player_size))

enemy_size = 40
enemy_img = pygame.image.load(os.path.join(base_path, "enemy.png"))
enemy_img = pygame.transform.scale(enemy_img, (enemy_size, enemy_size))

bullet_size = 10
bullet_img = pygame.Surface((bullet_size, bullet_size))
bullet_img.fill(BLACK)

# Jugador
player_x = 400
player_y = 500
player_speed = 5

# Balas
bullets = []
bullet_speed = 7

# Enemigos
enemies = []
enemy_speed = 3
enemy_spawn_rate = 3  # enemigos por segundo
last_enemy_spawn_time = 0

# Puntuación, niveles y vidas
score = 0
level = 1
goal = 10  # enemigos destruidos para subir de nivel
lives = 3

# Reiniciar nivel
def reset_level(new_level=False):
    global enemies, bullets, player_x, player_y
    enemies = []
    bullets = []
    player_x, player_y = 400, 500
    if new_level:
        pass

# Mostrar mensaje de nivel
def show_level_message(lvl):
    screen.fill(WHITE)
    text = big_font.render(f"¡Nivel {lvl}!", True, BLACK)
    screen.blit(text, (280, 250))
    pygame.display.update()
    pygame.time.delay(2000)

# Mostrar mensaje de derrota
def show_game_over():
    screen.fill(WHITE)
    text = big_font.render("¡Perdiste!", True, RED)
    text2 = font.render("Te quedaste sin vidas", True, RED)
    screen.blit(text, (250, 220))
    screen.blit(text2, (260, 300))
    pygame.display.update()
    pygame.time.delay(3000)

# Bucle principal
running = True
reset_level(new_level=True)

while running:
    screen.fill(WHITE)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Disparar bala
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x + player_size // 2 - bullet_size // 2, player_y])

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 800 - player_size:
        player_x += player_speed

    # Generar enemigos (3 por segundo)
    if current_time - last_enemy_spawn_time > 1000 // enemy_spawn_rate:
        enemies.append([random.randint(0, 800 - enemy_size), 0])
        last_enemy_spawn_time = current_time

    # Mover y dibujar balas
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)
        else:
            screen.blit(bullet_img, (bullet[0], bullet[1]))

    # Mover y dibujar enemigos
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > 600:
            enemies.remove(enemy)
        else:
            screen.blit(enemy_img, (enemy[0], enemy[1]))

        # Detectar colisión con jugador
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(enemy_rect):
            enemies.remove(enemy)
            lives -= 1
            if lives <= 0:
                show_game_over()
                running = False
                break

        # Detectar colisión con balas
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_size, bullet_size)
            if bullet_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1

                # Subir de nivel cada 10 enemigos destruidos
                if score % goal == 0:
                    level += 1
                    show_level_message(level)
                    enemy_speed += 1
                    reset_level(new_level=True)
                break

    # Dibujar jugador
    screen.blit(player_img, (player_x, player_y))

    # Mostrar score, nivel y vidas
    score_text = font.render(f"Puntos: {score}", True, BLACK)
    level_text = font.render(f"Nivel: {level}", True, BLACK)
    lives_text = font.render(f"Vidas: {lives}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))
    screen.blit(lives_text, (10, 90))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
