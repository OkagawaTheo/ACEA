# seu_projeto/settings_local.py
from pathlib import Path

try:
    BASE_DIR

except NameError:
    BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-**!$x^)05hbt2eamanp^yudra4v+ej8)6-ni7v_e15&8xm9kf@'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}