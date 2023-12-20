from config.settings import env


AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'users.backends.CinemaAuthBackend',
    # 'django.contrib.auth.backends.ModelBackend',
]

AUTH_API_LOGIN_URL = env.str('AUTH_API_LOGIN_URL')
AUTH_API_USER_INFO = env.str('AUTH_API_USER_INFO')

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation." "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation." "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation." "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation." "NumericPasswordValidator",
    },
]