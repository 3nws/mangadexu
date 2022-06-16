from typing import Dict, Any




class MangaAttributes:

    __slots__ = (
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
        "availableTranslatedLanguages"
    )

    def __init__(self, response: Dict[str, Any]) -> None:
        self.title = response.get("title", "").get("en", "")  # type: ignore
        self.altTitles = response.get("altTitles", "")
        self.description = response.get("description", "")
        self.isLocked = response.get("isLocked", "")
        self.links = response.get("links", "")
        self.originalLanguage = response.get("originalLanguage", "")
        self.lastVolume = response.get("lastVolume", "")
        self.lastChapter = response.get("lastChapter", "")
        self.publicationDemographic = response.get("publicationDemographic", "")
        self.status = response.get("status", "")
        self.year = response.get("year", "")
        self.contentRating = response.get("contentRating", "")
        self.tags = response.get("tags", "")
        self.state = response.get("state", "")
        self.chapterNumbersResetOnNewVolume = response.get("chapterNumbersResetOnNewVolume", "")
        self.createdAt = response.get("createdAt", "")
        self.updatedAt = response.get("updatedAt", "")
        self.version = response.get("version", "")
        self.availableTranslatedLanguages = response.get("availableTranslatedLanguages", "")
        


class Manga:

    __slots__ = (
        "id",
        "type",
        "attributes",
        "relationships"
    )

    def __init__(self, response: Dict[str, Any]) -> None:
        self.id = response.get("id", "")
        self.type = response.get("type", "")
        self.attributes = MangaAttributes(response.get("attributes", ""))
        self.relationships = response.get("relationships", "")


class ChapterAgg:
    
    __slots__ = (
        "chapter",
        "id",
        "others",
        "count"
    )
    def __init__(self, response: Dict[str, Any]) -> None:
        self.chapter = response.get("chapter", "")
        self.id = response.get("id", "")
        self.others = response["others"]
        self.count = response.get("count", None)


class VolumeAgg:

    __slots__ = (
        "volume",
        "count",
        "chapters"
    )

    def __init__(self, response: Dict[str, Any]) -> None:
        self.volume = response.get("volume", "")
        self.count = response.get("count", None)
        self.chapters = [ChapterAgg(response["chapters"][c]) for c in response["chapters"]]


class MangaAgg:

    __slots__ = (
        "volumes",
    )

    def __init__(self, response: Dict[str, Any]) -> None:
        self.volumes = [VolumeAgg(response["volumes"][v]) for v in response["volumes"]]