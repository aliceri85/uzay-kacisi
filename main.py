import pygame
import random
import sys
import os

pygame.init()

# ===== TAM EKRAN AYARLARI =====
# Bilgisayarda pencere modunda başlat, F11 ile tam ekran geçişi
# Android'de otomatik tam ekran olur
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Oyun alanı oranını koru (dikey telefon formatı)
GAME_WIDTH = 480
GAME_HEIGHT = 800

# Ekranı ortala
offset_x = (SCREEN_WIDTH - GAME_WIDTH) // 2
offset_y = (SCREEN_HEIGHT - GAME_HEIGHT) // 2

# Android kontrolü
IS_ANDROID = hasattr(sys, 'getandroidapilevel')

if IS_ANDROID:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    # Bilgisayarda pencere modu (F11 ile tam ekran)
    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)
    SCREEN_WIDTH = GAME_WIDTH
    SCREEN_HEIGHT = GAME_HEIGHT
    offset_x = 0
    offset_y = 0

pygame.display.set_caption("Uzay Kaçışı")
clock = pygame.time.Clock()

# ===== GÖRSEL YÜKLEME =====
def load_image(name, size=None):
    """Görsel yükle, boyutlandır, hata durumunda None döndür"""
    try:
        # Önce assets klasörüne bak
        paths = [
            os.path.join("assets", name),
            os.path.join(os.path.dirname(__file__), "assets", name),
            name
        ]
        for path in paths:
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
                if size:
                    img = pygame.transform.smoothscale(img, size)
                return img
        print(f"UYARI: {name} bulunamadı!")
        return None
    except Exception as e:
        print(f"Görsel hatası ({name}): {e}")
        return None

# Görselleri yükle
player_size = 60
enemy_size = 50

player_img = load_image("player.png", (player_size, player_size))
enemy_img = load_image("enemy.png", (enemy_size, enemy_size))
bg_img = load_image("background.png", (GAME_WIDTH, GAME_HEIGHT))

# Yedek renkler (görsel yoksa)
BLUE = (0, 100, 255)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)
DARK_BG = (15, 15, 35)

# Font
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 56)
small_font = pygame.font.SysFont(None, 28)

# ===== OYUN DEĞİŞKENLERİ =====
player_x = GAME_WIDTH // 2 - player_size // 2
player_y = GAME_HEIGHT - 120
player_speed = 8

enemy_speed = 6
enemies = []
particles = []

# Oyun durumu: START -> PLAY -> GAMEOVER
game_state = "START"
score = 0
high_score = 0
fullscreen = False

def create_enemy():
    x = random.randint(10, GAME_WIDTH - enemy_size - 10)
    return {"rect": pygame.Rect(x, -enemy_size, enemy_size, enemy_size), 
            "rot": random.randint(0, 360),
            "rot_speed": random.choice([-3, -2, -1, 1, 2, 3])}

def create_particle(x, y, color):
    return {"x": x, "y": y, 
            "vx": random.uniform(-3, 3), 
            "vy": random.uniform(-3, 3),
            "life": 30,
            "color": color,
            "size": random.randint(3, 7)}

def reset_game():
    global enemies, score, player_x, particles
    enemies = []
    particles = []
    score = 0
    player_x = GAME_WIDTH // 2 - player_size // 2

