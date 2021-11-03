from base import DataStreamControllerBase
from provider import Provider

CRON_TYPE = "day"

TEMPLATE_SHOPIFY_CUSTOMER_REPORT = {
    "schedules": [
        {
            "cron_type": CRON_TYPE,
            "cron_interval": 1,
            "cron_interval_start": 1,
            "cron_start_of_day": "04:00:00",
            "time_range_preset": 13,
            "offset_days": 0
        }
    ],
    "report_type": 3,
    "fields": [
        "shop_id",
        "shop_name",
        "shop_timezone",
        "created_at",
        "currency",
        "email",
        "first_name",
        "id",
        "last_name",
        "phone",
        "updated_at",
        "default_address.address1",
        "default_address.address2",
        "default_address.city",
        "default_address.country_code",
        "default_address.country_name",
        "default_address.customer_id",
        "default_address.first_name",
        "default_address.last_name",
        "default_address.name",
        "default_address.phone",
        "default_address.province",
        "default_address.province_code",
        "default_address.zip"
    ],
    "extract_name_keys": "null",
    "manage_extract_names": "false",
    "overwrite_datastream": "true",
    "overwrite_date_range_column_name": "null",
    "overwrite_key_columns": "false",
    "overwrite_filename": "false"
}


TEMPLATE_SHOPIFY_LINE_TIME_REPORT = {
    "schedules": [
        {
            "cron_type": CRON_TYPE,
            "cron_interval": 1,
            "cron_interval_start": 1,
            "cron_start_of_day": "04:00:00",
            "time_range_preset": 2,
            "offset_days": 0
        }
    ],
    "report_type": 4,
    "fields": [
        "shop_id",
        "shop_name",
        "shop_timezone",
        "name",
        "price",
        "product_id",
        "quantity",
        "sku",
        "total_discount",
        "order.subtotal_price",
        "order.closed_at",
        "order.cancelled_at",
        "order.currency",
        "order.total_price",
        "order.created_at",
        "order.test",
        "order.total_discounts",
        "order.location_id",
        "order.total_line_items_price",
        "order.number",
        "order.email",
        "order.updated_at",
        "order.id",
        "order.order_number",
        "order.processed_at",
        "order.total_tax",
        "shipping_address.city",
        "shipping_address.country",
        "shipping_address.province",
        "shipping_address.zip",
        "shipping_address.country_code",
        "shipping_address.province_code"
    ],
    "extract_name_keys": "null",
    "manage_extract_names": "false",
    "overwrite_datastream": "true",
    "overwrite_date_range_column_name": "null",
    "overwrite_key_columns": "false",
    "overwrite_filename": "false"
}

TEMPLATE_SHOPIFY_ORDERS_REPORT = {
    "schedules": [
        {
            "cron_type": CRON_TYPE,
            "cron_interval": 1,
            "cron_interval_start": 1,
            "cron_start_of_day": "04:00:00",
            "time_range_preset": 2,
            "offset_days": 0
        }
    ],
    "report_type": 2,
    "fields": [
        "shop_id",
        "shop_name",
        "shop_timezone",
        "cancelled_at",
        "closed_at",
        "created_at",
        "currency",
        "email",
        "processed_at",
        "subtotal_price",
        "test",
        "total_discounts",
        "total_price",
        "total_tax",
        "updated_at",
        "customer.email",
        "shipping_address.city",
        "shipping_address.first_name",
        "shipping_address.last_name",
        "shipping_address.country"
    ],
    "extract_name_keys": "null",
    "manage_extract_names": "false",
    "overwrite_datastream": "true",
    "overwrite_date_range_column_name": "null",
    "overwrite_key_columns": "false",
    "overwrite_filename": "false"
}


TEMPLATE_SHOPIFY_REFUNDS_REPORT = {
    "schedules": [
        {
            "cron_type": CRON_TYPE,
            "cron_interval": 1,
            "cron_interval_start": 1,
            "cron_start_of_day": "04:00:00",
            "time_range_preset": 2,
            "offset_days": 0
        }
    ],
    "report_type": 5,
    "fields": [
        "shop_id",
        "shop_name",
        "shop_timezone",
        "quantity",
        "subtotal",
        "total_tax",
        "order.created_at",
        "order.total_tax",
        "order.total_price",
        "order.processed_at",
        "order.cancelled_at",
        "order.total_line_items_price",
        "order.financial_status",
        "order.cancel_reason",
        "order.currency",
        "order.closed_at",
        "order.subtotal_price",
        "order.updated_at",
        "order.total_discounts",
        "order.app_id",
        "order.email",
        "order.order_number"
    ],
    "extract_name_keys": "null",
    "manage_extract_names": "false",
    "overwrite_datastream": "true",
    "overwrite_date_range_column_name": "null",
    "overwrite_key_columns": "false",
    "overwrite_filename": "false"
}


class DataStreamControllerShopify(DataStreamControllerBase):
    datastream_type_id = '340'

    def __init__(self, provider: Provider, template: dict):
        """Initialize Data Steam Controller

        :param provider: authentication token
        :type token: adverity.
        :param template: adverity data stream tempalte information
        :type template: dict
        """
        super().__init__(provider, template)


if __name__ == '__main__':
    STACK = 14
    AUTH = 6
    NAME = 'test-shopify-datastream-2'

    p = Provider(stack='rubix', username='rohan+api@rubixagency.com', password='AeUDm6Bp7d2jqJE6')
    dscs = DataStreamControllerShopify(p, TEMPLATE_SHOPIFY_REFUNDS_REPORT)
    # dscf.delete(99)
    dscs.create(stack=STACK, auth=AUTH, name=NAME)

    # dscf.enable_datastream(80)
