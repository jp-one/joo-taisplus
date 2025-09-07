import pytz
from odoo import models
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class PriceListItem(models.Model):
    _inherit = "taisplus.pricelist.item"

    def _evaluate_price_cap_exceedance(self, products, price_cap, currency, start_datetime_user_tz, end_datetime_user_tz_or_none):
        """
            オーバーライド：
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

        from_datetime = start_datetime_user_tz.astimezone(
            pytz.UTC).replace(tzinfo=None)
        to_datetime = end_datetime_user_tz_or_none.astimezone(
            pytz.UTC).replace(tzinfo=None) if end_datetime_user_tz_or_none else datetime.max
        company = self.env.company
        user_tz = pytz.timezone(self.env.user.tz or 'UTC')
        for p in products:
            product_service_model = self.env["taisplus_demo.product.service"]
            # 価格変動の日時を取得
            change_datetimes = product_service_model.get_list_price_change_datetimes(
                p.product_tmpl_id.id, p.id, from_datetime, to_datetime
            )
            # 変化点での価格リストアイテムを取得し、価格を評価(過去から)
            for dt in sorted(change_datetimes):
                pricelist_item = product_service_model.fetchone_product_pricelist_item(
                    p.product_tmpl_id.id, p.id, dt
                )
                if pricelist_item:
                    _logger.debug(
                        f"Product ID {p.id} at {dt}: {pricelist_item.fixed_price=}, {pricelist_item.currency_id.name=}")
                    price = pricelist_item.fixed_price if pricelist_item.fixed_price else 0.0
                    price_currency = pricelist_item.currency_id
                    if currency and price_currency and price_currency != currency:
                        # 通貨が異なる場合は、判定不能のため、Trueを返す
                        if _logger.isEnabledFor(logging.DEBUG):
                            _logger.error(
                                f"Currency mismatch: {currency=} vs {price_currency=}")
                        return (p, dt, price, price_cap)
                    if price_cap < price:
                        # 上限価格を超えている
                        return (p, dt, price, price_cap)
        return None
