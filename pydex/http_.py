import json
import aiohttp
import asyncio

from typing import (
    Optional,
    Any,
    List,
    Dict,
    Coroutine,
    Generator,
    OrderedDict,
    Union,
    Literal,
)
from aiohttp import ClientSession
from enum import Enum
from typing_extensions import Self
from .models import *
from .exceptions import *

ReqBody = Dict[str, Any]
Response = Optional[Union[Manga, List[Manga]]]


class URLs:
    base_search_url = "https://api.mangadex.org/manga"
    base_chapter_url = "https://api.mangadex.org/chapter"
    base_read_url = "https://mangadex.org/chapter"
    base_manga_info_url = "https://mangadex.org/manga"
    cover_url = "https://uploads.mangadex.org/covers"
    scanlation_base_url = "https://api.mangadex.org/group"


class Status:
    ongoing = "ongoing"
    completed = "completed"
    hiatus = "hiatus"
    cancelled = "cancelled"
    all_ = [ongoing, completed, hiatus, cancelled]


class ContentRating:
    safe = "safe"
    suggestive = "suggestive"
    erotica = "erotica"
    pornographic = "pornographic"
    all_ = [safe, suggestive, erotica, pornographic]


class http:

    _session: ClientSession

    def __init__(self, username: str, email: Optional[str], password: str) -> None:
        self.loop: asyncio.AbstractEventLoop
        self.username = username
        self.email = email
        self.password = password
        self.background_tasks = set()
        self.headers = {"Content-Type": "application/json"}

    def __await__(self):
        return self.start().__await__()

    async def start(self):
        loop = asyncio.get_running_loop()
        self.loop = loop
        self._session = aiohttp.ClientSession()
        async with self._session.post(
            "https://api.mangadex.org/auth/login",
            headers=self.headers,
            json={
                "username": self.username,
                "email": self.email,
                "password": self.password,
            },
        ) as res:
            if res.status == 200:
                resp = await res.read()
                r = json.loads(resp)
                self._session_token = r["token"]["session"]
                self._refresh_token = r["token"]["refresh"]
            else:
                raise UserPasswordMissMatch()
        return self

    async def end(self):
        async with self._session.post("https://api.mangadex.org/auth/logout") as res:
            if res.status == 200:
                print("logged out")
        await self._session.close()

    async def _get(self, url: str) -> Dict[str, Any]:
        async with self._session.get(url) as res:
            if res.status == 200:
                resp = await res.read()
                r = json.loads(resp)
                return r
            raise APIError()

    async def _post(self, url: str, payload: ReqBody) -> Response:
        async with self._session.post(url, json=payload, headers=self.headers) as res:
            if res.status == 200:
                resp = await res.read()
                r = json.loads(resp)
                raise NoResultsFound()
            raise APIError()

    async def _manga_search(
        self,
        *,
        title: str,
        limit: int = 10,
        offset: str = "",
        authors: str = Tags([], "authors").tags,
        artists: str = Tags([], "artists").tags,
        year: Union[str, int] = "",
        includedTags: str = Tags([], "includedTags").tags,
        includedTagsMode: Literal["AND", "OR"] = "AND",
        excludedTags: str = Tags([], "excludedTags").tags,
        excludedTagsMode: Literal["AND", "OR"] = "OR",
        status: str = Tags([], "status").tags,
        originalLanguage: str = Tags([], "originalLanguage").tags,
        excludedOriginalLanguage: str = Tags([], "excludedOriginalLanguage").tags,
        availableTranslatedLanguage: str = Tags([], "availableTranslatedLanguage").tags,
        publicationDemographic: str = Tags([], "publicationDemographic").tags,
        ids: str = Tags([], "ids").tags,
        contentRating: str = Tags([], "contentRating").tags,
        order: str = "[latestUploadedChapter]=desc",
        includes: str = Tags([], "includes").tags,
        hasAvailableChapters: Optional[bool] = None,
        group: str = "",
        createdAtSince: str = "",
        updatedAtSince: str = "",
    ) -> Response:
        if authors:
            authors = Tags(authors, "authors").tags

        if artists:
            artists = Tags(artists, "artists").tags

        if originalLanguage:
            originalLanguage = Tags(originalLanguage, "originalLanguage").tags

        if excludedOriginalLanguage:
            excludedOriginalLanguage = Tags(
                excludedOriginalLanguage, "excludedOriginalLanguage"
            ).tags

        if availableTranslatedLanguage:
            availableTranslatedLanguage = Tags(
                availableTranslatedLanguage, "availableTranslatedLanguage"
            ).tags

        if publicationDemographic:
            publicationDemographic = Tags(
                publicationDemographic, "publicationDemographic"
            ).tags

        if includes:
            includes = Tags(includes, "includes").tags

        if includedTags:
            includedTags = Tags(includedTags, "includedTags").tags

        if excludedTags:
            excludedTags = Tags(excludedTags, "excludedTags").tags

        if ids:
            ids = Tags(ids, "ids").tags

        if status:
            status = Tags(status, "status").tags

        if contentRating:
            contentRating = Tags(contentRating, "contentRating").tags

        url = f"{URLs.base_search_url}?limit={limit}&title={title}"
        for k, v in locals().items():
            if k not in ["limit", "title"]:
                if (
                    not isinstance(v, self.__class__)
                    and not isinstance(v, list)
                    and k != "url"
                    and v
                ):
                    if k != "order":
                        url += f"&{k}={v}"
                    else:
                        url += f"&{k}{v}"
                elif isinstance(v, list) and v or k in ["status", "contentRating"]:
                    url += f"&{k}[]={v}"
        print(url)
        results = await self._get(url)
        if results["data"]:
            if isinstance(results["data"], list):
                return [Manga(m) for m in results["data"]]
            else:
                return Manga(results["data"])
        raise NoResultsFound()

    async def get_manga_by_id(self, id: str) -> Response:
        url = f"{URLs.base_search_url}/{id}"
        result = await self._get(url)
        if not result:
            raise NoResultsFound()
        return Manga(result["data"])

    async def get_manga_agg(
        self,
        id: str,
        groups: str = Tags([], "groups").tags,
        translatedLanguage: str = Tags([], "translatedLanguage").tags,
    ) -> Optional[MangaAgg]:
        url = f"{URLs.base_search_url}/{id}/aggregate?id={id}"
        if groups:
            groups = Tags(groups, "groups").tags
        if translatedLanguage:
            translatedLanguage = Tags(translatedLanguage, "translatedLanguage").tags
        for k, v in locals().items():
            if k in ["groups", "translatedLanguage"]:
                url += f"&{k}={v}"
        result = await self._get(url)
        if result:
            if result["result"] != "error":
                return MangaAgg(result)
        raise NoResultsFound()

    async def get_random_manga(
        self,
        includes: str = Tags([], "includes").tags,
        contentRating: str = Tags(ContentRating.all_, "contentRating").tags,
    ) -> Response:
        if includes:
            includes = Tags(includes, "includes").tags
        if contentRating:
            contentRating = Tags(contentRating, "contentRating").tags
        url = f"{URLs.base_search_url}/random?contentRating[]={contentRating}&includes[]={includes}"
        result = await self._get(url)
        if not result:
            raise NoResultsFound()
        return Manga(result["data"])

    async def get_chapter(
        self,
        *,
        title: str,
        limit: int = 10,
        status: str = Tags(Status.all_, "status").tags,
        contentRating: str = Tags(ContentRating.all_, "contentRating").tags,
    ) -> List[Dict[str, Any]]:
        if status:
            status = Tags(status, "status").tags

        if contentRating:
            contentRating = Tags(contentRating, "contentRating").tags

        url = f"{URLs.base_search_url}?limit={limit}&includedTagsMode=AND&title={title}&status={status}&contentRating={contentRating}"
        result = await self._get(url)
        return result.get("data", [])


class PyDex:
    def __init__(self, *, username: str, email: str = "", password: str) -> None:
        self.username = username
        self.email = email
        self.password = password

    def __call__(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, Self]:
        return self.start(*args, **kwargs)

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, exc_type, exc, tb):
        await self.http.end()

    async def start(self) -> Self:
        self.http = await http(self.username, self.email, self.password)
        return self

    async def manga_search(self, *, title: str, **kwargs):
        return await self.http._manga_search(title=title, **kwargs)

    async def get_manga_by_id(self, id: str):
        return await self.http.get_manga_by_id(id)

    async def get_manga_agg(self, id: str, **kwargs):
        return await self.http.get_manga_agg(id, **kwargs)

    async def get_random_manga(self, **kwargs):
        return await self.http.get_random_manga(**kwargs)