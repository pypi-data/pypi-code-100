config_yaml = """
test:
  feed_env:
    function_name: update_feed_dataservice_connector
    value: Test
  sql_server_write_env:
    function_name: update_writer_table_name
    replace_values:
      - dev_
      - pp_
      - prod_
    new_value: test_
  azure_blob_write_env:
    function_name: update_azure_blob_prefix
    replace_values:
      - dev/
      - pp/
      - prod/
    new_value: test/
  refresh_rate_quarter_hour:
    function_name: update_refresh_frequency_reader
    variable: update_periodical.period.seconds
    new_value: 900

kitchensink:
  feed_env:
    function_name: update_feed_dataservice_connector
    value: Test
  sql_server_write_env:
    function_name: update_writer_table_name
    replace_values:
      - dev_
      - pp_
      - prod_
    new_value: test_
  azure_blob_write_env:
    function_name: update_azure_blob_prefix
    replace_values:
      - dev/
      - pp/
      - prod/
    new_value: test/
  refresh_rate_quarter_hour:
    function_name: update_refresh_frequency_reader
    variable: update_periodical.period.seconds
    new_value: 900
"""