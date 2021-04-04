from pydantic import BaseModel, Field, validator
import json

MAX_LIMIT = 5


class SortedMixin:

    @staticmethod
    def lim_sorted(data):
        result = data[:MAX_LIMIT]
        result = sorted(result, key=lambda i: i.ask)
        return result


class TickerPoloniex(BaseModel):
    pair: str = Field(alias='pair')
    ask: float = Field(alias='lowestAsk')
    bid: float = Field(alias='highestBid')

    @validator("pair")
    def normalize_pair(cls, v):
        """'BTC_BTS' -> 'BTC:BTS'"""
        return v.replace("_", ":")


class Poloniex(BaseModel, SortedMixin):
    name: str = 'Poloniex'
    tickers: list[TickerPoloniex]

    @validator('tickers')
    def get_limit_tickers(cls, value):
        return cls.lim_sorted(value)

    @staticmethod
    def prepare_data(api):
        api = json.loads(api.decode("utf-8"))
        lst_api = []
        for k, v in api.items():
            v.update({"pair": k})
            lst_api.append(v)
        return {"tickers": lst_api}


class TickerKrane(BaseModel):
    pair: str = Field(alias='pair', default=None)
    ask: float = Field(alias='ask', default=None)
    bid: float = Field(alias='bid', default=None)


class Kraken(BaseModel, SortedMixin):
    name = 'Kraken'
    tickers: list[TickerKrane]

    @validator('tickers')
    def get_limit_tickers(cls, value):
        return cls.lim_sorted(value)


class TikerBraziliex(BaseModel):
    pair: str = Field(alias='market', default=None)
    ask: float = Field(alias='lowestAsk', default=None)
    bid: float = Field(alias='highestBid', default=None)


class Braziliex(BaseModel, SortedMixin):
    name = 'Braziliex'
    tickers: list[TikerBraziliex]

    @validator('tickers')
    def get_limit_tickers(cls, value):
        return cls.lim_sorted(value)

    @staticmethod
    def prepare_data(api):
        api = json.loads(api.decode("utf-8"))
        return {"tickers": list(api.values())}