def draw_center(text, font_obj, color, y, surface=None):
    if surface is None:
        surface = game_surface
    img = font_obj.render(text, True, color)
    surface.blit(img, (GAME_WIDTH//2 - img.get_width()//2, y))

def draw_text(text, font_obj, color, x, y, surface=None):
    if surface is None:
        surface = game_surface
    img = font_obj.render(text, True, color)
    surface.blit(img, (x, y))

# ===== ANA DÖNGÜ =====
running = True
while running:
    dt = clock.tick(60) / 1000.0  # Delta time

    # Oyun yüzeyi (sabit çözünürlük)
    game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

    # Arka plan
    if bg_img:
        game_surface.blit(bg_img, (0, 0))
    else:
        game_surface.fill(DARK_BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)
                info = pygame.display.Info()
                SCREEN_WIDTH = info.current_w
                SCREEN_HEIGHT = info.current_h
                offset_x = (SCREEN_WIDTH - GAME_WIDTH) // 2
                offset_y = (SCREEN_HEIGHT - GAME_HEIGHT) // 2

            if event.key == pygame.K_ESCAPE and fullscreen:
                fullscreen = False
                screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)
                SCREEN_WIDTH = GAME_WIDTH
                SCREEN_HEIGHT = GAME_HEIGHT
                offset_x = 0
                offset_y = 0

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
            if game_state == "START":
                reset_game()
                game_state = "PLAY"
            elif game_state == "GAMEOVER":
                game_state = "START"

    if game_state == "START":
        # Başlangıç ekranı
        draw_center("UZAY KAÇIŞI", big_font, WHITE, 250)
        draw_center("Başlamak için dokun", font, (200, 200, 200), 330)
        draw_center("veya tıkla", small_font, (150, 150, 150), 370)
        draw_center("F11: Tam Ekran | ESC: Çıkış", small_font, (100, 100, 100), 450)

        # Oyuncu önizlemesi
        if player_img:
            game_surface.blit(player_img, (GAME_WIDTH//2 - player_size//2, 160))
        else:
            pygame.draw.rect(game_surface, BLUE, 
                           (GAME_WIDTH//2 - player_size//2, 160, player_size, player_size))

    elif game_state == "PLAY":
        # ===== HAREKET =====
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < GAME_WIDTH - player_size:
            player_x += player_speed

        # Mobil/Mouse dokunma
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            # Ekran koordinatlarını oyun koordinatlarına çevir
            if fullscreen or IS_ANDROID:
                mx = (mx - offset_x) * GAME_WIDTH // SCREEN_WIDTH
            else:
                mx = mx

            if mx < GAME_WIDTH // 2:
                player_x -= player_speed
            else:
                player_x += player_speed

        # Sınırları kontrol et
        player_x = max(0, min(player_x, GAME_WIDTH - player_size))

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

        # Oyuncu çiz
        if player_img:
            game_surface.blit(player_img, (player_x, player_y))
        else:
            pygame.draw.rect(game_surface, BLUE, player_rect, border_radius=8)

        # Motor parçacıkları
        if random.random() < 0.5:
            particles.append(create_particle(
                player_x + player_size//2, 
                player_y + player_size,
                random.choice([(100, 150, 255), (50, 100, 255), (200, 220, 255)])
            ))

        # ===== DÜŞMANLAR =====
        if random.randint(1, 35) == 1:
            enemies.append(create_enemy())

        for enemy in enemies[:]:
            enemy["rect"].y += enemy_speed
            enemy["rot"] += enemy["rot_speed"]

            # Düşman çiz (döndürülmüş)
            if enemy_img:
                rotated = pygame.transform.rotate(enemy_img, enemy["rot"])
                rect = rotated.get_rect(center=enemy["rect"].center)
                game_surface.blit(rotated, rect)
            else:
                pygame.draw.rect(game_surface, RED, enemy["rect"], border_radius=5)

            # Çarpışma
            if enemy["rect"].colliderect(player_rect):
                # Patlama efekti
                for _ in range(20):
                    particles.append(create_particle(
                        player_x + player_size//2,
                        player_y + player_size//2,
                        random.choice([RED, (255, 100, 0), (255, 200, 0), WHITE])
                    ))
                game_state = "GAMEOVER"
                if score > high_score:
                    high_score = score

            # Ekran dışına çıktı
            if enemy["rect"].y > GAME_HEIGHT:
                enemies.remove(enemy)
                score += 1
                # Skor arttıkça zorlaş
                if score % 10 == 0:
                    enemy_speed = min(enemy_speed + 0.3, 15)

        # Skor
        draw_text(f"Skor: {score}", font, WHITE, 15, 15)
        draw_text(f"Rekor: {high_score}", small_font, (180, 180, 180), 15, 50)

    elif game_state == "GAMEOVER":
        # Karanlık overlay
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        game_surface.blit(overlay, (0, 0))

        draw_center("GAME OVER", big_font, RED, 260)
        draw_center(f"Skor: {score}", font, WHITE, 330)
        if score >= high_score and score > 0:
            draw_center("YENİ REKOR!", font, (255, 215, 0), 370)
        draw_center("Tekrar için dokun", font, (200, 200, 200), 430)

    # ===== PARÇACIKLAR =====
    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["life"] -= 1
        p["size"] = max(1, p["size"] - 0.1)
        if p["life"] <= 0:
            particles.remove(p)
        else:
            alpha = min(255, p["life"] * 8)
            color = p["color"]
            pygame.draw.circle(game_surface, color, (int(p["x"]), int(p["y"])), int(p["size"]))

    # ===== EKRANA ÇİZ =====
    # Oyun yüzeyini gerçek ekrana ölçekle
    if fullscreen or IS_ANDROID:
        # Siyah kenarlıklar
        screen.fill(BLACK)
        scaled = pygame.transform.smoothscale(game_surface, 
            (SCREEN_WIDTH if IS_ANDROID else min(SCREEN_WIDTH, int(SCREEN_HEIGHT * GAME_WIDTH/GAME_HEIGHT)),
             SCREEN_HEIGHT if IS_ANDROID else min(SCREEN_HEIGHT, int(SCREEN_WIDTH * GAME_HEIGHT/GAME_WIDTH))))

        if IS_ANDROID:
            screen.blit(scaled, (0, 0))
        else:
            rect = scaled.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(scaled, rect)
    else:
        screen.blit(game_surface, (0, 0))

    pygame.display.update()

pygame.quit()
sys.exit()
