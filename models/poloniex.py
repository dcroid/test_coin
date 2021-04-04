from pydantic import BaseModel, Field, validator
import json
from .mixin import SortedMixin


class TickerPoloniex(BaseModel):
    pair: str = Field(alias='pair')
    ask: float = Field(alias='lowestAsk')
    bid: float = Field(alias='highestBid')

    @validator("pair")
    def normalize_pair(cls, v):
        """'BTC_BTS' -> 'BTC:BTS'"""
        return v.replace("_", ":")


class Exchange(BaseModel, SortedMixin):
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
