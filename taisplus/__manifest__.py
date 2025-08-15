# -*- coding: utf-8 -*-
{
    "name": "TAIS+",
    "version": "16.0.2.2",
    "author": "jp-one",
    "license": "LGPL-3",
    "website": "https://jp-one.github.io/joo-taisplus/",
    "summary": """
        福祉用具情報システム(TAIS)を活用し、貸与・販売する福祉用具商品を管理する
    """,
    "description": """
        福祉用具情報システム(TAIS)は、国内の福祉用具製造事業者や輸入事業者から
        「企業」および「福祉用具」情報を収集し、全国に散在する福祉用具に関する情報を
        分類・体系化して提供するシステムです。本モジュールは、TAISを活用して、
        利用者や介護者の状態に即した適切な福祉用具の選定および利用を支援します。
        また、介護テクノロジーを含む9分野16項目の機器等に関する情報も取り扱います。
    """,
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Sales",
    "application": False,
    "images": ["static/description/icon.png"],
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "product",
    ],
    "external_dependencies": {
        "python": ["openpyxl"],
    },
    # always loaded
    "data": [
        "data/taisplus.ccta95.csv",
        "security/ir.model.access.csv",
        "views/ccta95_views.xml",
        "views/price_list_import_views.xml",
        "views/price_list_views.xml",
        "views/product_product_views.xml",
        "views/product_template_views.xml",
        "views/tais_import_views.xml",
        "views/tais_views.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        # 'demo/demo.xml',
    ],
}
