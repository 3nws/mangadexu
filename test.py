import asyncio

from pydex.http_ import PyDex



async def main():
    client = await PyDex()
    # mangas = await client.search(title="asdasdaafasd", limit=2)
    # manga = await client.get_manga_by_id("a96676e5-8ae2-425e-b549-7f15dd34a6d8")
    manga = await client.get_manga_agg("a96676e5-8ae2-425e-b549-7f15dd34a6d8")
    print(manga)




asyncio.run(main())