from odoo import models, fields


class PriceList(models.Model):
    _name = "taisplus.pricelist"
    _description = "TAIS Code Price List (header)"
    _order = 'tais_code_date desc'

    name = fields.Char(
        string="リスト名",
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
        string="TAIS貸与価格",
    )

    # 注意： 処理コストが高いため、利用には注意が必要
    exceeded_item_ids = fields.One2many(
        comodel_name="taisplus.pricelist.item",
        inverse_name="pricelist_id",
        string="上限超過",
        compute="_compute_exceeded_items",
        store=False,
    )

    def _compute_exceeded_items(self):
        for record in self:
            record.exceeded_item_ids = record.item_ids.filtered(
                lambda item: item.price_cap_exceeded)

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
