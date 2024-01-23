import json

import aiohttp
import asyncio


async def main(key_word: str):
    async def parser(wb):
        wb = json.loads(wb)
        cards = wb["data"]["products"][0:10]
        return ["Название " + card["name"] + " Ссылка " + f"https://www.wildberries.ru/catalog/{card['id']}/detail.aspx"
                for
                card
                in cards]

    url = (f"https://search.wb.ru/exactmatch/ru/common/v4/search?"
           f"appType=1&curr=rub&dest=-1257786&page={1}"
           f"&query={'%20'.join(key_word.split())}&resultset=catalog"
           f"&sort=popular&spp=24&suppressSpellcheck=false")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json_res = await response.text()
            return await parser(json_res)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main("games"))
