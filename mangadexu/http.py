import json
from wsgiref import headers
import aiohttp
import asyncio

from typing import (
    Optional,
    Any,
    List,
    Dict,
    Union,
    Literal,
)
from aiohttp import ClientSession, FormData
from .models import *
from .exceptions import *

ReqBody = Union[Dict[str, Any], FormData]
Response = Optional[Union[Manga, List[Manga], Chapter, List[Chapter], ReqBody, MangaRelation, Cover, List[Cover]]]


class URLs:
    base_search_url = "https://api.mangadex.org/manga"
    base_chapter_url = "https://api.mangadex.org/chapter"
    base_read_url = "https://mangadex.org/chapter"
    base_manga_info_url = "https://mangadex.org/manga"
    cover_url = "https://api.mangadex.org/cover"
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
    def __init__(self, username: str, email: Optional[str], password: str) -> None:
        self.loop: asyncio.AbstractEventLoop
        self.username = username
        self.email = email
        self.password = password
        self.background_tasks = set()
        self.headers = {"Content-Type": "application/json"}
        self._logged = False
        self._session: Optional[ClientSession] = None

    def __await__(self):
        return self.start().__await__()

    async def _make_session(self):
        self._session = aiohttp.ClientSession(headers=self.headers)

    async def start(self):
        loop = asyncio.get_running_loop()
        self.loop = loop
        if self._session is None:
            await self._make_session()
        if self.username and self.password:
            async with self._session.post(
                "https://api.mangadex.org/auth/login",
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
                    self.headers["Authorization"] = f"Bearer {self._session_token}"
                    self.headers["accept"] = "application/json"
                    await self._session.close()
                    self._session = aiohttp.ClientSession(headers=self.headers)
                    self._logged = True
                else:
                    raise UserPasswordMissMatch()
        return self

    async def end(self):
        if self._session is None:
            await self._make_session()
        if self._logged:
            async with self._session.post(
                "https://api.mangadex.org/auth/logout"
            ) as res:
                if res.status == 200:
                    print("logged out")
            await self._session.close()

    async def _get(self, url: str) -> Dict[str, Any]:
        if self._session is None:
            await self._make_session()
        print(url)
        async with self._session.get(url) as res:
            print(await res.json())
            if res.status >= 200 and res.status < 300:
                resp = await res.read()
                r = json.loads(resp)
                return r
            raise APIError()

    async def _post(self, url: str, **kwargs: ReqBody) -> Response:
        if self._session is None:
            await self._make_session()
        if "json" in kwargs:
            async with self._session.post(url, json=kwargs["json"]) as res:
                # print(await res.json())
                if res.status >= 200 and res.status < 300:
                    resp = await res.read()
                    r = json.loads(resp)
                    if r:
                        if r.get("type", "") == "cover_art":
                            return Cover(r.get("data", None))
                        if r.get("type", "") == "manga_relation":
                            return MangaRelation(r.get("data", None))
                        return Manga(r.get("data", None))
                    raise NoResultsFound()
                raise APIError()
        else:
            async with self._session.post(url, data=kwargs["data"]) as res:
                print(await res.read())
                # print(await res.json())
                if res.status >= 200 and res.status < 300:
                    resp = await res.read()
                    r = json.loads(resp)
                    if r:
                        if r.get("type", "") == "cover_art":
                            return Cover(r.get("data", None))
                        if r.get("type", "") == "manga_relation":
                            return MangaRelation(r.get("data", None))
                        return Manga(r.get("data", None))
                    raise NoResultsFound()
                raise APIError()

    async def _put(self, url: str, payload: ReqBody) -> Response:
        if self._session is None:
            await self._make_session()
        async with self._session.put(url, json=payload) as res:
            # print(await res.json())
            if res.status >= 200 and res.status < 300:
                resp = await res.read()
                r = json.loads(resp)
                if r:
                    return Manga(r["data"])
                raise NoResultsFound()
            raise APIError()

    async def _delete(self, url: str) -> None:
        if self._session is None:
            await self._make_session()
        id = url.split("/")[-1]
        async with self._session.delete(url) as res:
            # print(await res.json())
            if res.status >= 200 and res.status < 300:
                resp = await res.read()
                r = json.loads(resp)
                if r:
                    print(f"Manga with id: {id} has been deleted/unfollowed.")
                else:
                    raise NoResultsFound()
            else:
                raise APIError()

    async def _manga_search(
        self,
        title: str,
        *,
        limit: int = 10,
        offset: Optional[int] = None,
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
        hasAvailableChapters: Optional[Union[str, bool]] = None,
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
        else:
            status = Tags(Status.all_, "status").tags

        if contentRating:
            contentRating = Tags(contentRating, "contentRating").tags
        else:
            contentRating = Tags(ContentRating.all_, "contentRating").tags

        if hasAvailableChapters is not None:
            hasAvailableChapters = str(hasAvailableChapters).lower()

        url = f"{URLs.base_search_url}"
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
        results = await self._get(url)
        if results["data"]:
            if isinstance(results["data"], list):
                return [Manga(m) for m in results["data"]]
            else:
                return Manga(results["data"])
        raise NoResultsFound()

    async def _get_manga_by_id(self, id: str) -> Response:
        url = f"{URLs.base_search_url}/{id}"
        result = await self._get(url)
        if not result:
            raise NoResultsFound()
        return Manga(result["data"])

    async def _get_manga_agg(
        self,
        id: str,
        *,
        groups: str = Tags([], "groups").tags,
        translatedLanguage: str = Tags([], "translatedLanguage").tags,
    ) -> Optional[MangaAgg]:
        url = f"{URLs.base_search_url}/{id}/aggregate"
        if groups:
            groups = Tags(groups, "groups").tags
            url += f"?groups={groups}"
        elif translatedLanguage and groups:
            translatedLanguage = Tags(translatedLanguage, "translatedLanguage").tags
            url += f"&translatedLanguage={translatedLanguage}"
        else:
            translatedLanguage = Tags(translatedLanguage, "translatedLanguage").tags
            url += f"?translatedLanguage={translatedLanguage}"
        result = await self._get(url)
        if result:
            if result["result"] != "error":
                return MangaAgg(result)
        raise NoResultsFound()

    async def _get_random_manga(
        self,
        includes: str = Tags([], "includes").tags,
        contentRating: str = Tags([], "contentRating").tags,
    ) -> Response:
        if includes:
            includes = Tags(includes, "includes").tags
        if contentRating:
            contentRating = Tags(contentRating, "contentRating").tags
        url = f"{URLs.base_search_url}/random?{contentRating}&includes[]={includes}"
        result = await self._get(url)
        if not result:
            raise NoResultsFound()
        return Manga(result["data"])

    async def _get_chapter(
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

    async def _create_manga(self, manga: ReqBody) -> Response:
        url = f"{URLs.base_search_url}"
        return await self._post(url, json=manga)

    async def _update_manga(self, id: str, manga: ReqBody) -> Response:
        url = f"{URLs.base_search_url}"
        return await self._put(f"{url}/{id}", manga)

    async def _delete_manga(
        self,
        id: str,
    ) -> Response:
        url = f"{URLs.base_search_url}/{id}"
        return await self._delete(url)

    async def _follow_manga(
        self,
        id: str,
    ) -> Response:
        url = f"{URLs.base_search_url}/{id}/follow"
        return await self._post(url, payload={})

    async def _unfollow_manga(
        self,
        id: str,
    ) -> Response:
        url = f"{URLs.base_search_url}/{id}/follow"
        return await self._delete(url)

    async def _get_manga_feed(
        self,
        id: str,
        *,
        limit: int = 10,
        offset: Optional[int] = None,
        translatedLanguage: str = Tags([], "translatedLanguage").tags,
        originalLanguage: str = Tags([], "originalLanguage").tags,
        excludedOriginalLanguage: str = Tags([], "excludedOriginalLanguage").tags,
        contentRating: str = Tags([], "contentRating").tags,
        excludedGroups: str = Tags([], "excludedGroups").tags,
        excludedUploaders: str = Tags([], "excludedUploaders").tags,
        includeFutureUpdates: Optional[Union[str, bool]] = True,
        createdAtSince: str = "",
        updatedAtSince: str = "",
        publishAtSince: str = "",
        order: str = "[createdAt]=asc&order[updatedAt]=asc&order[publishAt]=asc&order[readableAt]=asc&order[volume]=asc&order[chapter]=asc",
        includes: str = Tags([], "includes").tags,
    ) -> Response:

        if translatedLanguage:
            translatedLanguage = Tags(translatedLanguage, "translatedLanguage").tags

        if originalLanguage:
            originalLanguage = Tags(originalLanguage, "originalLanguage").tags

        if excludedOriginalLanguage:
            excludedOriginalLanguage = Tags(
                excludedOriginalLanguage, "excludedOriginalLanguage"
            ).tags

        if includes:
            includes = Tags(includes, "includes").tags

        if excludedGroups:
            excludedGroups = Tags(excludedGroups, "excludedGroups").tags

        if excludedUploaders:
            excludedUploaders = Tags(excludedUploaders, "excludedUploaders").tags

        if contentRating:
            contentRating = Tags(contentRating, "contentRating").tags
        else:
            contentRating = Tags(ContentRating.all_, "contentRating").tags

        if includeFutureUpdates is not None:
            includeFutureUpdates = str(includeFutureUpdates).lower()

        url = f"{URLs.base_search_url}/{id}/feed?limit={limit}"
        for k, v in locals().items():
            if k not in ["limit", "id"]:
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
                elif isinstance(v, list) and v or k in ["contentRating"]:
                    url += f"&{k}[]={v}"
        results = await self._get(url)
        if results["data"]:
            if isinstance(results["data"], list):
                return [Chapter(c) for c in results["data"]]
            else:
                return Chapter(results["data"])
        raise NoResultsFound()

    async def _get_tags(self) -> Response:
        url = f"{URLs.base_search_url}/tag"
        return await self._get(url)

    async def _get_my_list(self, *, status: Optional[str] = None) -> Response:
        url = f"{URLs.base_search_url}/status"
        if status:
            url += f"?status={status}"
        return await self._get(url)

    async def _get_manga_status(self, *, id: str) -> Response:
        url = f"{URLs.base_search_url}/{id}/status"
        return await self._get(url)

    async def _update_manga_status(
        self,
        *,
        id: str,
        status: Optional[str] = None,
    ) -> Response:
        url = f"{URLs.base_search_url}/{id}/status"
        if status is None:
            status = "null"
        return await self._post(url, json={"status": status})

    async def _get_manga_draft(
        self,
        id: str,
        *,
        includes: str = Tags([], "includes").tags,
    ) -> Response:
        url = f"{URLs.base_search_url}/draft/{id}"
        if includes:
            includes = Tags(includes, "includes").tags
            url += f"?includes[]={includes}"
        return Manga((await self._get(url))["data"])

    async def _submit_manga_draft(self, id: str, manga: ReqBody) -> Response:
        url = f"{URLs.base_search_url}/draft/{id}/commit"
        return await self._post(url, json=manga)

    async def _get_drafts(
        self,
        limit: Optional[int],
        *,
        state: Optional[Literal["draft", "submitted", "rejected"]],
        offset: Optional[int] = None,
        order: str = "[createdAt]=desc",
        includes: str = Tags([], "includes").tags,
    ) -> Response:
        url = f"{URLs.base_search_url}/draft?limit={limit}"
        if state:
            url += f"&state={state}"
        if offset:
            url += f"&offset={offset}"
        if includes:
            includes = Tags(includes, "includes").tags
            url += f"&includes={includes}"
        return await self._get(url)

    async def _get_manga_relations(
        self,
        id: str,
        *,
        includes: str = Tags([], "includes").tags,
    ) -> Response:
        url = f"{URLs.base_search_url}/{id}/relation"
        if includes:
            includes = Tags(includes, "includes").tags
            url += f"?includes={includes}"
        return await self._get(url)

    async def _add_relation(
        self,
        id: str,
        *,
        targetManga: str,
        relation: Literal[
            "monochrome",
            "main_story",
            "adapted_from",
            "based_on",
            "prequel",
            "side_story",
            "doujinshi",
            "same_franchise",
            "shared_universe",
            "sequel",
            "spin_off",
            "alternate_story",
            "alternate_version",
            "preserialization",
            "colored",
            "serialization",
        ],
    ) -> Response:
        url = f"{URLs.base_search_url}/{id}/relation"
        return await self._post(url, json={
            "targetManga": targetManga,
            "relation": relation
        })

    async def _delete_relation(
        self,
        id: str,
        mangaId: str
    ) -> Response:
        url = f"{URLs.base_search_url}/{mangaId}/relation/{id}"
        return await self._delete(url)

    async def _get_covers(
        self,
        *,
        limit: Optional[int]=10,
        offset: Optional[int] = None,
        manga: str = Tags([], "manga").tags,
        ids: str = Tags([], "ids").tags,
        uploaders: str = Tags([], "uploaders").tags,
        locales: str = Tags([], "locales").tags,
        order: str = "[createdAt]=asc&order[updatedAt]=asc&order[volume]=asc",
        includes: str = Tags([], "includes").tags,
    ) -> Response:
        if manga:
            manga = Tags(manga, "manga").tags
        if ids:
            ids = Tags(ids, "ids").tags
        if uploaders:
            uploaders = Tags(uploaders, "uploaders").tags
        if locales:
            locales = Tags(locales, "locales").tags
        if includes:
            includes = Tags(includes, "includes").tags
        url = f"{URLs.cover_url}?limit={limit}"
        for k, v in locals().items():
            if k not in ["limit"]:
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
                elif isinstance(v, list) and v:
                    url += f"&{k}[]={v}"
        results = await self._get(url)
        if results["data"]:
            if isinstance(results["data"], list):
                return [Cover(c) for c in results["data"]]
            else:
                return Cover(results["data"])
        raise NoResultsFound()

    async def _upload_cover(
        self,
        id: str,
        image: bytes,
        volume: int,
        description: str,
        locale: str,
    ) -> Response:
        url = f"{URLs.cover_url}/{id}"
        self._session.headers["Content-Type"] = "multipart/form-data"
        form = FormData()
        form.add_field("file", value=image, content_type="image/jpeg")
        form.add_field("volume", value=str(volume))
        form.add_field("description", value=description)
        form.add_field("locale", value=locale)
        res = await self._post(url, data=form)
        self._session.headers["Content-Type"] = "application/json"
        return res

    async def _get_chapters(
        self,
        limit: Optional[int],
        *,
        manga: Optional[str]=None,
        title: Optional[str]=None,
        offset: Optional[int] = None,
        originalLanguage: str = Tags([], "originalLanguage").tags,
        excludedOriginalLanguage: str = Tags([], "excludedOriginalLanguage").tags,
        availableTranslatedLanguage: str = Tags([], "availableTranslatedLanguage").tags,
        ids: str = Tags([], "ids").tags,
        contentRating: str = Tags([], "contentRating").tags,
        excludedGroups: str = Tags([], "excludedGroups").tags,
        excludedUploaders: str = Tags([], "excludedUploaders").tags,
        order: str = "[createdAt]=asc&order[updatedAt]=asc&order[publishAt]=asc&order[readableAt]=asc&order[volume]=asc&order[chapter]=asc",
        includes: str = Tags([], "includes").tags,
        groups: str = Tags([], "groups").tags,
        uploader: Optional[str]=None,
        volume: Optional[str]=None,
        chapter: Optional[str]=None,
        includeFutureUpdates: Optional[Union[str, bool]] = True,
        createdAtSince: str = "",
        updatedAtSince: str = "",
        publishAtSince: str = "",
    ) -> Response:

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

        if includes:
            includes = Tags(includes, "includes").tags

        if ids:
            ids = Tags(ids, "ids").tags

        if excludedGroups:
            excludedGroups = Tags(excludedGroups, "excludedGroups").tags

        if excludedUploaders:
            excludedUploaders = Tags(excludedUploaders, "excludedUploaders").tags

        if contentRating:
            contentRating = Tags(contentRating, "contentRating").tags
        else:
            contentRating = Tags(ContentRating.all_, "contentRating").tags

        if includeFutureUpdates is not None:
            includeFutureUpdates = str(includeFutureUpdates).lower()

        url = f"{URLs.base_chapter_url}?limit={limit}"
        for k, v in locals().items():
            if k not in ["limit"]:
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
                elif isinstance(v, list) and v or k in ["contentRating"]:
                    url += f"&{k}[]={v}"
        results = await self._get(url)
        if results["data"]:
            if isinstance(results["data"], list):
                return [Chapter(m) for m in results["data"]]
            else:
                return Chapter(results["data"])
        raise NoResultsFound()