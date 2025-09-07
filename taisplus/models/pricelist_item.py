from odoo import api, models, fields
from datetime import date, datetime, time, timedelta
import pytz
import logging

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


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
        default=lambda self: self.env.ref(
            "base.JPY"),  # Default to Japanese Yen
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
        string="TAIS貸与価格リスト",
        required=True,
        ondelete="cascade",
    )

    tais_code_date = fields.Date(
        string="適用開始日",
        related="pricelist_id.tais_code_date",
        store=True,
    )

    related_product_template_ids = fields.One2many(
        comodel_name="product.template",
        inverse_name="id",
        string="プロダクト",
        compute="_compute_related_product_template_ids",
        store=False,  # 表示するたびに再計算
    )

    related_product_template_count = fields.Integer(
        string="プロダクト",    # wiget=statinfoで表示するため、ここは"プロダクト"のままにする
        compute="_compute_related_product_template_count",
        store=False,  # 表示するたびに再計算
    )

    related_product_product_ids = fields.One2many(
        comodel_name="product.product",
        inverse_name="id",
        string="バリアント",
        compute="_compute_related_product_product_ids",
        store=False,  # 表示するたびに再計算
    )

    related_product_product_count = fields.Integer(
        string="バリアント",    # wiget=statinfoで表示するため、ここは"バリアント"のままにする
        compute="_compute_related_product_product_count",
        store=False,  # 表示するたびに再計算
    )

    price_cap_exceeded = fields.Boolean(
        string="上限の超過",
        compute="_compute_price_cap_exceeded",
        store=False,  # 表示するたびに再計算
    )

    def _compute_pricelist_item_ids(self):
        for record in self:
            items = self.env["taisplus.pricelist.item"].search(
                [("tais_code", "=", record.tais_code)]
            )
            record.pricelist_item_ids = items

    def _compute_related_product_template_ids(self):
        for record in self:
            record.related_product_template_ids = self.env["product.template"].search(
                [("tais_code", "=", record.tais_code)]
            )

    @api.depends('related_product_template_ids')
    def _compute_related_product_template_count(self):
        for record in self:
            record.related_product_template_count = len(
                record.related_product_template_ids) if record.related_product_template_ids else 0

    def _compute_related_product_product_ids(self):
        for record in self:
            record.related_product_product_ids = self.env["product.product"].search(
                [("tais_code", "=", record.tais_code)]
            )

    @api.depends('related_product_product_ids')
    def _compute_related_product_product_count(self):
        for record in self:
            record.related_product_product_count = len(
                record.related_product_product_ids) if record.related_product_product_ids else 0

    def _get_next_tais_code_date_or_none(self):
        self.ensure_one()
        domain = [
            ('tais_code', '=', self.tais_code),
            ('tais_code_date', '>', self.tais_code_date)
        ]
        next_item = self.search(domain, order='tais_code_date asc', limit=1)
        return next_item.tais_code_date if next_item else None

    def _get_user_tz_midnight(self, date):
        naive_dt = datetime.combine(date, time(0, 0))
        user_tz = pytz.timezone(self.env.user.tz or 'UTC')
        localized_dt = user_tz.localize(naive_dt)
        return localized_dt

    def _compute_price_cap_exceeded(self):
        Product = self.env['product.product']
        for item in self:
            start_datetime_user_tz = self._get_user_tz_midnight(
                item.tais_code_date)
            next_date = item._get_next_tais_code_date_or_none()
            end_datetime_user_tz_or_none = self._get_user_tz_midnight(
                next_date) if next_date else None
            products = Product.search([('tais_code', '=', item.tais_code)])
            if _logger.isEnabledFor(logging.DEBUG):
                _logger.debug(
                    f"Evaluating {item.tais_code}: {start_datetime_user_tz} to {end_datetime_user_tz_or_none}, {products=}")
            exceeded = self._evaluate_price_cap_exceedance(
                products,
                item.price_cap,
                item.currency_id,
                start_datetime_user_tz,
                end_datetime_user_tz_or_none
            )
            if _logger.isEnabledFor(logging.DEBUG):
                if exceeded:
                    (p, dt, price, price_cap) = exceeded
                    if dt.tzinfo is None:
                        user_tz = pytz.timezone(self.env.user.tz or 'UTC')
                        dt = user_tz.localize(dt)
                    _logger.warning(
                        f"Price cap exceeded: {price_cap=} < {price=}, {dt=}, {p.display_name=}")
            item.price_cap_exceeded = True if exceeded else False

    def _evaluate_price_cap_exceedance(self, products, price_cap, currency, start_datetime_user_tz, end_datetime_user_tz_or_none):
        """
            仮想関数：
                製品の価格を対象期間で評価し、上限価格を超えているかを判定する。

            Args:
                products: 製品のレコードセット
                price_cap (float): 上限価格
                currency: 通貨
                start_datetime_user_tz (datetime): 評価開始日時
                end_datetime_user_tz_or_none (datetime?): 評価終了日時（この日時より前までを対象）またはNone（未来永劫）

            Returns:
                (procuct, datetime, float, float)?:
                    上限価格を超えている場合は、(製品レコード, 日時, 価格, 上限価格)タプル
                    そうでない場合はNone

        """
        _logger.warning("_evaluate_price_cap_exceedance() is not implemented.")
        return None

    def action_open_filtered_templates(self):
        self.ensure_one()
        if not self.related_product_template_count > 0:
            raise UserError("関連するプロダクトが存在しません。")
        return {
            'type': 'ir.actions.act_window',
            'name': f"[TAIS:{self.tais_code}]プロダクト",
            'res_model': 'product.template',
            'view_mode': 'tree,form',
            'domain': [('tais_code', '=', self.tais_code)],
            'context': {'search_default_tais_code': self.tais_code},
            'target': 'current',
        }

    def action_open_filtered_products(self):
        self.ensure_one()
        if not self.related_product_product_count > 0:
            raise UserError("関連するバリアントが存在しません。")
        return {
            'type': 'ir.actions.act_window',
            'name': f"[TAIS:{self.tais_code}]バリアント",
            'res_model': 'product.product',
            'view_mode': 'tree,form',
            'domain': [('tais_code', '=', self.tais_code)],
            'context': {'search_default_tais_code': self.tais_code},
            'target': 'current',
        }

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The name must be unique."),
        (
            "unique_tais_code_date_combination",
            "UNIQUE(tais_code, tais_code_date)",
            "The combination of TAIS Code and Effective Date must be unique.",
        ),
    ]
