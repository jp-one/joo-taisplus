from odoo import models, fields


class PriceList(models.Model):
    _name = "taisplus.pricelist"
    _description = "TAIS Code Price List (header)"

    name = fields.Char(
        string="貸与価格のリスト名",
        required=True,
    )
    tais_code_date = fields.Date(
        string="適用開始日",
        required=True,
    )
    filename = fields.Char(string="ファイル名")
    sheetname = fields.Char(string="シート名")
    notes = fields.Text(string="補足説明")

    item_ids = fields.One2many(
        comodel_name="taisplus.pricelist.item",
        inverse_name="pricelist_id",
        string="貸与価格",
    )

    _sql_constraints = [
        (
            "unique_tais_code_date",
            "UNIQUE(tais_code_date)",
            "The tais_code_date must be unique.",
        ),
    ]

    def get_pricelist_item_view(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Price List Details",
            "view_mode": "tree,form",
            "res_model": "taisplus.pricelist.item",
            "domain": [("pricelist_id", "=", self.id)],
            "context": {"default_pricelist_id": self.id},
        }
