import asyncio
import aiohttp
import json
from ticker_model import Kraken, Poloniex, Braziliex


async def get_json(client, url):
    async with client.get(url) as response:
        if response.status != 200:
            raise Exception(f"Error get api {url}")
        return await response.read()


async def echo(model):
    print(f"Exchange {model.name}")
    for ticker in model.tickers:
        print(f"Pair: {ticker.pair}, Ask: {ticker.ask}, BID: {ticker.bid}")
    print("---------\n")


async def get_api(client, url):
    api = await get_json(client, url)
    model = await get_model(url, api)
    await echo(model)


async def get_model(url, api):
    if 'kraken' in url:
        return Kraken.parse_raw(api)
    elif "poloniex" in url:
        api = Poloniex.prepare_data(api)
        return Poloniex(**api)
    elif 'braziliex' in url:
        api = Braziliex.prepare_data(api)
        return Braziliex(**api)
    else:
        raise Exception("No support api")


async def task(loop, url):
    async with aiohttp.ClientSession(loop=loop) as client:
        await get_api(client, url)


if __name__ == '__main__':
    exchange_api_lst = [
        'https://poloniex.com/public?command=returnTicker',
        'https://futures.kraken.com/derivatives/api/v3/tickers',
        'https://braziliex.com/api/v1/public/ticker'
    ]

    loop = asyncio.get_event_loop()
    task_list = [loop.create_task(task(loop, url)) for url in exchange_api_lst]

    loop.run_until_complete(asyncio.gather(*task_list))
