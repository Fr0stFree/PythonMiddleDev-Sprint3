import json
from typing import Final, TypedDict
import logging

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from requests.exceptions import ConnectTimeout
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

User = get_user_model()
logger = logging.getLogger(__name__)


class UserInfoResponse(TypedDict):
    id: str
    email: str
    first_name: str
    last_name: str
    roles: list[str]
    created_at: str


class CinemaAuthBackend(BaseBackend):
    TIMEOUT: Final[int] = 5
    ATTEMPTS: Final[int] = 5
    TIME_GAP: Final[int] = 1

    def authenticate(self, request, username=None, password=None):
        try:
            access_token = self._get_access_token(username, password)
            user_data = self._get_user_info(access_token)
            user = self._update_user(user_data)
        except Exception as error:
            logger.exception("Error during authentication, error: %s", error)
            return None

        return user

    @retry(stop=stop_after_attempt(ATTEMPTS), wait=wait_fixed(TIME_GAP), retry=retry_if_exception_type(ConnectTimeout))
    def _get_access_token(self, email: str, password: str) -> str:
        payload = {'email': email, 'password': password}
        response = requests.post(settings.AUTH_API_LOGIN_URL, data=json.dumps(payload), timeout=self.TIMEOUT)
        response.raise_for_status()
        return response.json()['access_token']

    @retry(stop=stop_after_attempt(ATTEMPTS), wait=wait_fixed(TIME_GAP), retry=retry_if_exception_type(ConnectTimeout))
    def _get_user_info(self, access_token: str) -> UserInfoResponse:
        response = requests.get(
            settings.AUTH_API_USER_INFO,
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=self.TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    def _update_user(self, user_data: UserInfoResponse) -> User:
        user, _ = User.objects.get_or_create(id=user_data['id'],)
        user.email = user_data['email']
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.is_admin = 'ADM' in user_data['roles']
        user.is_active = True
        user.save()
        return user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
