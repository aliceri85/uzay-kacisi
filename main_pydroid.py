import pygame
import random
import sys
import os

pygame.init()

# Pydroid 3 uyumlu: Ekran boyutunu otomatik al
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Uzay Kaçışı")
clock = pygame.time.Clock()

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (200, 0, 0)
GRAY = (230, 230, 230)
DARK_BG = (15, 15, 35)

# Font
font = pygame.font.SysFont(None, 48)
big_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 32)

# ===== GÖRSEL YÜKLEME =====
def load_image(name, size=None):
    try:
        # Pydroid 3: dosya yolunu bul
        paths = [
            os.path.join(os.path.dirname(__file__), "assets", name),
            os.path.join("assets", name),
            name
        ]
        for path in paths:
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                if size:
                    img = pygame.transform.smoothscale(img, size)
                return img
        return None
    except:
        return None

# Görselleri yükle
player_size = int(WIDTH * 0.15)
enemy_size = int(WIDTH * 0.12)

player_img = load_image("player.png", (player_size, player_size))
enemy_img = load_image("enemy.png", (enemy_size, enemy_size))
bg_img = load_image("background.png", (WIDTH, HEIGHT))

# Oyuncu
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - int(HEIGHT * 0.18)
player_speed = int(WIDTH * 0.025)

# Engel
enemy_speed = int(HEIGHT * 0.012)
enemies = []
particles = []

def create_enemy():
    x = random.randint(10, WIDTH - enemy_size - 10)
    return {"rect": pygame.Rect(x, -enemy_size, enemy_size, enemy_size),
            "rot": random.randint(0, 360),
            "rot_speed": random.choice([-3, -2, -1, 1, 2, 3])}

def create_particle(x, y, color):
    return {"x": x, "y": y,
            "vx": random.uniform(-4, 4),
            "vy": random.uniform(-4, 4),
            "life": 30,
            "color": color,
            "size": random.randint(3, 8)}

# Oyun durumu
game_state = "START"
score = 0
high_score = 0

def reset_game():
    global enemies, score, player_x, particles
    enemies = []
    particles = []
    score = 0
    player_x = WIDTH // 2 - player_size // 2

def draw_center(text, font_obj, color, y):
    img = font_obj.render(text, True, color)
    screen.blit(img, (WIDTH//2 - img.get_width()//2, y))

def draw_text(text, font_obj, color, x, y):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))

# ===== ANA DÖNGÜ =====
running = True
while running:
    dt = clock.tick(60) / 1000.0

    # Arka plan
    if bg_img:
        screen.blit(bg_img, (0, 0))
    else:
        screen.fill(DARK_BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        # DOKUNMATIK KONTROL
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
            if game_state == "START":
                reset_game()
                game_state = "PLAY"
            elif game_state == "GAMEOVER":
                game_state = "START"

    if game_state == "START":
        draw_center("UZAY KAÇIŞI", big_font, WHITE, int(HEIGHT * 0.3))
        draw_center("Başlamak için dokun", font, (200, 200, 200), int(HEIGHT * 0.42))
        draw_center("Ekranın solu: sola git", small_font, (150, 150, 150), int(HEIGHT * 0.5))
        draw_center("Ekranın sağı: sağa git", small_font, (150, 150, 150), int(HEIGHT * 0.54))

        if player_img:
            screen.blit(player_img, (WIDTH//2 - player_size//2, int(HEIGHT * 0.15)))
        else:
            pygame.draw.rect(screen, BLUE, (WIDTH//2 - player_size//2, int(HEIGHT * 0.15), player_size, player_size))

    elif game_state == "PLAY":
        # ===== HAREKET =====
        # Dokunmatik kontrol - sola/sağa dokunma
        touch_x = None
        if pygame.mouse.get_pressed()[0]:
            touch_x = pygame.mouse.get_pos()[0]

        # Ayrıca FINGER motion da kontrol et
        for event in pygame.event.get():
            if event.type == pygame.FINGERDOWN or event.type == pygame.FINGERMOTION:
                touch_x = int(event.x * WIDTH)

        if touch_x is not None:
            if touch_x < WIDTH // 2:
                player_x -= player_speed
            else:
                player_x += player_speed

        # Sınırlar
        player_x = max(0, min(player_x, WIDTH - player_size))

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

        # Oyuncu çiz
        if player_img:
            screen.blit(player_img, (player_x, player_y))
        else:
            pygame.draw.rect(screen, BLUE, player_rect, border_radius=8)

        # Motor parçacıkları
        if random.random() < 0.6:
            particles.append(create_particle(
                player_x + player_size//2,
                player_y + player_size,
                random.choice([(100, 150, 255), (50, 100, 255), (200, 220, 255)])
            ))

        # ===== DÜŞMANLAR =====
        if random.randint(1, 30) == 1:
            enemies.append(create_enemy())

        for enemy in enemies[:]:
            enemy["rect"].y += enemy_speed
            enemy["rot"] += enemy["rot_speed"]

            if enemy_img:
                rotated = pygame.transform.rotate(enemy_img, enemy["rot"])
                rect = rotated.get_rect(center=enemy["rect"].center)
                screen.blit(rotated, rect)
            else:
                pygame.draw.rect(screen, RED, enemy["rect"], border_radius=5)

            # Çarpışma
            if enemy["rect"].colliderect(player_rect):
                for _ in range(25):
                    particles.append(create_particle(
                        player_x + player_size//2,
                        player_y + player_size//2,
                        random.choice([RED, (255, 100, 0), (255, 200, 0), WHITE])
                    ))
                game_state = "GAMEOVER"
                if score > high_score:
                    high_score = score

            if enemy["rect"].y > HEIGHT:
                enemies.remove(enemy)
                score += 1
                if score % 10 == 0:
                    enemy_speed = min(enemy_speed + 1, 20)

        # Skor
        draw_text(f"Skor: {score}", font, WHITE, 20, 20)
        draw_text(f"Rekor: {high_score}", small_font, (180, 180, 180), 20, 65)

    elif game_state == "GAMEOVER":
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        draw_center("GAME OVER", big_font, RED, int(HEIGHT * 0.35))
        draw_center(f"Skor: {score}", font, WHITE, int(HEIGHT * 0.45))
        if score >= high_score and score > 0:
            draw_center("YENİ REKOR!", font, (255, 215, 0), int(HEIGHT * 0.52))
        draw_center("Tekrar için dokun", font, (200, 200, 200), int(HEIGHT * 0.6))

    # Parçacıklar
    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["life"] -= 1
        p["size"] = max(1, p["size"] - 0.15)
        if p["life"] <= 0:
            particles.remove(p)
        else:
            pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), int(p["size"]))

    pygame.display.update()

pygame.quit()
sys.exit()
