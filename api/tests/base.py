from http import HTTPStatus
from typing import List
from typing import Optional
from typing import Union

import factory
from django.urls import reverse
from factories import UserFactory
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from api.models import User


class ActionClient:
    def __init__(self, api_client: APIClient) -> None:
        self.api_client = api_client
        self.user: Optional[User] = None

    def init_user(self) -> None:
        self.user = User.objects.create(username="api_user")
        self.api_client.force_authenticate(user=self.user, token=None)

    def request_create_user(self) -> Response:
        attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        url = reverse("users-list")
        return self.api_client.post(url, data=attributes)

    def create_user(self) -> dict:
        response = self.request_create_user()
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data


class TestViewSetBase(APITestCase):
    action_client: Optional[ActionClient] = None
    user: Optional[User] = None
    client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.admin = cls.create_superuser()
        cls.user = cls.create_api_user()
        cls.client = APIClient()
        cls.action_client = ActionClient(cls.client)
        cls.action_client.init_user()

    @staticmethod
    def create_api_user():
        return User.objects.create()

    @staticmethod
    def create_superuser():
        return User.objects.create_superuser("admin")

    @classmethod
    def detail_url(
        cls,
        key: Optional[Union[str, int]] = None,
        args: Optional[List[Union[str, int]]] = None,
    ) -> str:
        if not args:
            return reverse(f"{cls.basename}-detail", args=[key])
        return reverse(f"{cls.basename}-detail", args=[key, *args])

    @classmethod
    def list_url(cls, args: Optional[List[Union[str, int]]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def list(
        self,
        args: Optional[List[Union[str, int]]] = None,
        kwargs: Optional[dict] = None,
    ) -> dict:
        self.client.force_authenticate(user=self.user, token=None)
        response = self.client.get(self.list_url(args), kwargs)
        assert response.status_code == HTTPStatus.OK
        return response.json()

    def create(
        self,
        data: dict,
        args: Optional[List[Union[str, int]]] = None,
        formatting: Optional[str] = None,
    ) -> dict:
        response = self.request_create(
            data=data, args=args, formatting=formatting
        )
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create(
        self,
        data: dict,
        args: Optional[List[Union[str, int]]] = None,
        formatting: Optional[str] = None,
    ) -> Response:
        self.client.force_authenticate(user=self.user, token=None)
        response = self.client.post(
            self.list_url(args), data=data, format=formatting
        )
        return response

    def request_retrieve(
        self,
        key: Optional[Union[str, int]] = None,
        args: Optional[List[Union[str, int]]] = None,
    ) -> Response:
        self.client.force_authenticate(user=self.user, token=None)
        return self.client.get(self.detail_url(key, args))

    def retrieve(
        self,
        key: Optional[Union[str, int]] = None,
        args: Optional[List[Union[str, int]]] = None,
    ) -> dict:
        response = self.request_retrieve(key, args)
        assert response.status_code == HTTPStatus.OK
        return response.data

    def update(
        self,
        data: dict,
        key: Optional[Union[str, int]] = None,
        formatting: Optional[str] = None,
    ) -> dict:
        self.client.force_authenticate(user=self.user, token=None)
        response = self.client.patch(
            self.detail_url(key), data=data, format=formatting
        )
        assert response.status_code == HTTPStatus.OK
        return response.data

    def delete(self, key: Optional[Union[str, int]] = None) -> HTTPStatus:
        self.client.force_authenticate(user=self.admin, token=None)
        response = self.client.delete(self.detail_url(key))
        return response.status_code
