import requests
import requests
import urllib3
from requests.adapters import HTTPAdapter


def get_datas():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://cn.investing.com/indices/germany-30',
    }

    params = (
        ('pair_id', '172'),
        ('pair_id_for_news', '172'),
        ('chart_type', 'area'),
        ('pair_interval', '86400'),
        ('candle_count', '120'),
        ('events', 'yes'),
        ('volume_series', 'yes'),
        ('period', '1-year'),
    )

    urllib3.disable_warnings()
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))

    response = s.get('https://cn.investing.com/common/modules/js_instrument_chart/api/data.php',
                     headers=headers, params=params, verify=False)

    print(response.text)
