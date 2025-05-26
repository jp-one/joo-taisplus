from dataclasses import dataclass
from datetime import date, datetime
from typing import Any


@dataclass
class AidPriceData:
    target_datetime: datetime
    price: float
    currency: str
    datetime_start: datetime
    datetime_end: datetime


@dataclass
class AidVenderPriceData:
    target_date: date
    price: float
    currency: str
    date_start: date
    date_end: date
    vendor_name: str
    vendor_product_code: str
    vendor_product_name: str


@dataclass
class AidProductData:
    default_code: str
    product_name: str
    sales_price: AidPriceData
    purchase_price: AidVenderPriceData
    tais_pricecap: Any  # TaisPriceCapData
