# -*- coding: utf-8 -*-
{
    "name": "福祉用具(TAIS+)",
    "version": "16.0.1.0.0",
    "author": "jp-one",
    "license": "LGPL-3",
    "maintainer": "jp-one",
    "website": "https://github.com/jp-one/joo-taisplus",
    "summary": """
        (デモ・アプリ)福祉用具情報システム(TAIS)を活用し、貸与・販売する福祉用具商品を管理する
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
    "application": True,
    "images": ["static/description/icon.png"],
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "product",
        "taisplus",
    ],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "views/views.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        # 'demo/demo.xml',
    ],
}
