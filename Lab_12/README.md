# Lab 12 – Efekty Środowiskowe, Kamera i Fizyka Uników

## Co zostało zrealizowane
W ramach tego laboratorium skupiłem się na poprawie warstwy wizualnej (game feel) oraz dodaniu zaawansowanych mechanik interakcji gracza z otoczeniem. Zaimplementowałem następujące elementy:
* **Klimatyczne tło (Zadanie 1)**: Dodałem węzeł `WorldEnvironment` z zasobem `ProceduralSkyMaterial`, konfigurując ciemną, kosmiczną paletę barw oraz redukując natężenie światła otoczenia (`sky_energy_multiplier`), aby zapobiec przepaleniu sceny.
* **Fizyczny korytarz i system obrażeń (Zadanie 2)**: Stworzyłem symetryczne ściany jako obiekty `StaticBody3D` z dopasowanymi bryłami kolizji `BoxShape3D`. Przekształciłem najwyższy węzeł gracza w `Area3D` i podłączyłem sygnał `body_entered` (sygnał ten jest kluczowy, ponieważ ściany są ciałami fizycznymi, a nie strefami przejściowymi typu area). Dodałem prywatną metodę `_take_damage(amount)` zarządzającą punktami życia.
* **Płynna kamera z opóźnieniem (Zadanie 3)**: Wydzieliłem kamerę z dotychczasowej hierarchii szyny i umieściłem ją jako niezależny element w korzeniu sceny. Wewnątrz `PathFollow3D` dodałem pusty węzeł `CameraTarget`. Za pomocą metody `lerp` w skrypcie kamery, podąża ona za punktem docelowym z regulowanym opóźnieniem (`lag_speed`), co znacząco wygładziło ruch.
* **Mechanika Barrel Roll i Niezniszczalność (Zadanie 4)**: Do modelu statku (`MeshInstance3D`) dodałem `AnimationPlayer` i przygotowałem 0.6-sekundową animację obrotu wokół osi Z (od `0` do `TAU`). W kodzie zaimplementowałem flagę `is_invincible`, która aktywuje się w momencie uniku (wywoływanego klawiszem Spacji / `ui_select`), blokując otrzymywanie jakichkolwiek obrażeń od ścian lub wrogów.

## Prezentacja działania (Wideo)
<video src="gierka.mp4" width="100%" controls autoplay loop muted>
  Twoja przeglądarka nie obsługuje odtwarzania wideo.
</video>

## Uruchomienie
1.  Otwórz projekt w środowisku **Godot Engine 4.x**.
2.  Upewnij się, że węzeł `Player` posiada poprawny typ `Area3D` oraz przypisany bezpośrednio do niego kształt `CollisionShape3D`.
3.  Sprawdź, czy w Inspektorze węzła `Camera3D` w polu `Camera Target` znajduje się referencja do węzła `CameraTarget`.
4.  Uruchom scenę główną (`main.tscn`) za pomocą klawisza **F5**.
5.  **Sterowanie**:
    * **Strzałki / WSAD**: Poruszanie się (w klamrach `limit_x` i `limit_y`).
    * **Enter (ui_accept)**: Strzelanie z uwzględnieniem cooldownu.
    * **Spacja (ui_select)**: Wykonanie uniku (*Barrel Roll*).

## Trudności / refleksja
Największym wyzwaniem podczas tej pracowni była poprawna reorganizacja hierarchii węzłów. Początkowo umieszczenie kształtu kolizji wewnątrz podwęzła `Hitbox` sprawiło, że główny skrypt `Player` był "ślepy" na zderzenia fizyczne. Zrozumienie, że sygnały kolizji muszą być bezpośrednio powiązane z węzłem nadrzędnym posiadającym skrypt, pozwoliło skutecznie rozwiązać ten problem. 

**Refleksja dot. CameraTarget:** Wydzielenie osobnego punktu do lerpowania zamiast bezpośredniego śledzenia statku okazało się kluczowe. Dzięki temu kamera zachowuje stabilną odległość w osi ruchu do przodu (szyny), a opóźnienie (lag) aplikowane jest wyłącznie na widowiskowe manewry gracza na boki i w pionie. Zapobiega to uciekaniu statku z kadru podczas ruchu szyny.