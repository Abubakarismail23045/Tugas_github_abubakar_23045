import pygame
import sys
import random

pygame.init()

# ============= SETUP LAYAR =============
lebar_layar = 800
tinggi_layar = 600
layar = pygame.display.set_mode((lebar_layar, tinggi_layar))
pygame.display.set_caption("Harimau Makan Game")

clock = pygame.time.Clock()

# ============= LOAD GAMBAR HARIMAU =============
try:
    gambar_pemain = pygame.image.load('harimau-remove.png').convert_alpha()
    gambar_pemain = pygame.transform.scale(gambar_pemain, (150, 150))
except:
    print("Gambar harimau tidak ditemukan!")
    sys.exit()

# ============= LOAD BACKGROUND =============
try:
    gambar_bg_seram = pygame.image.load('bgseram.jpeg').convert()
    gambar_bg_seram = pygame.transform.scale(gambar_bg_seram, (lebar_layar, tinggi_layar))
except:
    print("Background tidak ditemukan!")
    sys.exit()

# ============= LOAD MAKANAN =============
try:
    gambar_makan = pygame.image.load('makanan-removebg.png').convert_alpha()
    gambar_makan = pygame.transform.scale(gambar_makan, (80, 80))
except:
    print("Gambar makanan tidak ditemukan!")
    sys.exit()

# Posisi awal harimau
lebar_gambar = gambar_pemain.get_width()
tinggi_gambar = gambar_pemain.get_height()

posisi_x = (lebar_layar - lebar_gambar) / 2
posisi_y = tinggi_layar - tinggi_gambar - 10

# Variabel gerakan
kecepatan_x = 0
kecepatan_y = 0
gravitasi = 0.8
sedang_melompat = False

dragging = False

# ============================================
#  VARIABEL MAKANAN BERGERAK
# ============================================
makan_x = random.randint(850, 1200)
makan_y = random.randint(0, tinggi_layar - 80)
makan_speed = 4
makan_muncul = True

# ============================================
#  LOOP GAME UTAMA
# ============================================
while True:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # DRAG & DROP
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if posisi_x <= mx <= posisi_x + lebar_gambar and posisi_y <= my <= posisi_y + tinggi_gambar:
                    dragging = True
                    offset_x = mx - posisi_x
                    offset_y = my - posisi_y
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        if event.type == pygame.MOUSEMOTION and dragging:
            mx, my = pygame.mouse.get_pos()
            posisi_x = mx - offset_x
            posisi_y = my - offset_y

    # ============================
    #   KONTROL KEYBOARD
    # ============================
    tombol = pygame.key.get_pressed()

    # Gerak kiri kanan
    if tombol[pygame.K_LEFT]:
        kecepatan_x = -5
    elif tombol[pygame.K_RIGHT]:
        kecepatan_x = 5
    else:
        kecepatan_x = 0

    # PGUP = naik
    if tombol[pygame.K_PAGEUP]:
        posisi_y -= 6

    # PGDN = turun
    if tombol[pygame.K_PAGEDOWN]:
        posisi_y += 6

    # LOMPAT
    if (tombol[pygame.K_UP] or tombol[pygame.K_SPACE]) and not sedang_melompat:
        sedang_melompat = True
        kecepatan_y = -15

    # ============= GERAK FISIKA =============
    posisi_x += kecepatan_x

    if sedang_melompat:
        posisi_y += kecepatan_y
        kecepatan_y += gravitasi

        if posisi_y + tinggi_gambar >= tinggi_layar:
            posisi_y = tinggi_layar - tinggi_gambar
            sedang_melompat = False
            kecepatan_y = 0

    # Batas layar
    posisi_x = max(0, min(posisi_x, lebar_layar - lebar_gambar))
    posisi_y = max(0, min(posisi_y, tinggi_layar - tinggi_gambar))

    # =====================================
    #     GERAKKAN MAKANAN
    # =====================================
    if makan_muncul:
        makan_x -= makan_speed

    if makan_x < -100:
        makan_x = random.randint(850, 1200)
        makan_y = random.randint(0, tinggi_layar - 80)
        makan_speed = random.randint(3, 6)
        makan_muncul = True

    # =====================================
    #  AREA MULUT HARIMAU
    # =====================================
    mulut_rect = pygame.Rect(
        posisi_x + lebar_gambar * 0.55,
        posisi_y + tinggi_gambar * 0.55,
        40,
        40
    )

    makan_rect = pygame.Rect(makan_x, makan_y, 80, 80)

    # =====================================
    #   CEK MAKAN
    # =====================================
    if makan_muncul and mulut_rect.colliderect(makan_rect):
        print("Harimau makan daging!")
        makan_muncul = False

        makan_x = random.randint(850, 1200)
        makan_y = random.randint(0, tinggi_layar - 80)
        makan_speed = random.randint(3, 6)
        makan_muncul = True

    # =====================================
    #     GAMBAR KE LAYAR
    # =====================================
    layar.blit(gambar_bg_seram, (0, 0))
    layar.blit(gambar_pemain, (posisi_x, posisi_y))

    if makan_muncul:
        layar.blit(gambar_makan, (makan_x, makan_y))

    pygame.display.flip()
