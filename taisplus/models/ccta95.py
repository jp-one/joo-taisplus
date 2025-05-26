from odoo import models, fields


class Ccta95(models.Model):
    _name = "taisplus.ccta95"
    _description = "分類コード(CCTA95)"

    hierarchy_level = fields.Selection(
        [("major", "大分類"), ("middle", "中分類"), ("minor", "小分類")],
        string="分類階層",
        required=True,
    )
    ccta95_code = fields.Char(
        string="分類コード",
        required=True,
        help="TAISに登録された福祉用具には、「分類コード(CCTA95)」が付番されます。",
    )
    name = fields.Char(string="分類項目")
    name_en = fields.Char(string="分類項目(EN)")
    description = fields.Text(string="解説")
    is_marked = fields.Boolean(
        string="(*)",
        default=False,
        help="分類コードに(*)が付与されている分類項目です。",
    )

    _sql_constraints = [
        ("ccta95_code", "UNIQUE(ccta95_code)", "The ccta95_code must be unique!"),
    ]

    def name_get(self):
        return [(record.id, f"[{record.ccta95_code}] {record.name}") for record in self]
