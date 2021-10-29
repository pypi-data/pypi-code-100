from google.cloud import bigquery


def get_url(headers, query, db):
    """Check the appoimentID from the url
    Match with the database to validate if exist

    Args:
        headers ([type]): [Headers Objec]

    Returns:
        url [string]: [url validate]
    """

    url_origin = headers["Origin"]
    try:
        appointment_id = url_origin.split("-")[2]
    except IndexError:
        appointment_id = ""

    # Set the name to None to use positional parameters.
    # Note that you cannot mix named and positional parameters.
    # Based in cloud bigquery documentation.
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "appointment_id", "STRING", appointment_id
            )
        ]
    )
    df = db.query(query["query"], job_config=job_config).to_dataframe()
    url = df.url if not df.empty else ""

    return url
