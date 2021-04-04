import asyncio
import aiohttp
from importlib import import_module

exchanges = {
    'kraken': 'https://poloniex.com/public?command=returnTicker',
    'poloniex': 'https://futures.kraken.com/derivatives/api/v3/tickers',
    'braziliex': 'https://braziliex.com/api/v1/public/ticker'
}


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
    mod = None
    for exc in exchanges.keys():
        if exc in url:
            mod = import_module(f'models.{exc}')
            break
    if not mod:
        raise Exception("No support api")
    exc_cls = getattr(mod, 'Exchange')

    api = exc_cls.prepare_data(api)
    return exc_cls(**api)


async def task(loop, url):
    async with aiohttp.ClientSession(loop=loop) as client:
        await get_api(client, url)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task_list = [loop.create_task(task(loop, url)) for url in exchanges.values()]

    loop.run_until_complete(asyncio.gather(*task_list))
