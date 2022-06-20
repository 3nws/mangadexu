import asyncio

from pydex.http_ import PyDex
from config import *


async def main():
    async with PyDex(username=USERNAME, password=PASS) as client:
        # mangas = await client.manga_search(
        #     "kanojo",
        #     limit=10,
        #     authors=[
        #         "08ebed9d-57dd-40ac-990f-9fb77c7ac256",
        #     ],
        #     ids=[
        #         "32fdfe9b-6e11-4a13-9e36-dcd8ea77b4e4",
        #     ],
        #     includedTags=[
        #         "4d32cc48-9f00-4cca-9b5a-a839f0764984",
        #         "423e2eae-a7a2-4a8b-ac03-a8351462d71d",
        #     ],
        #     year=2017,
        #     includedTagsMode="OR",
        #     excludedTags=[
        #         "a3c67850-4684-404e-9b7f-c69850ee5da6",
        #         # "e5301a23-ebd9-49dd-a0cb-2add944c7fe9",
        #     ],
        #     excludedTagsMode="OR",
        #     publicationDemographic=[
        #         "shounen",
        #     ],
        #     hasAvailableChapters=True,
        #     availableTranslatedLanguage=[
        #         "en",
        #         "en",
        #     ],
        #     excludedOriginalLanguage=[],
        #     originalLanguage=[
        #         "ja",
        #     ],
        #     includes=[
        #         "Ka",
        #         "Ok",
        #     ],
        #     artists=[
        #         "08ebed9d-57dd-40ac-990f-9fb77c7ac256",
        #     ],
        #     contentRating=["safe", "suggestive"],
        #     status=["ongoing"],
        # )
        # manga = await client.get_manga_by_id("32fdfe9b-6e11-4a13-9e36-dcd8ea77b4e4")
        # manga = await client.get_manga_agg("32fdfe9b-6e11-4a13-9e36-dcd8ea77b4e4", translatedLanguage=["en", "de"])
        manga = await client.get_random_manga(
            includes=["shounen", "romance"], contentRating=["safe"]
        )
        print(manga)
    while True:
        pass


asyncio.run(main())
