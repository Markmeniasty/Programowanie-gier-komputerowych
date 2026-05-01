# Neon Labyrinth - Podstawowa Mechanika i System Kolizji

## Opis projektu
Projekt jest grą zręcznościową typu Top-Down tworzoną w języku Python. Głównym celem gracza jest sprawne poruszanie się w labiryncie i omijanie przeszkód. Obecna wersja skupia się na implementacji płynnego sterowania oraz fizyki kolizji w przestrzeni 2D.

## Wybrana Technologia
*   **Silnik:** Raylib (biblioteka `pyray`)
*   **Język programowania:** Python 3.13
*   **System kontroli wersji:** Git

## Funkcjonalności i wymagania techniczne
W bieżącej wersji projektu zaimplementowano następujące elementy:

*   **Pętla gry (Game Loop):** Zarządzanie czasem za pomocą `Delta Time`, co zapewnia identyczną prędkość ruchu gracza niezależnie od liczby klatek na sekundę (FPS).
*   **System Sterowania:** Obsługa wejścia klawiatury (WSAD) umożliwiająca poruszanie się w ośmiu kierunkach.
*   **Obsługa Kolizji:** Implementacja wykrywania kolizji typu "koło-prostokąt" (`check_collision_circle_rec`).
*   **Separacja osi ruchu:** Logika ruchu została rozdzielona na oś X oraz Y, co pozwala na płynne ślizganie się gracza po krawędziach ścian zamiast całkowitego blokowania ruchu.
*   **Środowisko:** Statyczna mapa składająca się z zestawu przeszkód (ścian) definiujących granice gry.

## Instrukcja uruchomienia
1. Upewnij się, że masz zainstalowanego Pythona w wersji 3.10 lub nowszej.
2. Zainstaluj wymaganą bibliotekę komendą:
   ```bash
   pip install raylib