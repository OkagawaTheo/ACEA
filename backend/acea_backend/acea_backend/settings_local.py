# seu_projeto/settings_local.py

# A CHAVE SECRETA REAL (obtida da instalação inicial do Django)
# Mantenha esta chave LONGA e SECRETA!
SECRET_KEY = 'django-insecure-**!$x^)05hbt2eamanp^yudra4v+ej8)6-ni7v_e15&8xm9kf@'

# Configuração do Banco de Dados Local (SQLite neste caso, mas poderia ser Postgres/MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}