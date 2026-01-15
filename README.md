# 💾 RetroShop.exe

> **Poczuj nostalgię lat 90.** Sklep internetowy napisany w Django, stylizowany na system operacyjny Windows 95/98.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-4.x-green?style=flat-square&logo=django)
![CSS](https://img.shields.io/badge/Style-Retro-gray?style=flat-square)

## 📸 Zrzuty ekranu

*(Tutaj wstaw screeny swojego sklepu. Zrób zrzut ekranu strony głównej i szczegółów produktu, wrzuć je do folderu, a potem podmień linki poniżej)*

![Ekran Główny](https://via.placeholder.com/800x400?text=Tu+wstaw+screen+strony+glownej)
*Widok listy produktów w stylu okienkowym.*

## ⚙️ Funkcjonalności

Aplikacja posiada w pełni działający backend e-commerce ukryty pod warstwą retro interfejsu:

* **🛒 Koszyk:** Dodawanie produktów, zmiana ilości, usuwanie, podliczanie sumy.
* **📦 Zamówienia:** System Checkout (sprawdzanie stanów magazynowych, zapis historii).
* **👤 Profil Użytkownika:** Historia zamówień z opcją "Kup ponownie".
* **⭐ Recenzje:** System oceniania produktów (1-5 gwiazdek) i dodawania opinii.
* **🎨 UI/UX:**
    * Autorski styl CSS (brak gotowych frameworków typu Bootstrap).
    * Elementy interfejsu: okna, przyciski 3D, paski tytułu, oldschoolowe czcionki (MS Sans Serif).
    * Responsywność (Flexbox).

## 🛠️ Technologie

* **Backend:** Python, Django
* **Baza danych:** SQLite (domyślnie)
* **Frontend:** HTML5, CSS3 (Custom Retro CSS)

## 🚀 Jak uruchomić projekt?

1.  **Sklonuj repozytorium (lub pobierz pliki):**
    ```bash
    git clone [https://github.com/twoj-nick/retro-shop.git](https://github.com/twoj-nick/retro-shop.git)
    cd retro-shop
    ```

2.  **Stwórz i aktywuj wirtualne środowisko:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Zainstaluj wymagane biblioteki:**
    ```bash
    pip install django pillow
    ```

4.  **Wykonaj migracje bazy danych:**
    ```bash
    python manage.py migrate
    ```

5.  **Uruchom serwer:**
    ```bash
    python manage.py runserver
    ```

6.  **Uruchom "przeglądarkę":**
    Wejdź na `http://127.0.0.1:8000/` i ciesz się zakupami w stylu lat 90!

---
*Created with ❤️ & ☕ based on Windows 95 aesthetics.*
