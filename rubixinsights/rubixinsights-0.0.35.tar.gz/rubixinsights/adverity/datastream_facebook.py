from base import DataStreamControllerBase
from provider import Provider

template_facebook_age_gender_report = {
    "cron_type": "day",
    "cron_interval": 1,
    "cron_start_of_day": "04:00:00",
    "cron_interval_start": 1,
    "time_range_preset": 2,
    "enabled": True,
    "fields": [
        "account_currency",
        "account_id",
        "account_name",
        "action_values",
        "actions",
        "attribution_setting",
        "campaign_id",
        "campaign_name",
        "clicks",
        "date_start",
        "date_stop",
        "impressions",
        "spend"
    ],
    "calculated_fields": [],
    "action_attribution_windows": [],
    "action_breakdowns": [],
    "force_action_fields": "false",
    "action_report_time": "mixed",
    "breakdowns": [
        "age",
        "gender"
    ],
    # "product_id_limit": "null",
    "translate_custom_conversions": "false",
    "include_future_campaigns": "false",
    "time_increment": "1",
    "pivot_action_fields": "false",
    "adset_targeting_fields": [],
    "extract_name_keys": "date_start",
    "manage_extract_names": "true",
    "overwrite_datastream": "true",
    "overwrite_date_range_column_name": "null",
    "overwrite_key_columns": "true",
    "overwrite_filename": "false"
}

template_facebook_country_report = {
    "cron_type": "day",
    "cron_interval": 1,
    "cron_start_of_day": "04:00:00",
    "cron_interval_start": 1,
    "time_range_preset": 2,
    "enabled": True,
    "fields": [
        "account_currency",
        "account_id",
        "account_name",
        "action_values",
        "actions",
        "attribution_setting",
        "campaign_id",
        "campaign_name",
        "clicks",
        "date_start",
        "date_stop",
        "impressions",
        "spend"
    ],
    "calculated_fields": [],
    "action_attribution_windows": [],
    "action_breakdowns": [],
    "force_action_fields": "false",
    "action_report_time": "mixed",
    "breakdowns": [
        "country"
    ],
    "product_id_limit": "null",
    "translate_custom_conversions": "false",
    "include_future_campaigns": "false",
    "time_increment": "1",
    "pivot_action_fields": "false",
    "adset_targeting_fields": [],
    "extract_name_keys": "date_start",
    "manage_extract_names": "true",
    "overwrite_datastream": "true",
    "overwrite_date_range_column_name": "null",
    "overwrite_key_columns": "true",
    "overwrite_filename": "false"
}

template_facebook_region_report = {
    "cron_type": "day",
    "cron_interval": 1,
    "cron_start_of_day": "04:00:00",
    "cron_interval_start": 1,
    "time_range_preset": 2,
    "enabled": True,
    "fields": [
        "account_currency",
        "account_id",
        "account_name",
        "action_values",
        "actions",
        "attribution_setting",
        "campaign_id",
        "campaign_name",
        "clicks",
        "date_start",
        "date_stop",
        "impressions",
        "spend"
    ],
    "calculated_fields": [],
    "action_attribution_windows": [],
    "action_breakdowns": [],
    "force_action_fields": "false",
    "action_report_time": "mixed",
    "breakdowns": [
        "region"
    ],
    "product_id_limit": "null",
    "translate_custom_conversions": "false",
    "include_future_campaigns": "false",
    "time_increment": "1",
    "pivot_action_fields": "false",
    "adset_targeting_fields": [],
    "extract_name_keys": "date_start",
    "manage_extract_names": "true",
    "overwrite_datastream": "true",
    "overwrite_date_range_column_name": "null",
    "overwrite_key_columns": "true",
    "overwrite_filename": "false"
}

