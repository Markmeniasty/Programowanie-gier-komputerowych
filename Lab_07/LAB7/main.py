import pyray as rl
import random
import config
from ship import Ship
from asteroid import Asteroid
from bullet import Bullet
from explosion import Explosion
from utils import check_collision_circles


def main():
    # --- INICJALIZACJA SYSTEMÓW ---
    rl.init_window(config.SCREEN_W, config.SCREEN_H, "Lab 07: Asteroids - Combat & Resources")
    rl.init_audio_device()
    rl.set_target_fps(60)

    # --- ŁADOWANIE ZASOBÓW (Zadanie 3 i 4) ---
    # Tekstura tła
    texture_stars = rl.load_texture("assets/stars.png")

    # Dźwięki
    sfx_shoot = rl.load_sound("assets/shoot.wav")
    sfx_explode = rl.load_sound("assets/explode.wav")

    # --- INICJALIZACJA OBIEKTÓW ---
    player = Ship(config.SCREEN_W // 2, config.SCREEN_H // 2)
    bullets = []
    explosions = []
    asteroids = []

    # Generowanie dużej liczby asteroid na start
    for _ in range(12):
        asteroids.append(Asteroid(
            random.randint(0, config.SCREEN_W),
            random.randint(0, config.SCREEN_H),
            random.choice(["LARGE", "MEDIUM"])
        ))

    # --- PĘTLA GŁÓWNA ---
    while not rl.window_should_close():
        dt = rl.get_frame_time()

        # 1. OBSŁUGA WEJŚCIA (Strzelanie - Zadanie 2 & **)
        if rl.is_key_pressed(rl.KeyboardKey.KEY_SPACE):
            if len(bullets) < config.BULLET_LIMIT:
                # Tworzymy pocisk i odtwarzamy dźwięk
                bullets.append(Bullet(player.pos.x, player.pos.y, player.angle))
                rl.play_sound(sfx_shoot)

        # 2. AKTUALIZACJA LOGIKI (Update)
        player.update(dt)

        for b in bullets: b.update(dt)
        for a in asteroids: a.update(dt)
        for e in explosions: e.update(dt)

        # 3. DETEKCJA KOLIZJI (Zadanie 5)
        new_asteroids = []
        for b in bullets:
            for a in asteroids:
                if a.alive and b.alive:
                    if check_collision_circles(b.pos, b.radius, a.pos, a.radius):
                        # Trafienie: dezaktywacja obiektów
                        b.alive = False
                        a.alive = False

                        # Efekty: dźwięk i animacja eksplozji
                        rl.play_sound(sfx_explode)
                        explosions.append(Explosion(a.pos.x, a.pos.y))

                        # LOGIKA ROZPADANIA (Zwiększanie gęstości gry)
                        if a.size_key == "LARGE":
                            new_asteroids.append(Asteroid(a.pos.x, a.pos.y, "MEDIUM"))
                            new_asteroids.append(Asteroid(a.pos.x, a.pos.y, "MEDIUM"))
                        elif a.size_key == "MEDIUM":
                            new_asteroids.append(Asteroid(a.pos.x, a.pos.y, "SMALL"))
                            new_asteroids.append(Asteroid(a.pos.x, a.pos.y, "SMALL"))

        # Dodanie nowych odłamków do głównej listy
        asteroids.extend(new_asteroids)

        # Zadanie *: Kolizja Statek - Asteroida
        for a in asteroids:
            if a.alive and check_collision_circles(player.pos, player.radius, a.pos, a.radius):
                rl.play_sound(sfx_explode)
                explosions.append(Explosion(player.pos.x, player.pos.y))
                # Reset statku na środek ekranu
                player.pos = rl.Vector2(config.SCREEN_W // 2, config.SCREEN_H // 2)
                player.vel = rl.Vector2(0, 0)

        # 4. CZYSZCZENIE LIST (List Comprehension - Zadanie 2)
        bullets = [b for b in bullets if b.alive]
        asteroids = [a for a in asteroids if a.alive]
        explosions = [e for e in explosions if e.alive]

        # 5. REGENERACJA (Utrzymywanie poziomu trudności)
        if len(asteroids) < 8:
            asteroids.append(Asteroid(
                random.randint(0, config.SCREEN_W),
                random.randint(0, config.SCREEN_H),
                "LARGE"
            ))

        # 6. RENDEROWANIE (Kolejność warstw!)
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        # Rysowanie tła (musi być pierwsze!)
        rl.draw_texture_pro(
            texture_stars,
            rl.Rectangle(0, 0, texture_stars.width, texture_stars.height),
            rl.Rectangle(0, 0, config.SCREEN_W, config.SCREEN_H),
            rl.Vector2(0, 0), 0, rl.WHITE
        )

        # Rysowanie obiektów gry
        for a in asteroids: a.draw()
        for b in bullets: b.draw()
        for e in explosions: e.draw()
        player.draw()

        # Interfejs użytkownika (UI)
        rl.draw_text(f"ASTEROIDS: {len(asteroids)}", 10, 10, 20, rl.GREEN)
        rl.draw_text(f"BULLETS: {len(bullets)}/{config.BULLET_LIMIT}", 10, 35, 20, rl.YELLOW)
        rl.draw_text("SPACE: Shoot | ARROWS: Move | Z: Brake", 10, config.SCREEN_H - 30, 15, rl.GRAY)

        rl.end_drawing()

    # --- ZWALNIANIE ZASOBÓW (Cleanup) ---
    rl.unload_texture(texture_stars)
    rl.unload_sound(sfx_shoot)
    rl.unload_sound(sfx_explode)
    rl.close_audio_device()
    rl.close_window()


if __name__ == "__main__":
    main()