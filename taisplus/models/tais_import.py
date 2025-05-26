from odoo import models, fields, api
from .tais_service import TaisService
from .tais import Tais
from .ccta95 import Ccta95
import logging

_logger = logging.getLogger(__name__)


class TaisImport(models.TransientModel):
    _name = "taisplus.tais.import"
    _description = "Import TAIS Codes"

    tais_codes = fields.Text(
        string="TAISコード(複数可)",
        required=True,
        help="複数のTAISコードを改行で区切って入力してください",
    )

    @api.model
    def fetch_tais_data(self, tais_code):
        tais_service_model = self.env["taisplus.tais.service"]  # type: TaisService
        tais_url = tais_service_model.generate_tais_url(tais_code)
        return tais_service_model.fetch_tais_product_details(tais_url)

    def import_tais_codes(self):
        """Import TAIS codes from the entered text."""
        tais_model = self.env["taisplus.tais"].sudo()  # type: Tais

        if not self.tais_codes:
            raise ValueError("No TAIS codes provided.")

        tais_code_list = [
            code.strip() for code in self.tais_codes.splitlines() if code.strip()
        ]

        for tais_code in tais_code_list:
            try:
                data = self.fetch_tais_data(tais_code)
                # ccta95_id
                ccta95 = self.env["taisplus.ccta95"].search(
                    [("ccta95_code", "=", data.ccta95_code)], limit=1
                )  # type: Ccta95
                record_vals = {
                    "name": data.product_name,
                    "tais_code": tais_code,
                    "ccta95_id": ccta95.id if ccta95 else None,
                    "model_number": data.model_number,
                    "manufacturer": data.manufacturer,
                    "rental_service": "R" + data.rental_service_code,
                    "sales_service": "S" + data.sales_service_code,
                    "image_url": data.image_url,
                    "product_summary": data.product_summary,
                    "is_discontinued": data.is_discontinued,
                    "tais_url": data.tais_url,
                }
                filtered_vals = {k: v for k, v in record_vals.items() if v is not None}

                existing_record = tais_model.search(
                    [("tais_code", "=", tais_code)], limit=1
                )
                if existing_record:
                    existing_record.write(filtered_vals)
                else:
                    tais_model.create(filtered_vals)
            except Exception as e:
                _logger.error(f"Error importing TAIS code {tais_code}: {e}")
