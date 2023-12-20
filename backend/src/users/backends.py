import http
import json

import requests
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CinemaAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        payload = {'email': username, 'password': password}
        response = requests.post(settings.AUTH_API_LOGIN_URL, data=json.dumps(payload))
        if response.status_code != http.HTTPStatus.OK:
            return None

        auth_data = response.json()
        if 'access_token' not in auth_data:
            return None

        response = requests.get(
            settings.AUTH_API_USER_INFO,
            headers={'Authorization': f'Bearer {auth_data["access_token"]}'}
        )
        if response.status_code != http.HTTPStatus.OK:
            return None
        user_data = response.json()

        try:
            user, created = User.objects.get_or_create(id=user_data['id'],)
            user.email = user_data.get('email')
            user.first_name = user_data.get('first_name')
            user.last_name = user_data.get('last_name')
            user.is_admin = 'ADM' in user_data.get('roles')
            user.is_active = True
            user.save()
        except Exception:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
