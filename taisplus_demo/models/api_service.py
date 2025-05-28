from odoo import api, models
from dataclasses import asdict
from datetime import date, datetime
import json
from .product_service import ProductService


class ApiService(models.AbstractModel):
    _inherit = "taisplus.api.service"

    @api.model
    def get_aid_product_json(self, default_code: str, date_string: str):
        """
        Returns aid product information as a JSON string.

        Args:
            default_code (str): The internal reference code of the product.
            date_string (str): The target date and time in ISO format (e.g., '2024-05-25T12:00:00').
                You can also specify only the date (e.g., '2024-05-25'). In this case, the time will be set to 00:00:00.

        Returns:
            str: A JSON string containing product details, sales price, purchase price, and TAIS price cap.
        """
        productService = self.env[
            "taisplus_demo.product.service"
        ]  # type: ProductService
        local_datetime = self._fromisoformat_to_local(date_string)
        aidProductData = productService.get_aid_product(default_code, local_datetime)
        return json.dumps(asdict(aidProductData), default=self.date_serializer)
