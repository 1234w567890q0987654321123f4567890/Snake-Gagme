import pygame # type: ignore
import time
import random

# Ekran boyutları
WIDTH = 600
HEIGHT = 400

# Renkler
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 102)

# Yılan boyutu ve başlangıç hızı
BLOCK_SIZE = 10
INITIAL_SPEED = 5

# Pygame başlatma
pygame.init()

# Ekran ve fontlar
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Yılan Oyunu')
clock = pygame.time.Clock()

font = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Arka plan resmi yükle
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Yılanın çizilmesi
def draw_snake(block_size, snake_list):
    for i, block in enumerate(snake_list):
        color = GREEN if i % 2 == 0 else (0, 255, 255)  # Alternatif renk
        pygame.draw.rect(display, color, [block[0], block[1], block_size, block_size])

# Skorun gösterilmesi
def show_score(score):
    value = score_font.render("Skor: " + str(score), True, YELLOW)
    display.blit(value, [10, 10])

# Başlangıç ekranı
def show_start_screen():
    display.fill(BLUE)
    show_message("Yılan Oyunu - Başlamak için Enter'a basın", WHITE, WIDTH / 2, HEIGHT / 2)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# Mesaj gösterme
def show_message(msg, color, x, y):
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    display.blit(text, text_rect)

# Yiyecek üretme
def generate_food():
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
    return food_x, food_y

# Engeller üretme (her yemek yediğinde yer değiştirecek)
def generate_obstacles():
    obstacles = []
    for _ in range(5):  # 5 adet engel
        x = random.randint(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE
        obstacles.append((x, y))
    return obstacles

def draw_obstacles(obstacles):
    for x, y in obstacles:
        pygame.draw.rect(display, BLACK, [x, y, BLOCK_SIZE, BLOCK_SIZE])

# En yüksek skor kaydetme
def save_high_score(score):
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
        if score > high_score:
            with open("high_score.txt", "w") as file:
                file.write(str(score))
    except FileNotFoundError:
        with open("high_score.txt", "w") as file:
            file.write(str(score))

# Oyun döngüsü
def game_loop():
    game_over = False
    game_close = False
    paused = False  # Duraklatma durumu
    x = WIDTH / 2
    y = HEIGHT / 2
    x_change = 0
    y_change = 0
    snake_list = []
    snake_length = 1
    speed = INITIAL_SPEED
    food_x, food_y = generate_food()
    obstacles = generate_obstacles()  # Başlangıçta engeller oluşturulur
    
    while not game_over:
        while game_close:
            display.fill(WHITE)
            display.blit(background, (0, 0))
            show_message("Kaybettin! Q ile tekrar oyna, C ile çık.", RED, WIDTH / 2, HEIGHT / 2)
            show_score(snake_length - 1)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_loop()
                    if event.key == pygame.K_c:
                        game_over = True
                        game_close = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:  # Sol yön, sağa gitmiyorsa
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:  # Sağ yön, sola gitmiyorsa
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:  # Yukarı yön, aşağıya gitmiyorsa
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:  # Aşağı yön, yukarı gitmiyorsa
                    y_change = BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_p:  # Duraklatma işlevi
                    paused = not paused
        
        if paused:  # Oyun duraklatıldığında
            show_message("Oyun Duraklatıldı - P ile devam et", YELLOW, WIDTH / 2, HEIGHT / 2)
            pygame.display.update()
            continue
        
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0 or (x, y) in obstacles:
            game_close = True
        
        x += x_change
        y += y_change
        display.blit(background, (0, 0))
        pygame.draw.rect(display, BLUE, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        draw_obstacles(obstacles)  # Engelleri çiz
        
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)
        
        if len(snake_list) > snake_length:
            del snake_list[0]
        
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True
        
        draw_snake(BLOCK_SIZE, snake_list)
        show_score(snake_length - 1)
        pygame.display.update()
        
        if x == food_x and y == food_y:
            food_x, food_y = generate_food()  # Yiyecek yeni bir konuma gider
            snake_length += 1
            obstacles = generate_obstacles()  # Yılan her yemek yediğinde engeller yeniden yerleşir
            if (snake_length - 1) % 5 == 0:  # Her 5 puanda hız artar
                speed += 1
        
        save_high_score(snake_length - 1)  # En yüksek skoru kaydetme
        clock.tick(speed)
    
    pygame.quit()
    quit()

show_start_screen()  # Başlangıç ekranını göster
game_loop()
