from pydantic import BaseModel, Field, validator
from .mixin import SortedMixin
import json


class TikerBraziliex(BaseModel):
    pair: str = Field(alias='market', default=None)
    ask: float = Field(alias='lowestAsk', default=None)
    bid: float = Field(alias='highestBid', default=None)

    @validator('pair')
    def norm_pair(cls, v):
        """ltc_brl -> LTC:BRL"""
        return v.upper().replace("_", ":")


class Exchange(BaseModel, SortedMixin):
    name = 'Braziliex'
    tickers: list[TikerBraziliex]

    @validator('tickers')
    def get_limit_tickers(cls, value):
        return cls.lim_sorted(value)

    @staticmethod
    def prepare_data(api):
        api = json.loads(api.decode("utf-8"))
        return {"tickers": list(api.values())}
