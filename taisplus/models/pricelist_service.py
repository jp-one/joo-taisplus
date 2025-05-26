from odoo import api, models
from datetime import date, datetime
from typing import Optional
from dataclasses import asdict
import json
import pytz
from ..schemas.tais_pricecap import TaisPriceCapData, TaisPriceCapItemData
from .pricelist_item import PriceListItem


def date_serializer(obj):
    """Custom serializer for date objects."""
    if isinstance(obj, date):
        return obj.isoformat()
    return obj  # Return the object as-is if it's not serializable


class PriceListService(models.AbstractModel):
    _name = "taisplus.pricelist.service"
    _description = "TAIS Code Price List Service"

    def _fromisoformat_to_local(self, date_string: str) -> datetime:
        """
        Convert an ISO format date string to a datetime object in the user's local timezone.
        """
        user_timezone = pytz.timezone(self.env.user.tz)
        dt_parsed = datetime.fromisoformat(date_string)
        if dt_parsed.tzinfo is None:
            dt_local = user_timezone.localize(dt_parsed)
        else:
            dt_local = dt_parsed.astimezone(user_timezone)
        return dt_local

    def get_tais_price_cap(
        self,
        tais_code: str,
        target_date: date,
    ) -> TaisPriceCapData:
        target = self._get_tais_price_cap_item(tais_code, target_date, is_future=False)
        future = self._get_tais_price_cap_item(tais_code, target_date, is_future=True)
        selected = self._select_target_or_future(target, future)
        return TaisPriceCapData(
            tais_code=tais_code or None,
            target_date=target_date,
            target=target,
            future=selected,
        )

    def _get_tais_price_cap_item(
        self,
        tais_code: str,
        target_date: date,
        is_future: bool = False,
    ) -> Optional[TaisPriceCapItemData]:
        priceListItem = self.env["taisplus.pricelist.item"]  # type: PriceListItem
        domain = [
            ("tais_code", "=", tais_code),
            (
                ("tais_code_date", ">", target_date)
                if is_future
                else ("tais_code_date", "<=", target_date)
            ),
        ]
        order = "price_cap asc" if is_future else "tais_code_date desc"
        record = priceListItem.search(domain, order=order, limit=1)
        if not record:
            return None
        return TaisPriceCapItemData(
            name=record.pricelist_id.name,
            date=record.tais_code_date,
            average_price=record.average_price,
            price_cap=record.price_cap,
            currency=record.currency_id.name,
        )

    def _select_target_or_future(
        self,
        target: Optional[TaisPriceCapItemData],
        future: Optional[TaisPriceCapItemData],
    ) -> Optional[TaisPriceCapItemData]:
        if not future:
            return target
        if not target:
            return future
        return future if target.price_cap > future.price_cap else target

    @api.model
    def get_tais_price_cap_json(self, tais_code: str, date_string: str):
        """
        Get TAIS price cap data as a JSON string.

        Args:
            tais_code (str): The TAIS code for which to retrieve price cap data.
            date_string (str): The target date and time in ISO format (e.g., '2024-05-25T12:00:00').
                You can also specify only the date (e.g., '2024-05-25'). In this case, the time will be set to 00:00:00.

        Returns:
            str: A JSON string representing the TAIS price cap data for the given code and date.
        """
        target_date = self._fromisoformat_to_local(date_string).date()
        taisPriceCapData = self.get_tais_price_cap(tais_code, target_date)
        return json.dumps(asdict(taisPriceCapData), default=date_serializer)
