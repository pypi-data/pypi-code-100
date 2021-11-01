from google.cloud import bigquery


class Querys:
    def __init__(self, appointment_id):
        self.appointment_id = appointment_id

    def from_telehealth_room_url(self):
        query = """
            SELECT telehealth_room_url AS url FROM
        `crx-beta-bsti.NY_BSTI_Dev.Telehealth_Room_URL`
        WHERE appointment_id = @appointment_id
        LIMIT 1"""

        # Set the name to None to use positional parameters.
        # Note that you cannot mix named and positional parameters.
        # Based in cloud bigquery documentation.
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(
                    "appointment_id", "STRING", self.appointment_id
                )
            ]
        )

        return query, job_config
