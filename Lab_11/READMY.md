# Lab 11 – System Walki, VFX i Inteligencja Przeciwników

## Co zostało zrealizowane
W ramach tego laboratorium zaimplementowałem kompletny system interakcji bojowych oraz oprawę wizualną zniszczeń. Kluczowe elementy to:

*   **Efekt rozpadu (VFX)**: Stworzyłem system cząsteczek `GPUParticles3D`, który generuje efekt eksplozji w momencie zniszczenia wroga lub celu. Wykorzystałem podejście *One Shot* z automatycznym usuwaniem węzła z pamięci po zakończeniu emisji.
*   **Uniwersalny system pocisków**: Zmodyfikowałem skrypt pocisku, wprowadzając zmienną `@export var direction`, co pozwoliło na użycie tego samego zasobu przez gracza i przeciwników.
*   **Sztuczna Inteligencja (AI)**: Przeciwnicy zyskali zdolność aktywnego namierzania gracza. Co określony interwał (`shoot_interval`) lokalizują statek gracza w grupie "player" i obliczają znormalizowany wektor kierunku strzału.
*   **System Punktacji i Kolizji**: Skonfigurowałem zaawansowaną macierz kolizji (Layer/Mask), aby pociski gracza trafiały tylko wrogów, a pociski wrogów tylko gracza. Zniszczenie obiektów automatycznie aktualizuje wynik w skrypcie głównym.

## Prezentacja działania (Wideo)
<video src="twoje_nagranie.mp4" width="100%" controls autoplay loop muted>
  Twoja przeglądarka nie obsługuje odtwarzania wideo.
</video>

## Uruchomienie
1.  Otwórz projekt w **Godot Engine 4.x**.
2.  Upewnij się, że w Inspektorze węzła **Enemy** przypisane są sceny `DeathParticles.tscn` oraz `EnemyBullet.tscn`.
3.  Uruchom scenę główną (`main.tscn`) za pomocą klawisza **F5**.
4.  **Sterowanie**: Strzałki/WSAD do poruszania się, **Spacja** (`ui_accept`) do strzelania.

## Trudności / refleksja
Największą trudnością okazało się poprawne zarządzanie warstwami kolizji po wprowadzeniu uniwersalnego skryptu pocisku – początkowo wrogowie trafiali samych siebie natychmiast po strzale. Rozwiązaniem było precyzyjne ustawienie masek bitowych tak, aby pocisk wroga (Layer 4) ignorował warstwę przeciwników (Layer 2). Odkryłem również, że spawnowanie efektów cząsteczkowych bezpośrednio w `get_tree().root` jest niezbędne, aby efekt nie znikał przedwcześnie wraz z usuwanym obiektem wroga.
