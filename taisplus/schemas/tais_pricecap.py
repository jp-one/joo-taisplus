from datetime import date
from dataclasses import dataclass


@dataclass
class TaisPriceCapItemData:
    name: str
    date: date
    average_price: float
    price_cap: float
    currency: str


@dataclass
class TaisPriceCapData:
    tais_code: str
    target_date: date
    target: TaisPriceCapItemData
    future: TaisPriceCapItemData
