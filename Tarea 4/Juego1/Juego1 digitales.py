import pygame
import random
import os
import time

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Evasión con Niveles")
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

# Jugador
player_x = 400
player_y = 500
player_speed = 5

# Enemigos
enemies = []
enemy_speed = 3

# Puntuación y niveles
score = 0
level = 1
goal = 30 # enemigos esquivados para subir de nivel

# Reiniciar nivel
def reset_level(new_level=False):
    global enemies, player_x, player_y
    enemies = []
    player_x, player_y = 400, 500
    if new_level:
        pass  # aquí podrías aumentar variedad si quieres

# Mostrar mensaje de nivel
def show_level_message(lvl):
    screen.fill(WHITE)
    text = big_font.render(f"¡Nivel {lvl}!", True, BLACK)
    screen.blit(text, (280, 250))
    pygame.display.update()
    pygame.time.delay(2000)

# Mostrar mensaje de derrota
def show_game_over(msg="¡Perdiste!"):
    screen.fill(WHITE)
    text = big_font.render(msg, True, RED)
    screen.blit(text, (250, 250))
    pygame.display.update()
    pygame.time.delay(3000)

# Bucle principal
running = True
reset_level(new_level=True)

while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 800 - player_size:
        player_x += player_speed
        
    # Generar enemigos
    if random.randint(1, 20) == 1:
        enemies.append([random.randint(0, 800 - enemy_size), 0])
        
    # Mover y dibujar enemigos
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > 600:
            enemies.remove(enemy)
            score += 1  # Contar bloque esquivado
            
            # Subir nivel
            if score % goal == 0:
                level += 1
                show_level_message(level)
                enemy_speed += 1  # Aumentar dificultad
                reset_level(new_level=True)
                
        else:
            screen.blit(enemy_img, (enemy[0], enemy[1]))
            
        # Detectar colisiones usando rectángulos invisibles
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(enemy_rect):
            show_game_over()
            running = False
            break
    
    # Dibujar jugador
    screen.blit(player_img, (player_x, player_y))
    
    # Mostrar score y nivel
    score_text = font.render(f"Esquivados: {score}", True, BLACK)
    level_text = font.render(f"Nivel: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()

