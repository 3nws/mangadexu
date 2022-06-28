from this import d
from typing import Dict, Any, List, Union


class Tags:
    def __init__(self, tags: Union[str, List[str]], type: str) -> None:
        self.tags = self._convert(tags, type)

    def _convert(self, arr: Union[str, List[str]], type: str) -> str:
        if len(arr) == 1:
            res = f"&{type}[]={arr[0]}"
        elif type in ["contentRating", "status"]:
            res = ""
            for t in arr:
                res += f"&{type}[]={t}"
        else:
            res = f"&{type}[]=".join(arr)
        return res

    def __str__(self) -> str:
        return self.tags


class MangaAttributes:

    __slots__ = (
        "payload",
        "title",
        "altTitles",
        "description",
        "isLocked",
        "links",
        "originalLanguage",
        "lastVolume",
        "lastChapter",
        "publicationDemographic",
        "status",
        "year",
        "contentRating",
        "tags",
        "state",
        "chapterNumbersResetOnNewVolume",
        "createdAt",
        "updatedAt",
        "version",
        "availableTranslatedLanguages",
    )

    def __init__(self, payload: Dict[str, Any]) -> None:
        self.payload = payload
        self.title = payload.get("title", "").get("en", "")  # type: ignore
        self.altTitles = payload.get("altTitles", "")
        self.description = payload.get("description", "")
        self.isLocked = payload.get("isLocked", "")
        self.links = payload.get("links", "")
        self.originalLanguage = payload.get("originalLanguage", "")
        self.lastVolume = payload.get("lastVolume", "")
        self.lastChapter = payload.get("lastChapter", "")
        self.publicationDemographic = payload.get("publicationDemographic", "")
        self.status = payload.get("status", "")
        self.year = payload.get("year", "")
        self.contentRating = payload.get("contentRating", "")
        self.tags = payload.get("tags", "")
        self.state = payload.get("state", "")
        self.chapterNumbersResetOnNewVolume = payload.get(
            "chapterNumbersResetOnNewVolume", ""
        )
        self.createdAt = payload.get("createdAt", "")
        self.updatedAt = payload.get("updatedAt", "")
        self.version = payload.get("version", "")
        self.availableTranslatedLanguages = payload.get(
            "availableTranslatedLanguages", ""
        )

    def json(self):
        return self.payload


class Manga:

    __slots__ = ("payload", "id", "type", "attributes", "relationships")

    def __init__(self, payload: Dict[str, Any]) -> None:
        if payload:
            self.payload = payload
            self.id = payload.get("id", "")
            self.type = payload.get("type", "")
            self.attributes = MangaAttributes(payload.get("attributes", ""))
            self.relationships = payload.get("relationships", "")

    def json(self):
        if self.payload:
            return self.payload


class ChapterAgg:

    __slots__ = ("chapter", "id", "others", "count")

    def __init__(self, payload: Dict[str, Any]) -> None:
        self.chapter = payload.get("chapter", "")
        self.id = payload.get("id", "")
        self.others = payload["others"]
        self.count = payload.get("count", None)


class VolumeAgg:

    __slots__ = ("volume", "count", "chapters")

    def __init__(self, payload: Dict[str, Any]) -> None:
        self.volume = payload.get("volume", "")
        self.count = payload.get("count", None)
        self.chapters = [
            ChapterAgg(payload["chapters"][c]) for c in payload["chapters"]
        ]


class MangaAgg:

    __slots__ = ("volumes",)

    def __init__(self, payload: Dict[str, Any]) -> None:
        self.volumes = [VolumeAgg(payload["volumes"][v]) for v in payload["volumes"]]


class MangaRequest:

    __slots__ = (
        "payload",
        "title",
        "altTitles",
        "description",
        "authors",
        "artists",
        "links",
        "originalLanguage",
        "lastVolume",
        "lastChapter",
        "publicationDemographic",
        "status",
        "year",
        "contentRating",
        "chapterNumberResetOnNewVolume",
        "tags",
        "primaryCover",
        "version",
    )

    def __init__(self, payload: Dict[str, Any]) -> None:
        self.payload = payload
        self.title = payload.get("title", "")
        self.altTitles = payload.get("altTitles", [])
        self.description = payload.get("description", "")
        self.authors = payload.get("authors", [])
        self.artists = payload.get("artists", [])
        self.links = payload.get("links", [])
        self.originalLanguage = payload.get("originalLanguage", "")
        self.lastVolume = payload.get("lastVolume", "")
        self.lastChapter = payload.get("lastChapter", "")
        self.publicationDemographic = payload.get("publicationDemographic", "")
        self.status = payload.get("status", "")
        self.year = payload.get("year", "")
        self.contentRating = payload.get("contentRating", "")
        self.chapterNumberResetOnNewVolume = payload.get(
            "chapterNumberResetOnNewVolume", ""
        )
        self.tags = payload.get("tags", [])
        self.primaryCover = payload.get("primaryCover", "")
        self.version = payload.get("version", "")

    def json(self):
        return self.payload

