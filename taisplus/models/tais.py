import base64
import requests
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class Tais(models.Model):
    _name = "taisplus.tais"
    _description = "TAIS Code"

    _sql_constraints = [
        ("tais_code", "UNIQUE(tais_code)", "The tais_code must be unique!")
    ]

    name = fields.Char(string="商品名", required=True)
    tais_code = fields.Char(
        string="TAISコード",
        required=True,
        help="TAISコードは、企業コード(5桁)と福祉用具コード(6桁)で構成されています。",
    )
    ccta95_id = fields.Many2one(
        "taisplus.ccta95",
        string="分類項目",
        help="福祉用具は、分類コード(CCTA95)で分類されています。",
    )
    model_number = fields.Char(string="型番")
    manufacturer = fields.Char(string="製造メーカー")

    RENTAL_SERVICE_SELECTION = [
        ("R00", "--:（非貸与）"),
        ("R01", "01: 車いす"),
        ("R02", "02: 車いす付属品"),
        ("R03", "03: 特殊寝台"),
        ("R04", "04: 特殊寝台付属品"),
        ("R05", "05: 床ずれ防止用具"),
        ("R06", "06: 体位変換器"),
        ("R07", "07: 手すり"),
        ("R08", "08: スロープ"),
        ("R09", "09: 歩行器"),
        ("R10", "10: 歩行補助つえ"),
        ("R11", "11: 認知症老人徘徊感知機器"),
        ("R12", "12: 移動用リフト"),
        ("R13", "13: 自動排泄処理装置"),
    ]
    SALES_SERVICE_SELECTION = [
        ("S00", "--:（非購入）"),
        ("S01", "01: 腰掛便座"),
        ("S02", "02: 自動排泄処理装置の交換可能部品"),
        ("S03", "03: 排泄予測支援機器"),
        ("S04", "04: 入浴補助用具"),
        ("S05", "05: 簡易浴槽"),
        ("S06", "06: 移動用リフトのつり具の部分"),
        ("S07", "07: スロープ"),
        ("S08", "08: 歩行器"),
        ("S09", "09: 歩行補助つえ"),
    ]

    rental_service = fields.Selection(
        selection=RENTAL_SERVICE_SELECTION,
        string="貸与サービス種目",
        required=True,
        help="福祉用具貸与サービス種目です。",
    )
    sales_service = fields.Selection(
        selection=SALES_SERVICE_SELECTION,
        string="販売サービス種目",
        required=True,
        help="福祉用具販売サービス種目です。",
    )
    image_url = fields.Char(string="画像リンク", help="商品に関連する画像のURLです。")
    tais_url = fields.Char(string="TAIS URL", help="福祉用具情報システムのURLです。")
    image = fields.Binary(string="Image", compute="_compute_image_url")
    product_summary = fields.Text(string="製品概要")
    is_discontinued = fields.Boolean(string="生産終了", default=False)

    pricelist_item_ids = fields.One2many(
        comodel_name="taisplus.pricelist.item",
        inverse_name="id",
        string="価格リスト",
        compute="_compute_pricelist_item_ids",
        store=False,
    )

    related_product_template_ids = fields.One2many(
        comodel_name="product.template",
        inverse_name="id",
        string="関連プロダクト",
        compute="_compute_related_product_template_ids",
        store=False,
    )

    @api.depends("image_url")
    def _compute_image_url(self):
        for record in self:
            record.image = False
            if record.image_url:
                try:
                    response = requests.get(record.image_url, timeout=10)
                    response.raise_for_status()
                    record.image = base64.b64encode(response.content)
                except requests.RequestException as e:
                    _logger.error(
                        f"Failed to fetch image from URL {record.image_url}: {e}"
                    )

    @api.depends("pricelist_item_ids")
    def _compute_pricelist_item_ids(self):
        for record in self:
            items = self.env["taisplus.pricelist.item"].search(
                [("tais_code", "=", record.tais_code)]
            )
            record.pricelist_item_ids = items

    @api.depends("related_product_template_ids")
    def _compute_related_product_template_ids(self):
        for record in self:
            products = self.env["product.product"].search(
                [("tais_code", "=", record.tais_code)]
            )
            template_ids = products.mapped("product_tmpl_id").ids
            templates = self.env["product.template"].browse(template_ids)
            record.related_product_template_ids = templates

    def name_get(self):
        return [(record.id, f"[{record.tais_code}] {record.name}") for record in self]