template_facebook_device_platform_report = {
    "cron_type": "day",
    "cron_interval": 1,
    "cron_start_of_day": "04:00:00",
    "cron_interval_start": 1,
    "time_range_preset": 2,
    "enabled": True,
    "fields": [
        "account_currency",
        "account_id",
        "account_name",
        "action_values",
        "actions",
        "attribution_setting",
        "campaign_id",
        "campaign_name",
        "clicks",
        "date_start",
        "date_stop",
        "impressions",
        "spend"
    ],
    "calculated_fields": [],
    "action_attribution_windows": [],
    "action_breakdowns": [],
    "force_action_fields": "false",
    "action_report_time": "mixed",
    "breakdowns": [
        "device_platform"
    ],
    "product_id_limit": "null",
    "translate_custom_conversions": "false",
    "include_future_campaigns": "false",
    "time_increment": "1",
    "pivot_action_fields": "false",
    "adset_targeting_fields": [],
    "extract_name_keys": "date_start",
    "manage_extract_names": "true",
    "overwrite_datastream": "true",
    "overwrite_date_range_column_name": "null",
    "overwrite_key_columns": "true",
    "overwrite_filename": "false"
}

template_facebook_dma_report = {
    "cron_type": "day",
    "cron_interval": 1,
    "cron_start_of_day": "04:00:00",
    "cron_interval_start": 1,
    "time_range_preset": 2,
    "enabled": True,
    "fields": [
        "account_currency",
        "account_id",
        "account_name",
        "action_values",
        "actions",
        "attribution_setting",
        "campaign_id",
        "campaign_name",
        "clicks",
        "date_start",
        "date_stop",
        "impressions",
        "spend"
    ],
    "calculated_fields": [],
    "action_attribution_windows": [],
    "action_breakdowns": [],
    "force_action_fields": "false",
    "action_report_time": "mixed",
    "breakdowns": [
        "dma"
    ],
    "product_id_limit": "null",
    "translate_custom_conversions": "false",
    "include_future_campaigns": "false",
    "time_increment": "1",
    "pivot_action_fields": "false",
    "adset_targeting_fields": [],
    "extract_name_keys": "date_start",
    "manage_extract_names": "true",
    "overwrite_datastream": "true",
    "overwrite_date_range_column_name": "null",
    "overwrite_key_columns": "true",
    "overwrite_filename": "false"
}

template_facebook_hourly_advertiser_tz_report = {
    "cron_type": "day",
    "cron_interval": 1,
    "cron_start_of_day": "04:00:00",
    "cron_interval_start": 1,
    "time_range_preset": 2,
    "enabled": True,
    "fields": [
        "account_currency",
        "account_id",
        "account_name",
        "action_values",
        "actions",
        "attribution_setting",
        "campaign_id",
        "campaign_name",
        "clicks",
        "date_start",
        "date_stop",
        "impressions",
        "spend"
    ],
    "calculated_fields": [],
    "action_attribution_windows": [],
    "action_breakdowns": [],
    "force_action_fields": "false",
    "action_report_time": "mixed",
    "breakdowns": [
        "hourly_stats_aggregated_by_advertiser_time_zone"
    ],
    "product_id_limit": "null",
    "translate_custom_conversions": "false",
    "include_future_campaigns": "false",
    "time_increment": "1",
    "pivot_action_fields": "false",
    "adset_targeting_fields": [],
    "extract_name_keys": "date_start",
    "manage_extract_names": "true",
    "overwrite_datastream": "true",
    "overwrite_date_range_column_name": "null",
    "overwrite_key_columns": "true",
    "overwrite_filename": "false"
}


class DataStreamControllerFacebook(DataStreamControllerBase):
    datastream_type_id = '727'

    def __init__(self, provider: Provider, template: dict, connection_string: str):
        """Initialize Data Steam Controller

        :param provider: authentication token
        :type token: adverity.
        :param template: adverity data stream tempalte information
        :type template: dict
        """
        super().__init__(provider, template, connection_string)


if __name__ == '__main__':
    STACK = 14
    AUTH = 6
    NAME = 'test-facebook-datastream-2'
    CONNECTION_STRING = 'postgresql://postgres:postgres@localhost:5432/mydatabase'

    p = Provider(stack='rubix', username='rohan+api@rubixagency.com', password='AeUDm6Bp7d2jqJE6')
    dscf = DataStreamControllerFacebook(p, template_facebook_age_gender_report, connection_string=CONNECTION_STRING)
    response = dscf.get_all_datastreams('prd')
    print(response['results'])
    # dscf.delete(102)
    # dscf.create(stack=STACK, auth=AUTH, name=NAME)

    # dscf.enable_datastream(80)
