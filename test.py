import asyncio

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
        # print(manga.attributes.json())
        # manga = await client.get_manga_agg("32fdfe9b-6e11-4a13-9e36-dcd8ea77b4e4", translatedLanguage=["en", "de"])
        # manga = await client.get_random_manga(
        #     includes=["shounen", "romance"], contentRating=["safe"]
        # )
        # manga = await client.create_manga(
        #     {
        #         "title": {"additionalProp1": "TESTa"},
        #         "originalLanguage": "en",
        #         "status": "ongoing",
        #         "contentRating": "safe",
        #         # "cover": "https://i.imgur.com/cfYsAJH.png",
        #         "version": 1,
        #     }
        # )
        # manga_id = manga.id
        # manga = await client.create_manga(
        #     {
        #         "title": {"additionalProp1": "TESTa"},
        #         "originalLanguage": "en",
        #         "status": "ongoing",
        #         "contentRating": "safe",
        #         # "cover": "https://i.imgur.com/cfYsAJH.png",
        #         "version": 1,
        #     }
        # )
        # manga_id2 = manga.id
        # manga = await client.update_manga(
        #     manga.id,
        #     {
        #         "title": {"additionalProp1": "TEST2"},
        #         "originalLanguage": "en",
        #         "status": "ongoing",
        #         "contentRating": "safe",
        #         "authors": ["14b9cd88-3f29-4cf4-8c46-72f51dda924f"],
        #         "artists": ["14b9cd88-3f29-4cf4-8c46-72f51dda924f"],
        #         "cover": "https://i.imgur.com/cfYsAJH.png",
        #         "version": 1,
        #     },
        # )
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
        # draft = await client.submit_manga_draft(
        #     "be435719-a2ef-4f0e-852e-bceb6bb502a7",
        #     {
        #         "title": {"additionalProp1": "TESTa"},
        #         "originalLanguage": "en",
        #         "status": "ongoing",
        #         "contentRating": "safe",
        #         "version": 1,
        #     },
        # )
        # print(draft.json())
        # drafts = await client.get_drafts(10, state="draft", order={"createdAt": "desc"}, includes=["TEST"])
        # print(drafts)
        # relation = await client.add_relation(manga_id, targetManga=manga_id2, relation="monochrome")
        # print(relation)
        # relations = await client.get_manga_relations(manga_id2, includes=["kanojo"])
        # print(relations)
        # await client.delete_relation(manga_id, relation.id)
        # covers = await client.get_covers(limit=5, manga=["a96676e5-8ae2-425e-b549-7f15dd34a6d8", "37f5cce0-8070-4ada-96e5-fa24b1bd4ff9"])
        # print(covers)
    while True:
        pass
    

asyncio.run(main())
