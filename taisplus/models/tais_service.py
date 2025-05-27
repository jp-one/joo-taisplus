from odoo import api, models
from bs4 import BeautifulSoup
import re
import requests
from ..schemas.tais import TaisData


class TaisService(models.AbstractModel):
    _name = "taisplus.tais.service"
    _description = "TAIS Code"

    _BASE_URL_TAIS = "https://www.techno-tais.jp/"

    @api.model
    def generate_tais_url(self, tais_code):
        if not tais_code:
            raise ValueError(
                "TAIS code is required. Please provide it in the format '01234-012345'."
            )
        parts = tais_code.split("-")
        if len(parts) != 2:
            raise ValueError(
                f"Invalid TAIS code format: '{tais_code}'. Expected format is '01234-012345'."
            )
        base_url = self._BASE_URL_TAIS + "ServiceWelfareGoodsDetail.php"
        tais_url = f"{base_url}?RowNo=0&YouguCode1={parts[0]}&YouguCode2={parts[1]}"
        return tais_url

    _name_to_code_rental = {
        "車いす": "01",
        "車いす付属品": "02",
        "特殊寝台": "03",
        "特殊寝台付属品": "04",
        "床ずれ防止用具": "05",
        "体位変換器": "06",
        "手すり": "07",
        "スロープ": "08",
        "歩行器": "09",
        "歩行補助つえ": "10",
        "認知症老人徘徊感知機器": "11",
        "移動用リフト": "12",
        "自動排泄処理装置": "13",
    }

    def _get_rental_service_code(self, name):
        return self._name_to_code_rental.get(name, "00")

    _name_to_code_sales = {
        "腰掛便座": "01",
        "自動排泄処理装置の交換可能部品": "02",
        "排泄予測支援機器": "03",
        "入浴補助用具": "04",
        "簡易浴槽": "05",
        "移動用リフトのつり具の部分": "06",
        "スロープ": "07",
        "歩行器": "08",
        "歩行補助つえ": "09",
    }

    def _get_sales_service_code(self, name):
        return self._name_to_code_sales.get(name, "00")

    @api.model
    def fetch_tais_product_details(self, tais_url: str):
        # Access TAIS and parse HTML with BeautifulSoup
        response = requests.get(tais_url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # Narrow the scope to the main tag
        main_tag = soup.find("main")
        if not main_tag:
            raise ValueError("The main tag was not found.")

        section = main_tag.find("section", class_="p-welfareDetail1")
        if not section:
            raise ValueError("The section tag was not found.")

        div_left = main_tag.find("div", class_="p-welfareDetail1__left")
        if not div_left:
            raise ValueError("The div (p-welfareDetail1__left) tag was not found.")

        div_right = main_tag.find("div", class_="p-welfareDetail1__right")
        if not div_right:
            raise ValueError("The div (p-welfareDetail1__right) tag was not found.")

        # Rental category - rental_service_name, rental_service_code
        rental_service_name = None
        rental_service_name_dt = div_left.find("dt", string="貸与")
        if rental_service_name_dt:
            rental_service_name_item = getattr(
                rental_service_name_dt.find_next("dd"), "text", None
            )
            rental_service_name = (
                rental_service_name_item.strip() if rental_service_name_item else None
            )
        rental_service_code = self._get_rental_service_code(rental_service_name)

        # Sales category - sales_service_name, sales_service_code
        sales_service_name = None
        sales_service_name_dt = div_left.find("dt", string="購入")
        if sales_service_name_dt:
            sales_service_name_item = getattr(
                sales_service_name_dt.find_next("dd"), "text", None
            )
            sales_service_name = (
                sales_service_name_item.strip() if sales_service_name_item else None
            )
        sales_service_code = self._get_sales_service_code(sales_service_name)

        # Manufacturer/Product name/model
        manufacturer = None
        product_name = None
        model_number = None
        product_div = div_left.find("div", class_="c-block2__head")
        if product_div:
            manufacturer_item = getattr(product_div.find("p"), "text", None)
            manufacturer = manufacturer_item.strip() if manufacturer_item else None
            prudoct_h3 = product_div.find("h3")
            if prudoct_h3:
                product_name_item = getattr(prudoct_h3, "text", None)
                product_name = product_name_item.strip() if product_name_item else None
                model_number_item = getattr(prudoct_h3.find_next("p"), "text", None)
                model_number = model_number_item.strip() if model_number_item else None

        # TAIS code
        tais_code = None
        tais_code_dt = div_left.find("dt", string="TAISコード")
        if tais_code_dt:
            tais_code_dd = tais_code_dt.find_next("dd")
            if tais_code_dd:
                tais_code_span = tais_code_dd.find("span")
                if tais_code_span:
                    tais_code_item = getattr(tais_code_span, "text", None)
                    tais_code = (
                        tais_code_item.replace(" ", "").strip()
                        if tais_code_item
                        else None
                    )

        # Classification code - ccta95_code
        ccta95_code = None
        ccta95_code_dt = div_left.find("dt", string="分類コード")
        if ccta95_code_dt:
            ccta95_code_dd = ccta95_code_dt.find_next("dd")
            if ccta95_code_dd:
                ccta95_code_p = ccta95_code_dd.find("p")
                if ccta95_code_p:
                    ccta95_code_item = getattr(ccta95_code_p, "text", None)
                    if ccta95_code_item:
                        match = re.search(r"\[(\d+)](\d+):", ccta95_code_item)
                        ccta95_code = match.group(2) if match else None

        # Product summary
        product_summary = None
        product_summary_dt = div_left.find("dt", string="製品概要")
        if product_summary_dt:
            product_summary_dd = product_summary_dt.find_next("dd")
            if product_summary_dd:
                product_summary_item = getattr(
                    product_summary_dd.find("p"), "text", None
                )
                product_summary = (
                    product_summary_item.strip() if product_summary_item else None
                )

        # Image URL
        image_url_img = div_right.find("img")
        image_url = (
            self._BASE_URL_TAIS + image_url_img["src"].lstrip("./")
            if image_url_img and "src" in image_url_img.attrs
            else None
        )

        # Check if the product is discontinued
        discontinued_tag = div_right.find("p", string="生産終了")
        is_discontinued = discontinued_tag is not None

        return TaisData(
            tais_code=tais_code,
            tais_url=tais_url,
            ccta95_code=ccta95_code,
            product_name=product_name,
            model_number=model_number,
            manufacturer=manufacturer,
            rental_service_code=rental_service_code,
            rental_service_name=rental_service_name,
            sales_service_code=sales_service_code,
            sales_service_name=sales_service_name,
            product_summary=product_summary,
            image_url=image_url,
            is_discontinued=is_discontinued,
        )
