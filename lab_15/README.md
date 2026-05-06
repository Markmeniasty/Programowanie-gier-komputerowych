# Neon Labyrinth - Proceduralny Labirynt Nieskończoności

## Opis projektu
Projekt jest zaawansowaną grą zręcznościową typu Top-Down, w której głównym wyzwaniem jest pokonywanie unikalnych, generowanych w czasie rzeczywistym labiryntów. Gra została zaprojektowana z naciskiem na **proceduralną generację treści** oraz **modularną architekturę kodu**.

> **Uwaga:** Projekt ma charakter rozwojowy. Obecna forma nie jest wersją finalną – z tygodnia na tydzień aplikacja będzie modernizowana i wzbogacana o nowe funkcjonalności, mechaniki oraz optymalizacje.

## Wybrana Technologia
*   **Język:** Python 3.13
*   **Biblioteka graficzna:** Raylib (wrapper `pyray`)
*   **Architektura:** Modularna (podział na moduły logiczne)
*   **System kontroli wersji:** Git

---

## Kluczowe Funkcjonalności

### 1. Proceduralna Generacja (Recursive Backtracker)
W przeciwieństwie do statycznych map, gra wykorzystuje algorytm **Recursive Backtracker** do tworzenia korytarzy.
*   **Gwarancja przejścia:** Algorytm zawsze generuje spójny labirynt, w którym istnieje co najmniej jedna ścieżka od startu do wyjścia.
*   **Unikalność:** Każdy poziom jest generowany w locie, co zapewnia nieskończoną regrywalność.
*   **Struktura:** Parametry są ustawione na generowanie ciasnych korytarzy, co zwiększa poziom trudności.

### 2. Modularna Architektura
Projekt został zrefaktoryzowany i podzielony na niezależne moduły:
*   `main.py`: Zarządzanie pętlą główną i obsługą stanów.
*   `maze_logic.py`: Serce algorytmu generującego.
*   `constants.py`: Centralne repozytorium ustawień (prędkość, kolory).
*   `states.py`: Definicja Maszyny Stanów (FSM).

### 3. System Kolizji i Fizyka
*   **Separacja osi:** Umożliwia płynne ślizganie się gracza po krawędziach ścian.
*   **Detekcja Circle-to-Rectangle:** Precyzyjne obliczenia kolizji między graczem a blokami labiryntu.

---

## Sterowanie
*   **WSAD:** Poruszanie się postacią.
*   **ENTER:** Start gry z poziomu menu.
*   **Zielone Pole (Exit):** Cel poziomu. Wejście w nie generuje nowy labirynt.

---

## Instrukcja uruchomienia

1.  Zainstaluj wymaganą bibliotekę:
    ```bash
    pip install raylib