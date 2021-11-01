from .functions import Querys


def get_url(headers, db):
    """Check the appoimentID from the url
    Match with the database to validate if exist

    Args:
        headers ([type]): [Headers Objec]

    Returns:
        url [string]: [url validate]
    """

    try:
        url_origin = headers.get("Origin", False)
        appointment_id = url_origin.split("-")[2]
        query_functions = Querys(appointment_id)
        query, job_config = query_functions.from_telehealth_room_url()
        df = db.query(query, job_config=job_config).to_dataframe()
        url = df.url[0] if not df.empty else ""
    except IndexError:
        url = ""
    except AttributeError:
        url = ""

    return url
