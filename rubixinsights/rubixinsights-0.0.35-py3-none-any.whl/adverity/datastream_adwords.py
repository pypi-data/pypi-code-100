from base import DataStreamControllerBase
from provider import Provider

CRON_TYPE = "day"

TEMPLATE_ADWORDS_GEO_PERFORMANCE_REPORT = {
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
    "exclude_customers": "false",
    "segments": [
        "segments.date",
        "segments.geo_target_region",
        "segments.geo_target_city",
        "segments.geo_target_metro",
        "segments.device"
    ],
    "metrics": [
        "metrics.clicks",
        "metrics.conversions",
        "metrics.conversions_value",
        "metrics.cost_micros",
        "metrics.impressions",
        "metrics.view_through_conversions"
    ],
    "attributes": [
        "campaign.name",
        "customer.id",
        "customer.name",
        "ad_group.name",
        "campaign.advertising_channel_type"
    ],
    "extract_name_keys": "Date",
    "manage_extract_names": "true",
    "overwrite_datastream": "true",
    "overwrite_date_range_column_name": "null",
    "overwrite_key_columns": "false",
    "overwrite_filename": "false"
}

TEMPLATE_ADWORDS_GENDER_PERFORMANCE_REPORT = {
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
    "exclude_customers": "false",
    "segments": [
        "segments.date",
        "segments.device"
    ],
    "metrics": [
        "metrics.clicks",
        "metrics.conversions",
        "metrics.conversions_value",
        "metrics.cost_micros",
        "metrics.impressions",
        "metrics.view_through_conversions"
    ],
    "attributes": [
        "campaign.name",
        "customer.id",
        "customer.name",
        "ad_group.name",
        "campaign.advertising_channel_type",
        "gender_view.resource_name"
    ],
    "extract_name_keys": "Date",
    "manage_extract_names": "true",
    "overwrite_datastream": "true",
    "overwrite_date_range_column_name": "null",
    "overwrite_key_columns": "false",
    "overwrite_filename": "false"
}

TEMPLATE_ADWORDS_AGE_PERFORMANCE_REPORT = {
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
    "exclude_customers": "false",
    "segments": [
        "segments.date",
        "segments.device"
    ],
    "metrics": [
        "metrics.clicks",
        "metrics.conversions",
        "metrics.conversions_value",
        "metrics.cost_micros",
        "metrics.impressions",
        "metrics.view_through_conversions"
    ],
    "attributes": [
        "campaign.name",
        "customer.id",
        "customer.name",
        "ad_group.name",
        "campaign.advertising_channel_type",
        "age_range_view.resource_name"
    ],
    "extract_name_keys": "Date",
    "manage_extract_names": "true",
    "overwrite_datastream": "true",
    "overwrite_date_range_column_name": "null",
    "overwrite_key_columns": "false",
    "overwrite_filename": "false"
}


class DataStreamControllerAdwords(DataStreamControllerBase):
    datastream_type_id = '457'

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
    NAME = 'test-adwords-datastream-2'

    p = Provider(stack='rubix', username='rohan+api@rubixagency.com', password='AeUDm6Bp7d2jqJE6')
    dscs = DataStreamControllerAdwords(p, TEMPLATE_ADWORDS_AGE_PERFORMANCE_REPORT)
    # dscf.delete(99)
    dscs.create(stack=STACK, auth=AUTH, name=NAME)

    # dscf.enable_datastream(80)


# {"id":101,"cron_type":"day","cron_interval":1,"cron_start_of_day":"04:00:00","cron_interval_start":1,"time_range_preset":2,"delta_type":2,"delta_interval":1,"delta_interval_start":1,"delta_start_of_day":"00:00:00","datatype":"Staging","creator":"rohan+api@rubixagency.com","datastream_type_id":457,"absolute_url":"https://rubix.datatap.adverity.com/adwords/101/test-adwords-datastream-2/","schedules":[{"id":2845,"cron_preset":"CRON_EVERY_DAY","cron_type":"day","cron_interval":1,"cron_start_of_day":"04:00:00","cron_interval_start":1,"time_range_preset":2,"time_range_preset_label":"Last 30 Days","delta_type":2,"delta_interval":1,"delta_start_of_day":"00:00:00","delta_interval_start":1,"fixed_start":null,"fixed_end":null,"offset_days":0}],"created":"2021-10-27T20:25:50Z","updated":"2021-10-27T20:25:50Z","slug":"test-adwords-datastream-2","name":"test-adwords-datastream-2","description":"","enabled":false,"retention_type":1,"retention_number":null,"overwrite_key_columns":false,"overwrite_datastream":true,"overwrite_filename":false,"is_insights_mediaplan":false,"manage_extract_names":true,"extract_name_keys":"Date","report_type":"ADGROUP_PERFORMANCE_REPORT","client_customer_ids":[],"fields":["AdGroupId","AdGroupName","AdNetworkType2","CampaignName","Clicks","Cost","Date","Device","Impressions","VideoViews","CampaignId","CampaignStatus","AccountCurrencyCode","Engagements","Interactions","Labels","ViewThroughConversions","CurrentModelAttributedConversions","AccountTimeZone","CurrentModelAttributedConversionValue"],"feed_placeholder_fields":[],"stack":{"id":14,"name":"insights-prd","slug":"insights-prd","url":"https://rubix.datatap.adverity.com/api/stacks/insights-prd/","change_url":"/core/stack/14/change/","extracts_url":"/core/datastreamextract/?stack_id=14","issues_url":"/core/datastreamextractionlog/?ack__exact=0&stack_id=14","overview_url":"/insights-prd/","permissions":{"isCreator":true,"isDatastreamManager":true,"isViewer":true}},"auth":6,"transformers":[],"mccs":[],"active_destination":null,"app_label":"adwords","change_url":"/adwords/googleadwordsdatastream/101/change/","extracts_stream_url":"/api/datastreams/101/extracts/streaming/download/","extracts_url":"/datastream/101/extracts/all","fetch_url":"https://rubix.datatap.adverity.com/adwords/101/test-adwords-datastream-2/?action=fetch","frequency":"Disabled","has_schema_mapping":false,"has_schema_mapping_dimension":false,"issues_url":"/core/datastreamextractionlog/?ack__exact=0&datastream_id=101","last_fetch":null,"next_run":"Not Scheduled","overview_url":"/insights-prd/test-adwords-datastream-2-101/","passive_destinations":"/api/datastreams/101/passive-destinations/","stack_id":14,"supports_extended_intervals":false,"time_range_available":null,"time_range_max":null}
