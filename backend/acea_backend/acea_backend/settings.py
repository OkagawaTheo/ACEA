from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

try:
    from .settings_local import *
except ImportError:
    pass

if 'DATABASES' not in locals():
    print("Aviso: settings_local.py não encontrado. Usando SQLite padrão.")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


if 'SECRET_KEY' not in locals():
    SECRET_KEY = 'chave_de_fallback_insegura_para_dev_se_settings_local_falhar'