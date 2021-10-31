
import requests
from MSApi.MSLowApi import MSLowApi, error_handler, caching

from MSApi.Meta import Meta
from MSApi.Organization import Organization, Account
from MSApi.Template import Template
from MSApi.Product import Product
from MSApi.Service import Service
from MSApi.ProductFolder import ProductFolder
from MSApi.Discount import Discount, SpecialPriceDiscount, AccumulationDiscount
from MSApi.PriceType import PriceType
from MSApi.CompanySettings import CompanySettings
from MSApi.Bundle import Bundle
from MSApi.Variant import Variant
from MSApi.Employee import Employee
from MSApi.documents.CustomerOrder import CustomerOrder

from MSApi.exceptions import *


class MSApi(MSLowApi):

    __objects_dict = {
        'product': Product,
        'organization': Organization,
        'template': Template,
        'productfolder': ProductFolder,
        'discount': Discount,
        'specialpricediscount': SpecialPriceDiscount,
        'accumulationdiscount': AccumulationDiscount,
        'service': Service,
        'companysettings': CompanySettings,
        'bundle': Bundle,
        'variant': Variant,
        'employee': Employee,
        'account': Account,
        'customerorder': CustomerOrder

    }

    @classmethod
    def get_company_settings(cls) -> CompanySettings:
        """Запрос на получение Настроек компании."""
        response = cls.auch_get('context/companysettings')
        error_handler(response)
        return CompanySettings(response.json())

    @classmethod
    def get_default_price_type(cls) -> PriceType:
        """Получить тип цены по умолчанию"""
        response = cls.auch_get('context/companysettings/pricetype/default')
        error_handler(response)
        return PriceType(response.json())

    @classmethod
    def get_object_by_meta(cls, meta: Meta):
        obj_type = cls.__objects_dict.get(meta.get_type())
        if obj_type is None:
            raise MSApiException(f"Unknown object type \"{meta.get_type()}\"")
        response = cls._auch_get_by_href(meta.get_href())
        error_handler(response)
        return obj_type(response.json())

    @classmethod
    def get_object_by_json(cls, json_data):
        meta = Meta(json_data.get('meta'))
        obj_type = cls.__objects_dict.get(meta.get_type())
        if obj_type is None:
            raise MSApiException(f"Unknown object type \"{meta.get_type()}\"")
        return obj_type(json_data)

    @classmethod
    def get_object_by_href(cls, href):
        response = cls._auch_get_by_href(href)
        error_handler(response)
        return cls.get_object_by_json(response.json())

    @classmethod
    @caching
    def gen_organizations(cls, **kwargs):
        return cls.gen_objects('entity/organization', Organization, **kwargs)

    @classmethod
    @caching
    def gen_variants(cls, **kwargs):
        return cls.gen_objects('entity/variant', Variant, **kwargs)

    @classmethod
    @caching
    def gen_services(cls, **kwargs):
        return cls.gen_objects('entity/service', Service, **kwargs)

    @classmethod
    @caching
    def gen_bundles(cls, **kwargs):
        return cls.gen_objects('entity/bundle', Bundle, **kwargs)

    @classmethod
    @caching
    def gen_assortment(cls, **kwargs):
        return cls.gen_objects('entity/assortment', lambda row_json: cls.get_object_by_json(row_json), **kwargs)

    @classmethod
    @caching
    def gen_customtemplates(cls, **kwargs):
        return cls.gen_objects('entity/assortment/metadata/customtemplate', Template, **kwargs)

    @classmethod
    @caching
    def gen_products(cls, **kwargs):
        return cls.gen_objects('entity/product', Product, **kwargs)

    @classmethod
    @caching
    def gen_productfolders(cls, **kwargs):
        return cls.gen_objects('entity/productfolder', ProductFolder, **kwargs)

    @classmethod
    @caching
    def gen_discounts(cls, **kwargs):
        return cls.gen_objects('entity/discount', Discount, **kwargs)

    @classmethod
    @caching
    def gen_special_price_discounts(cls, **kwargs):
        return cls.gen_objects('entity/specialpricediscount', SpecialPriceDiscount, **kwargs)

    @classmethod
    @caching
    def gen_accumulation_discounts(cls, **kwargs):
        return cls.gen_objects('entity/accumulationdiscount', AccumulationDiscount, **kwargs)

    @classmethod
    @caching
    def gen_customer_orders(cls, **kwargs):
        return cls.gen_objects('entity/customerorder', CustomerOrder, **kwargs)

    @classmethod
    def get_product_by_id(cls, product_id, **kwargs):
        response = cls.auch_get(f'entity/product/{product_id}', **kwargs)
        error_handler(response)
        return Product(response.json())

    @classmethod
    def set_products(cls, json_data):
        response = cls.auch_post(f'entity/product/', json=json_data)
        error_handler(response)

    @classmethod
    def load_label(cls, product: Product, organization: Organization, template: Template, sale_price=None, **kwargs):

        if not sale_price:
            sale_price = next(product.gen_sale_prices(), None)
            if not sale_price:
                raise MSApiException(f"Sale prices is empty in {product}")

        request_json = {
            'organization': {
                'meta': organization.get_meta().get_json()
            },
            'count': 1,
            'salePrice': sale_price.get_json(),
            'template': {
                'meta': template.get_meta().get_json()
            }

        }

        response = cls.auch_post(f"/entity/product/{product.get_id()}/export", json=request_json, **kwargs)
        if response.status_code == 303:
            url = response.json().get('Location')
            file_response = requests.get(url)
            data = file_response.content
        elif response.status_code == 200:
            data = response.content
        else:
            raise MSApiHttpException(response)

        return data
