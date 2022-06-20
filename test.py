import asyncio

from pydex.http_ import PyDex
from config import *


async def main():
    async with PyDex(username=USERNAME, password=PASS) as client:
        mangas = await client.manga_search(
            title="kanojo",
            limit=10,
            authors=[
                "d78b9656-71c4-4b51-b1ce-2fe1a571ce2c",
                "686a63a6-a96f-4a7e-a5cf-80274e0b9e20",
            ],
            ids=[
                "d78b9656-71c4-4b51-b1ce-2fe1a571ce2c",
                "686a63a6-a96f-4a7e-a5cf-80274e0b9e20",
            ],
            includedTags=[
                "4d32cc48-9f00-4cca-9b5a-a839f0764984",
                "423e2eae-a7a2-4a8b-ac03-a8351462d71d",
            ],
            excludedTags=[
                "a3c67850-4684-404e-9b7f-c69850ee5da6",
                "e5301a23-ebd9-49dd-a0cb-2add944c7fe9",
            ],
            publicationDemographic=[
                "shounen",
                "shoujo",
            ],
            availableTranslatedLanguage=[
                "en",
                "en",
            ],
            excludedOriginalLanguage=[
                "de",
                "de",
            ],
            originalLanguage=[
                "ja",
                "en",
            ],
            includes=[
                "Ka",
                "Ok",
            ],
            artists=[
                "4218b1ee-cde4-44dc-84c7-d9a794a7e56d",
                "08ebed9d-57dd-40ac-990f-9fb77c7ac256",
            ],
            contentRating=["safe"],
            status=["ongoing"]
        )
        # manga = await client.get_manga_by_id("a96676e5-8ae2-425e-b549-7f15dd34a6d8")
        # manga = await client.get_manga_agg("a96676e5-8ae2-425e-b549-7f15dd34a6d8")
        # (print(m) for m in mangas)
        # manga = await client.get_random_manga(includes=["shounen", "romance"], content_rating="safe")
        print(mangas)
    while True:
        pass


asyncio.run(main())