class Relationship:

    __slots__ = (
        "payload",
        "id",
        "type",
        "related",
        "attributes"
    )

    def __init__(self, payload: Dict[str, Any]) -> None:
        if payload:
            self.payload = payload
            self.id = payload.get("id", "")
            self.type = payload.get("type", "")
            self.related = payload.get("related", "")
            self.attributes = payload.get("attributes", "")

    def json(self):
        return self.payload

class ChapterAttributes:

    __slots__ = (
        "payload",
        "title",
        "volume",
        "chapter",
        "pages",
        "translatedLanguage",
        "uploader",
        "externalUrl",
        "version",
        "createdAt",
        "updatedAt",
        "publishAt",
        "readableAt",
    )

    def __init__(self, payload: Dict[str, Any]) -> None:
        self.payload = payload
        self.title = payload.get("title", "")
        self.volume = payload.get("volume", "")
        self.chapter = payload.get("chapter", "")
        self.pages = payload.get("pages", 0)
        self.translatedLanguage = payload.get("translatedLanguage", "")
        self.uploader = payload.get("uploader", "")
        self.externalUrl = payload.get("externalUrl", "")
        self.version = payload.get("version", "")
        self.createdAt = payload.get("createdAt", "")
        self.updatedAt = payload.get("updatedAt", "")
        self.publishAt = payload.get("publishAt", "")
        self.readableAt = payload.get("readableAt", "")

    def json(self):
        return self.payload


class Chapter:

    __slots__ = (
        "payload",
        "id",
        "type",
        "attributes",
        "relationships"
    )

    def __init__(self, payload: Dict[str, Any]) -> None:
        if payload:
            self.payload = payload
            self.id = payload.get("id", "")
            self.type = payload.get("type", "")
            self.attributes = ChapterAttributes(payload.get("attributes", ""))
            self.relationships = [Relationship(r) for r in payload.get("relationships", [])]

    def json(self):
        return self.payload

class MangaRelationAttributes:

    __slots__ = (
        "payload",
        "relation",
        "version"
    )

    def __init__(self, payload: Dict[str, Any]) -> None:
        if payload:
            self.payload = payload
            self.relation = payload.get("relation", "")
            self.version = payload.get("version", 1)
    
    def json(self):
        return self.payload

class MangaRelation:

    __slots__ = (
        "payload",
        "id",
        "type",
        "attributes",
        "relationships"
    )

    def __init__(self, payload: Dict[str, Any]) -> None:
        if payload:
            self.payload = payload
            self.id = payload.get("id", "")
            self.type = payload.get("type", "")
            self.attributes = MangaRelationAttributes(payload.get("attributes", ""))
            self.relationships = [Relationship(r) for r in payload.get("relationships", [])]

    def json(self):
        return self.payload

class CoverAttributes:

    __slots__ = (
        "payload",
        "volume",
        "fileName",
        "description",
        "locale",
        "version",
        "createdAt",
        "updatedAt"
    )
    
    def __init__(self, payload: Dict[str, Any]) -> None:
        if payload:
            self.payload = payload
            self.volume = payload.get("volume", "")
            self.fileName = payload.get("fileName", "")
            self.description = payload.get("description", "")
            self.locale = payload.get("locale", "")
            self.version = payload.get("version", 1)
            self.createdAt = payload.get("createdAt", "")
            self.updatedAt = payload.get("updatedAt", "")

    def json(self):
        return self.payload

class Cover:

    __slots__ = (
        "payload",
        "id",
        "type",
        "attributes",
        "relationships"
    )

    def __init__(self, payload: Dict[str, Any]) -> None:
        if payload:
            self.payload = payload
            self.id = payload.get("id", "")
            self.type = payload.get("type", "")
            self.attributes = CoverAttributes(payload.get("attributes", ""))
            self.relationships = [Relationship(r) for r in payload.get("relationships", [])]