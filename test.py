import asyncio
from xml.etree.ElementInclude import include

from pydex.client import PyDex
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
        # manga = await client.get_random_manga(
        #     includes=["shounen", "romance"], contentRating=["safe"]
        # )
        manga = await client.create_manga(
            {
                "title": {"additionalProp1": "TEST"},
                "originalLanguage": "en",
                "status": "ongoing",
                "contentRating": "safe",
            }
        )
        manga_id = manga.id
        # manga = await client.update_manga(manga.id, {
        #         "title": {
        #             "additionalProp1": "TEST2"
        #         },
        #         "originalLanguage": "ja",
        #         "status": "completed",
        #         "contentRating": "suggestive",
        #         "version": 1
        # })
        # manga = await client.follow_manga(manga_id)
        # print(manga)
        # await client.unfollow_manga(manga_id)
        # await client.delete_manga(manga_id)
        # feed = await client.get_manga_feed("32fdfe9b-6e11-4a13-9e36-dcd8ea77b4e4")
        # print(feed)
        # tags = await client.get_tags()
        # print(tags)
        # reading = await client.get_my_list()
        # print(reading)
        # status = await client.get_manga_status("a96676e5-8ae2-425e-b549-7f15dd34a6d8")
        # print(status)
        # status = await client.get_manga_status("28c77530-dfa1-4b05-8ec3-998960ba24d4")
        # print(status)
        # status = await client.get_manga_status("37f5cce0-8070-4ada-96e5-fa24b1bd4ff9")
        # print(status)
        # new_status = await client.update_manga_status("a96676e5-8ae2-425e-b549-7f15dd34a6d8", status="completed")
        # status = await client.get_manga_status("a96676e5-8ae2-425e-b549-7f15dd34a6d8")
        # print(status)
        # draft = await client.get_manga_draft(manga_id)
        # print(draft.json())
    while True:
        pass


asyncio.run(main())
