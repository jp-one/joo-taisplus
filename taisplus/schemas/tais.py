from dataclasses import dataclass


@dataclass
class TaisData:
    tais_code: str
    tais_url: str
    ccta95_code: str
    product_name: str
    model_number: str
    manufacturer: str
    rental_service_code: str
    rental_service_name: str
    sales_service_code: str
    sales_service_name: str
    product_summary: str
    image_url: str
    is_discontinued: bool
