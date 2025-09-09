import pygame
import random
import os
import time

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Recolección de Gasolina")
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
player_size = 40
player_img = pygame.image.load(os.path.join(base_path, "player.png"))
player_img = pygame.transform.scale(player_img, (player_size, player_size))

item_size = 30
item_img = pygame.image.load(os.path.join(base_path, "gasolina.png"))
item_img = pygame.transform.scale(item_img, (item_size, item_size))

obstacle_size = 60
obstacle_img = pygame.image.load(os.path.join(base_path, "obstaculo.png"))
obstacle_img = pygame.transform.scale(obstacle_img, (obstacle_size, obstacle_size))

# Jugador
player_x = 400
player_y = 300
player_speed = 5

# Objetos para recolectar
items = []
last_item_time = 0  # Control de 1 objeto por segundo

# Obstáculos (cada uno con posición y velocidad)
obstacles = []

# Puntuación y niveles
score = 0
level = 1
goal = 10  # Gasolinas necesarias para pasar nivel

# Tiempo
time_limit = 30
level_start_time = time.time()

# Reiniciar nivel
def reset_level(new_level=False):
    global items, obstacles, player_x, player_y, level_start_time
    items = []
    obstacles = []
    player_x, player_y = 400, 300
    level_start_time = time.time()
    if new_level:
        for _ in range(level):  # Más obstáculos en niveles altos
            ox = random.randint(0, 800 - obstacle_size)
            oy = random.randint(0, 600 - 100 - obstacle_size)
            dx = random.choice([-3, -2, 2, 3])
            dy = random.choice([-3, -2, 2, 3])
            obstacles.append([ox, oy, dx, dy])

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
    new_x, new_y = player_x, player_y
    if keys[pygame.K_LEFT] and player_x > 0:
        new_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 800 - player_size:
        new_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        new_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < 550 - player_size:  # No pisar el texto inferior
        new_y += player_speed
    
    # Comprobar colisión con obstáculos
    for ox, oy, _, _ in obstacles:
        if (new_x < ox + obstacle_size and
            new_x + player_size > ox and
            new_y < oy + obstacle_size and
            new_y + player_size > oy):
            show_game_over()
            running = False
            break
    
    if not running:
        break
    
    # Actualizar posición del jugador
    player_x, player_y = new_x, new_y
        
    # Generar objetos (máximo 1 cada segundo)
    current_time = time.time()
    if current_time - last_item_time >= 1:
        if len(items) < 1:  # Solo 1 gasolina activa
            items.append([random.randint(0, 800 - item_size),
                          random.randint(0, 550 - item_size)])
        last_item_time = current_time
        
    # Recolectar gasolina
    for item in items[:]:
        if (player_x < item[0] + item_size and
            player_x + player_size > item[0] and
            player_y < item[1] + item_size and
            player_y + player_size > item[1]):
            items.remove(item)
            score += 1
            
            if score % goal == 0:  # Subir nivel
                level += 1
                show_level_message(level)
                reset_level(new_level=True)
                
    # Verificar tiempo
    elapsed = int(current_time - level_start_time)
    remaining_time = max(0, time_limit - elapsed)
    if remaining_time == 0:
        show_game_over("¡Se acabó el tiempo!")
        running = False
    
    # ====== Mover obstáculos ======
    for i, obs in enumerate(obstacles):
        obs[0] += obs[2]  # mover en x
        obs[1] += obs[3]  # mover en y
        
        # Rebotar en bordes
        if obs[0] <= 0 or obs[0] >= 800 - obstacle_size:
            obs[2] *= -1
        if obs[1] <= 0 or obs[1] >= 600 - 100 - obstacle_size:
            obs[3] *= -1
        
        # Comprobar colisiones entre obstáculos
        for j, other in enumerate(obstacles):
            if i != j:
                rect1 = pygame.Rect(obs[0], obs[1], obstacle_size, obstacle_size)
                rect2 = pygame.Rect(other[0], other[1], obstacle_size, obstacle_size)
                if rect1.colliderect(rect2):
                    obs[2] *= -1
                    obs[3] *= -1
                    other[2] *= -1
                    other[3] *= -1
    
    # Dibujar objetos
    for item in items:
        screen.blit(item_img, (item[0], item[1]))
        
    # Dibujar obstáculos
    for obs in obstacles:
        screen.blit(obstacle_img, (obs[0], obs[1]))
        
    # Dibujar jugador
    screen.blit(player_img, (player_x, player_y))
    
    # Mostrar puntuación, nivel y tiempo
    score_text = font.render(f"Gasolina recogida: {score}", True, BLACK)
    level_text = font.render(f"Nivel: {level}", True, BLACK)
    time_text = font.render(f"Tiempo: {remaining_time}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))
    screen.blit(time_text, (10, 90))
    
    # Texto inferior
    instruction_text = font.render("Coge la gasolina y evita los ateroides antes que se acabe el tiempo", True, BLACK)
    screen.blit(instruction_text, (0, 570))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()

