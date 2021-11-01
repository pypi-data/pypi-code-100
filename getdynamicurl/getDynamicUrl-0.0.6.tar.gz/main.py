from dynamic_url import Url
from google.cloud import bigquery

db = bigquery.Client()

dic = {
    "Origin": "https://bsti-telehealth-3040f7f35c4f4a0-b7lefc4bya-uc.a.run.app/"
}
url_obj = Url()
url_validate = url_obj.get_url(dic, db)
