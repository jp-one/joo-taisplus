from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    tais_code = fields.Char(string="TAISコード")

    pricelist_item_ids = fields.One2many(
        comodel_name="taisplus.pricelist.item",
        inverse_name="id",  # dummy. not actually used.
        string="TAIS貸与価格明細",
        compute="_compute_pricelist_item_ids",
        store=False,
    )

    def _compute_pricelist_item_ids(self):
        for product in self:
            if product.tais_code:
                items = self.env["taisplus.pricelist.item"].search(
                    [("tais_code", "=", product.tais_code)]
                )
                product.pricelist_item_ids = items
            else:
                product.pricelist_item_ids = self.env["taisplus.pricelist.item"]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    detailed_type = fields.Selection(
        selection_add=[
            ("tais_product", "福祉用具(TAIS)"),
        ],
        ondelete={"tais_product": "set consu"},
    )

    def _detailed_type_mapping(self):
        type_mapping = super()._detailed_type_mapping()
        type_mapping["tais_product"] = "consu"
        return type_mapping

    @api.depends("detailed_type")
    def _compute_product_tooltip(self):
        super()._compute_product_tooltip()
        for record in self:
            if record.detailed_type == "tais_product":
                record.product_tooltip = _(
                    "福祉用具商品です。販売もしくは貸与が可能です。"
                )

    # The implementation of 'tais_code' is inspired by the 'barcode' field.
    tais_code = fields.Char(
        string="TAISコード",
        compute="_compute_tais_code",
        inverse="_set_tais_code",
        search="_search_tais_code",
    )

    # related to display product product information if is_product_variant
    def _get_related_fields_variant_template(self):
        """Return a list of fields present on template and variants models and that are related"""
        related_fields = super(
            ProductTemplate, self
        )._get_related_fields_variant_template()
        related_fields += ["tais_code"]
        return related_fields

    @api.depends("product_variant_ids.tais_code")
    def _compute_tais_code(self):
        self.tais_code = False
        for template in self:
            # TODO master: update product_variant_count depends and use it instead
            variant_count = len(template.product_variant_ids)
            if variant_count == 1:
                template.tais_code = template.product_variant_ids.tais_code
            elif variant_count == 0:
                archived_variants = template.with_context(
                    active_test=False
                ).product_variant_ids
                if len(archived_variants) == 1:
                    template.tais_code = archived_variants.tais_code

    def _search_tais_code(self, operator, value):
        query = self.with_context(active_test=False)._search(
            [("product_variant_ids.tais_code", operator, value)]
        )
        return [("id", "in", query)]

    def _set_tais_code(self):
        variant_count = len(self.product_variant_ids)
        if variant_count == 1:
            self.product_variant_ids.tais_code = self.tais_code
        elif variant_count == 0:
            archived_variants = self.with_context(active_test=False).product_variant_ids
            if len(archived_variants) == 1:
                archived_variants.tais_code = self.tais_code

    pricelist_item_ids = fields.One2many(
        comodel_name="taisplus.pricelist.item",
        inverse_name="id",  # dummy. not actually used.
        string="TAIS貸与価格明細",
        compute="_compute_pricelist_item_ids",
        store=False,
    )

    def _compute_pricelist_item_ids(self):
        for template in self:
            tais_codes = [
                v.tais_code for v in template.product_variant_ids if v.tais_code
            ]
            if tais_codes:
                items = self.env["taisplus.pricelist.item"].search(
                    [("tais_code", "in", tais_codes)]
                )
            else:
                items = self.env["taisplus.pricelist.item"]
            template.pricelist_item_ids = items
