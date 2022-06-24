
from typing_extensions import Self

from .http import http, ReqBody, Response
from .models import *

class PyDex:
    def __init__(self, *, username: str, email: str = "", password: str) -> None:
        self.username = username
        self.email = email
        self.password = password

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, exc_type, exc, tb):
        await self.http.end()

    async def start(self) -> Self:
        self.http = await http(self.username, self.email, self.password)
        return self

    async def manga_search(self, title: str, **kwargs):
        return await self.http._manga_search(title, **kwargs)

    async def get_manga_by_id(self, id: str):
        return await self.http._get_manga_by_id(id)

    async def get_manga_agg(self, id: str, **kwargs):
        return await self.http._get_manga_agg(id, **kwargs)

    async def get_random_manga(self, **kwargs):
        return await self.http._get_random_manga(**kwargs)

    async def create_manga(self, manga: ReqBody) -> Response:
        return await self.http._create_manga(manga)

    async def update_manga(self, id: str, manga: ReqBody):
        return await self.http._update_manga(id, manga)

    async def delete_manga(self, id: str):
        return await self.http._delete_manga(id)

    async def follow_manga(self, id: str):
        return await self.http._follow_manga(id)

    async def unfollow_manga(self, id: str):
        return await self.http._unfollow_manga(id)

    async def get_manga_feed(self, id: str, **kwargs):
        return await self.http._get_manga_feed(id, **kwargs)
