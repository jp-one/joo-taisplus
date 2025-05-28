from odoo import api, models
from dataclasses import asdict
from datetime import date, datetime
import json
import pytz
from .pricelist_service import PriceListService
from .tais_service import TaisService
from ..schemas.product import ProductData


class ApiService(models.AbstractModel):
    _name = "taisplus.api.service"
    _description = "TAISPLUS API Service"

    @staticmethod
    def date_serializer(obj):
        """Custom serializer for date objects."""
        if isinstance(obj, date):
            return obj.isoformat()
        return obj  # Return the object as-is if it's not serializable

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

    @api.model
    def fetch_tais_product_json(self, tais_code):
        """
        Retrieve product information for the specified TAIS code and return it as JSON.

        Args:
            tais_code (str): TAIS code in the format '01234-012345'

        Returns:
            str: JSON string of product information
        """
        taisService = self.env["taisplus.tais.service"]  # type: TaisService
        tais_url = taisService.generate_tais_url(tais_code)
        try:
            taisData = taisService.fetch_tais_product_details(tais_url)
        except Exception as e:
            raise RuntimeError(
                f"Failed to fetch TAIS product information: {e} (URL: {tais_url})"
            )
        if taisData.tais_code != tais_code:
            raise ValueError(
                f"TAIS code mismatch. Expected: '{tais_code}', got: '{taisData.tais_code}'."
            )
        return json.dumps(asdict(taisData))

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
        priceListService = self.env[
            "taisplus.pricelist.service"
        ]  # type: PriceListService
        target_date = self._fromisoformat_to_local(date_string).date()
        taisPriceCapData = priceListService.get_tais_price_cap(tais_code, target_date)
        return json.dumps(asdict(taisPriceCapData), default=self.date_serializer)

    def _get_tais_product_by_default_code(self, default_code: str):
        # default_code (Internal Reference)
        product_product = self.env["product.product"]
        product = product_product.search(
            [
                ("default_code", "=", default_code),
                ("product_tmpl_id.detailed_type", "=", "tais_product"),
            ],
            limit=1,
        )

        if not product:
            raise ValueError(f"Product with default_code '{default_code}' not found.")

        # Get product name in user's language
        user_lang = self.env.user.lang or "en_US"
        product_name = product.with_context(lang=user_lang).name

        return ProductData(
            default_code=default_code,
            product_name=product_name,
            tais_code=product.tais_code,
        )

    @api.model
    def get_tais_product_json(self, default_code: str):
        """
        Returns tais product information as a JSON string.

        Args:
            default_code (str): The internal reference code of the product.

        Returns:
            str: A JSON string containing product details.
        """
        productData = self._get_tais_product_by_default_code(default_code)
        return json.dumps(asdict(productData))
