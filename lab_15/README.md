# Neon Labyrinth 

Dynamiczna gra akcji typu **top-down maze shooter** osadzona w neonowym, proceduralnie generowanym świecie. Projekt łączy w sobie elementy eksploracji, survivalu oraz mechanikę walki arcade.

## 🛠️  Aktualizacje 

W fazie rozwoju zaimplementowano kluczowe systemy gry:

### ⚔️ System Walki i Postępu
* **Combat System**: Gracz posiada możliwość eliminacji przeciwników za pomocą pocisków energetycznych (inicjowanych klawiszem `SPACE`).
* **Level Scaling**: Poziom trudności rośnie dynamicznie – z każdym ukończonym labiryntem liczba Strażników (Sentinels) ulega zwiększeniu.
* **Procedural Generation**: Każdy poziom jest unikalnym labiryntem generowanym w czasie rzeczywistym.

### 🧠 Inteligentne AI
* **Detection & Chase**: Przeciwnicy reagują na obecność gracza. Po przekroczeniu promienia detekcji przechodzą z trybu patrolowania w tryb aktywnego pościgu.
* **Collision Logic**: Zaawansowane odbicia i blokowanie się AI na ścianach, uniemożliwiające przenikanie przez przeszkody.

### 🎨 Efekty Wizualne i Audio
* **Dynamic Lighting (Fog of War)**: Gracz widzi tylko ograniczony obszar wokół siebie, co potęguje klimat tajemnicy i zagrożenia.
* **Cyberpunk UI**: Menu główne wyposażone w efekty glitch, neonową siatkę (Retro Grid) oraz animowane cząsteczki tła.
* **Audio System**: Implementacja dedykowanej ścieżki dźwiękowej odtwarzanej w pętli.

### 💾 Zarządzanie danymi
* **Persistent Highscore**: System automatycznie zapisuje i odczytuje najlepszy osiągnięty poziom (Highscore).
* **Organized Structure**: Dane zapisywane są w dedykowanym folderze `/score`, a muzyka w `/music`.

---

## 🏗️ Plany rozwoju (Work in Progress)

**Uwaga:** Projekt jest w fazie aktywnej deweloperki i **będzie nadal rozszerzany**. W planach znajdują się m.in.:
* [ ] Implementacja różnych typów przeciwników (strzelających oraz bossów).
* [ ] System Power-upów (szybszy bieg, większy zasięg światła).
* [ ] Rozbudowa efektów dźwiękowych (SFX strzału i kolizji).
* [ ] Dodanie animowanych przejść między poziomami.

---

## 🎮 Sterowanie
| Klawisz | Akcja |
| :--- | :--- |
| **W, S, A, D** | Poruszanie się |
| **SPACE** | Strzał (Purge System) |
| **ENTER** | Start gry / Reset po porażce |
| **ESC** | Wyjście z gry |

---

## Wybrana Technologia
*   **Język:** Python 3.13
*   **Biblioteka graficzna:** Raylib (wrapper `pyray`)
*   **Architektura:** Modularna (podział na moduły logiczne)
*   **System kontroli wersji:** Git

---
*Projekt realizowany w ramach przedmiotu: Programowanie gier komputerowych.*
## Instrukcja uruchomienia

1.  Zainstaluj wymaganą bibliotekę:
    ```bash
    pip install raylib
    