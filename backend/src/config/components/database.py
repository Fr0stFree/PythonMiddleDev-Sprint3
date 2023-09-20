from config.settings import env

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.int("POSTGRES_PORT"),
        "OPTIONS": {
            "options": f'-c search_path={env.str("POSTGRES_SEARCH_PATHS")}',
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
