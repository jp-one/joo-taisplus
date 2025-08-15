from odoo import models, fields


class PriceListItem(models.Model):
    _name = "taisplus.pricelist.item"
    _description = "TAIS Code Price List (detail)"
    _order = 'tais_code asc, tais_code_date desc'

    name = fields.Char(
        string="TAISコード:適用開始日",
        required=True,
    )

    tais_code = fields.Char(string="TAISコード", required=True, help="商品コード")
    product_name = fields.Char(string="商品名称")
    manufacturer = fields.Char(string="製造メーカー", help="法人名")
    model_number = fields.Char(string="型番")

    currency_id = fields.Many2one(
        "res.currency",
        string="通貨",
        default=lambda self: self.env.ref("base.JPY"),  # Default to Japanese Yen
        required=True,
    )
    average_price = fields.Monetary(
        string="全国平均貸与価格", currency_field="currency_id"
    )
    price_cap = fields.Monetary(
        string="貸与価格の上限", currency_field="currency_id", required=True
    )

    pricelist_id = fields.Many2one(
        comodel_name="taisplus.pricelist",
        string="貸与価格のリスト",
        required=True,
        ondelete="cascade",
    )

    tais_code_date = fields.Date(
        string="適用開始日",
        related="pricelist_id.tais_code_date",
        store=True,
        readonly=True,
    )

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The name must be unique."),
        (
            "unique_tais_code_date_combination",
            "UNIQUE(tais_code, tais_code_date)",
            "The combination of TAIS Code and Effective Date must be unique.",
        ),
    ]
