[app]
# Uygulama başlığı
title = Uzay Kaçışı
# Paket adı (benzersiz olmalı)
package.name = uzaykacisi
# Paket domaini
package.domain = org.example
# Kaynak dizini (main.py ve assets burada olmalı)
source.dir = .
# Ana dosya
source.include_exts = py,png,jpg,kv,atlas,ttf,ogg,wav,mp3
# Dahil edilecek dosyalar
source.include_patterns = assets/*
# Hariç tutulacaklar
source.exclude_patterns = bin/*

# Versiyon
version = 1.0

# İzinler (Android)
android.permissions = INTERNET

# API seviyesi
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# ABI (işlemci mimarileri)
android.archs = arm64-v8a, armeabi-v7a

# SDL2 + pygame desteği
requirements = python3,pygame,SDL2,SDL2_image,SDL2_mixer,SDL2_ttf

# Oryantasyon (dikey)
orientation = portrait

# Tam ekran
fullscreen = 1

# İkon (varsa)
# icon.filename = assets/icon.png

# Presplash (başlangıç ekranı)
# presplash.filename = assets/presplash.png

[buildozer]
# Log seviyesi
log_level = 2
