from pydantic import BaseModel, Field, validator
from .mixin import SortedMixin
import json


class TickerKraken(BaseModel):
    pair: str = Field(alias='pair', default=None)
    ask: float = Field(alias='ask', default=None)
    bid: float = Field(alias='bid', default=None)


class Exchange(BaseModel, SortedMixin):
    name = 'Kraken'
    tickers: list[TickerKraken]

    @validator('tickers')
    def get_limit_tickers(cls, value):
        return cls.lim_sorted(value)

    @staticmethod
    def prepare_data(api):
        return json.loads(api.decode("utf-8"))
