# MacMedic — Aplikacja serwisowa Django

Aplikacja webowa wspierająca zarządzanie serwisem urządzeń Apple. Projekt stworzony w Django w ramach pracy zaliczeniowej. Obsługuje klientów, rezerwacje wizyt, pracowników, magazyn oraz generowanie faktur.

---

## Wymagania systemowe

- Python 3.10 lub nowszy
- Git
- pip (Python Package Installer)
- (Opcjonalnie) virtualenv

---

## Instalacja (lokalnie)

1. **Sklonuj repozytorium**
   git clone https://github.com/TWOJ-LOGIN/macmedic.git
   cd macmedic

2. Utwórz środowisko wirtualne
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/macOS:
    source venv/bin/activate

3. Zainstaluj zależności
    pip install -r requirements.txt

    Jeśli nie masz pliku requirements.txt, użyj:

    pip install django django-widget-tweaks

4. Wykonaj migracje
    python manage.py makemigrations
    python manage.py migrate

5. Utwórz superużytkownika (admin)
    python manage.py createsuperuser

6. Uruchom serwer
    python manage.py runserver

7. Otwórz w przeglądarce
    http://127.0.0.1:8000/
