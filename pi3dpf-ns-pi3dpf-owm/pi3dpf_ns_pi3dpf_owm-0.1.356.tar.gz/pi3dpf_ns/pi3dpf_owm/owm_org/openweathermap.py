import datetime
import pyoo
import json
import logging
import os
import pdb
import re
import shutil
import string
import time
import traceback
from decimal import Decimal, ROUND_HALF_UP
# from com.sun.star.uno import RuntimeException
# from com.sun.star.lang import IllegalArgumentException
# from com.sun.star.connection import NoConnectException

from pathlib import Path
import requests
from pi3dpf_ns.pi3dpf_owm.owm_org import openweathermapToerikflowers_wi as owm
from pi3dpf_ns.pi3dpf_owm.owm_org import suncalc as suncalc
from pi3dpf_ns.pi3dpf_owm.owm_org import pythainlp_util_date as th_date
from pi3dpf_ns.pi3dpf_common import pf_common as pfc

import zipfile

# from collections import ChainMap
import uno

_log = logging.getLogger(__name__)


def extract_hourly(data_list, index, field):
    if field in ['rain', 'snow']:
        return data_list[index][field]['1h'] if field in data_list[index].keys() else None
    elif field == 'weather':
        # id: owm weather condition id, see https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
        # main:
        # description:
        # icon:
        if len(data_list[index][field]) > 1:
            _log.error("extract_hourly - weather has {} elements instead of one. '{}' in PI3D_OWM_LOCATIONS".format(
                len(data_list[index][field]), data_list[index][field]))
            exit(1)
        return data_list[index][field][0]
    else:
        return data_list[index][field]


def value_prep(data):
    if data is None:
        return ""
    elif type(data) is dict:
        return "/".join(data.values())
    return str(data)


def port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def restart_libreoffice_service():
    cmd = "sudo systemctl start libreoffice-headless-owm"
    _log.error("restart_libreoffice_service - libreoffice service not running")
    _log.info("restart_libreoffice_service - using command «{}»".format(cmd))
    rc = os.system("{}".format(cmd))
    return rc


def read_consolidated_csv(csv_file):
    cells = []
    with open(csv_file) as weather_data:
        x = weather_data.readlines()
    max_elements = max([x[i].count(';') for i in range(0, len(x))]) + 1

    with open(csv_file) as weather_data:
        for line in weather_data:
            cells.append(line.strip().split(';') + ["" for i in range(0, max_elements - line.count(';') - 1)])
    for line in range(0, len(cells)):
        cells[line] = [pfc.convert_basic_data_type(cells[line][i]) for i in range(0, len(cells[line]))]
    return cells


def get_sheet_by_name(sheet_spec, lb_calc_obj):
    m = re.search("worksheet=(.*),\s+top_left_cell=(.*)", ", ".join(sheet_spec))
    if not m:
        _log.error("get_sheet_by_name - OWM_5D3H_DATA_RANGE has unexpected format")
        exit(1)
    worksheet = m.group(1)
    cell_address = m.group(2)
    m = re.search("\$?([A-Z]+)\$?(\d+)", cell_address)
    if not m:
        _log.error("get_sheet_by_name - cell address '{}' has unexpected format".format(cell_address))
        exit(1)
    top_left_cell = [int(m.group(2)) - 1, int(col2num(m.group(1))) - 1]
    # idx = [i for i in range(0, len(lb_cacl_obj.sheets)) if lb_cacl_obj.sheets[i].name == worksheet]
    try:
        lb_calc_obj.sheets[worksheet]
    except KeyError:
        _log.error("get_sheet_by_name - unable detecting worksheet with name '{}'".format(worksheet))
        exit(1)
    return worksheet, top_left_cell


def col2num(col):
    # m = re.search("([A-Z])+\d+", cell_address)
    # if not m:
    #     _log.error("col2num - invalid cell address '{}'".format(cell_address))
    #     exit(1)
    # col = m.group(1)
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num


class OpenWeatherMap:

    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.OWM_DATA_DIR = pfc.get_config_param(self.config, 'OWM_DATA_DIR')
        if not os.path.exists(self.OWM_DATA_DIR):
            os.makedirs(self.OWM_DATA_DIR)
        self.OWM_API_KEY = pfc.get_config_param(self.config, 'OWM_API_KEY')
        if self.OWM_API_KEY == 'add-your-secret-here':
            print('ERROR - OWM_API_KEY is not defined')
            _log.error('OWM_API_KEY is not defined')
            exit(1)
        self.OWM_UNITS = pfc.get_config_param(self.config, 'OWM_UNITS')
        self.locations_hourly = []

        self.OWM_CITY_IDS = pfc.get_config_param(self.config, 'OWM_CITY_IDS')
        self.OWM_5D3H_BASE_URL = pfc.get_config_param(self.config, 'OWM_5D3H_BASE_URL')
        self.locations_5d = []
        self.city_names = []
        for i in range(0, len(self.OWM_CITY_IDS)):
            m = re.match(r'(\d+):(.*)', self.OWM_CITY_IDS[i])
            if not m:
                _log.error("__init__ - unexpected pattern in OWM_CITY_IDS: '{}'".format(
                    self.OWM_CITY_IDS[i]))
                exit(1)
            self.locations_5d.append({'id': m.group(1), 'langs': m.group(2).split('+')})

        self.unit_temp = "°K"
        self.unit_len_s = "mm"
        self.unit_len_l = "m"
        self.unit_speed = "km/h"
        self.unit_press = "hPa"
        if self.OWM_UNITS == 'metric':
            self.unit_temp = "°C"
        elif self.OWM_UNITS == 'imperial ':
            self.unit_temp = "°F"
            self.unit_len_s = '"'
            self.unit_speed = "miles/h"

        self.units = {'rain': self.unit_len_s, 'snow': self.unit_len_s, 'temp': self.unit_temp,
                      'pressure': self.unit_press, 'humidity': '%', 'dew_point': self.unit_temp, 'uvi': '',
                      'clouds': '%', 'visibility': self.unit_len_l, 'wind_speed': self.unit_speed, 'wind_deg': '°',
                      'wind_gust': self.unit_speed, 'pop': '%', 'feels_like': self.unit_temp,
                      'temp_min': self.unit_temp, 'temp_max': self.unit_temp, 'sea_level': self.unit_press,
                      'grnd_level': self.unit_press}
        self.OWM_DT_FORMAT = pfc.get_config_param(self.config, 'OWM_DT_FORMAT')
        self.OWM_DATE_FORMAT = pfc.get_config_param(self.config, 'OWM_DATE_FORMAT')
        self.OWM_TIME_FORMAT = pfc.get_config_param(self.config, 'OWM_TIME_FORMAT')
        self.OWM_5D3H_SHOW_REQUEST_DETAIL = pfc.get_config_param(self.config, 'OWM_5D3H_SHOW_REQUEST_DETAIL')
        self.OWM_5D3H_LIBREOFFICE_TEMPLATE_IN = pfc.get_config_param(self.config, 'OWM_5D3H_LIBREOFFICE_TEMPLATE_IN')
        self.OWM_THAI_BA_DTFORMAT = pfc.get_config_param(self.config, 'OWM_THAI_BA_DTFORMAT')
        self.OWM_LIBREOFFICE_PNG_CONVERT_CMD = pfc.get_config_param(self.config, 'OWM_LIBREOFFICE_PNG_CONVERT_CMD')
        self.owm4pf = owm.owm4pf(config, _log)
        self.OWM_5D3H_DATA_RANGE = pfc.get_config_param(self.config, 'OWM_5D3H_DATA_RANGE')
        self.OWM_5D3H_LIBREOFFICE_PRINT_READY = pfc.get_config_param(self.config, 'OWM_5D3H_LIBREOFFICE_PRINT_READY')
        self.desktop = None
        # retry = 2
        # succeeded = False
        # while retry > 0 and not succeeded:
        #     try:
        #         self.desktop = pyoo.Desktop('localhost', 8052)
        #         succeeded = True
        #     except OSError as e:
        #         restart_libreoffice_service()
        #         # cmd = "sudo systemctl start libreoffice-headless"
        #         # _log.error("__init__ - libreoffice service not running")
        #         # _log.info("__init__ - using command «{}»".format(cmd))
        #         # rc = os.system("{}".format(cmd))
        #     retry -= 1

    def get_5_days(self):
        self.city_names = []
        for i in range(0, len(self.locations_5d)):
            p_dict, city_names, first_lang_run, sunrise, sunset = {}, {}, True, "", ""
            for lang in self.locations_5d[i]['langs']:
                req_params = {"id": self.locations_5d[i]['id'], "appid": self.OWM_API_KEY,
                              "units": self.OWM_UNITS, "lang": lang}
                try:
                    _log.info("get_5_days - retrieving {} for id='{}' lang='{}'".format(
                        self.OWM_5D3H_BASE_URL, self.locations_5d[i]['id'], lang))
                    resp = self.session.get(self.OWM_5D3H_BASE_URL, params=req_params)
                    resp_json = json.loads(resp.text)
                    if self.OWM_5D3H_SHOW_REQUEST_DETAIL:
                        _log.info("get_5_days - successfully retrieved from url {}".format(resp.url))
                        _log.info("get_5_days - json results: {}".format(json.dumps(resp_json, indent=4)))
                    # dt = [resp_json['list'][i]['dt'] for i in range(0, len(resp_json['list']))]
                    tz_offset_secs = resp_json['city']['timezone']
                    if city_names == {}:
                        city_names = {lang: resp_json['city']['name'], 'country_code': resp_json['city']['country']}
                    else:
                        city_names[lang] = resp_json['city']['name']

                    tz_offset = datetime.timedelta(seconds=tz_offset_secs)
                    tz = datetime.timezone(tz_offset)
                    d = resp_json['city']['sunrise']
                    sunrise = "{}".format(datetime.datetime.fromtimestamp(d, tz=tz).strftime(self.OWM_TIME_FORMAT))
                    d = resp_json['city']['sunset']
                    sunset = "{}".format(datetime.datetime.fromtimestamp(d, tz=tz).strftime(self.OWM_TIME_FORMAT))
                    sun_time_s = resp_json['city']['sunset'] - resp_json['city']['sunrise']
                    sun_time_hhmm = time.strftime('%Hh %Mmin', time.gmtime(sun_time_s))
                    lat, long = resp_json['city']['coord']['lat'], resp_json['city']['coord']['lon']
                    mt = suncalc.getMoonTimes(datetime.datetime.now(), lat, long)
                    moon_rise = mt['rise'].strftime(self.OWM_TIME_FORMAT) if 'rise' in mt.keys() else ""
                    moon_set = mt['set'].strftime(self.OWM_TIME_FORMAT) if 'set' in mt.keys() else ""
                    moon_phase = suncalc.getMoonIllumination(datetime.datetime.now(tz=tz))['phase']
                    moon_offset = int(Decimal(moon_phase * 27).quantize(0, ROUND_HALF_UP))
                    # 0xf0d0...: when font is white, these icons look confusing. Better use 0xf095
                    moon_wi_icon = chr(0xf095 + moon_offset)

                    weekday = ""
                    for t in range(0, len(resp_json['list'])):
                        dt_format_label = "%H"
                        dt_index = datetime.datetime.fromtimestamp(
                            resp_json['list'][t]['dt'], tz=tz).strftime(self.OWM_DT_FORMAT)
                        if first_lang_run:
                            wd = datetime.datetime.fromtimestamp(resp_json['list'][t]['dt'], tz=tz, ).strftime('%a')
                            p_dict[dt_index] = {'dt_weekday': wd if wd != weekday else "",
                                                'dt_label': "{}".format(datetime.datetime.fromtimestamp(
                                                    resp_json['list'][t]['dt'], tz=tz).strftime(dt_format_label))}
                            weekday = wd
                    keys_list_of_list = [[*resp_json['list'][i]] for i in range(0, len(resp_json['list']))]

                    for param in ['tl_snow', 'tl_rain', 'main_temp', 'main_feels_like', 'main_temp_min',
                                  'main_temp_max', 'main_pressure', 'main_sea_level', 'main_grnd_level',
                                  'main_humidity', 'wind_speed', 'wind_deg', 'wind_gust', 'tl_pop', 'weather_id',
                                  'weather_main', 'weather_description', 'weather_icon']:
                        m = re.match(r'^(tl|main|wind|weather)_(.*)', param)
                        if not m:
                            _log.error("get_5_days - unable identifying top_element in '{}'".format(param))
                            exit(1)
                        el_top, el_base = m.group(1), m.group(2)
                        # print("working on {}".format(param))
                        p_list = [self.extract_5d(resp_json['list'], i, el_top, el_base) for i in
                                  range(0, len(resp_json['list']))]
                        p_label = el_base
                        if el_top in ['wind', 'weather']:
                            p_label = "{}_{}".format(el_top, el_base)
                        for count, key in enumerate(p_dict):
                            if p_label == 'weather_description':
                                if p_label in p_dict[key].keys():
                                    p_dict[key][p_label][lang] = p_list[count]
                                else:
                                    p_dict[key][p_label] = {lang: p_list[count]}
                            else:
                                p_dict[key][p_label] = p_list[count]
                            if param == 'weather_icon':
                                wid, icon = p_dict[key]['weather_id'], p_dict[key]['weather_icon']
                                p_dict[key]['weather_icon_ef'] = chr(self.owm4pf.map_owm_wi(wid, icon))
                            elif param == 'wind_speed':
                                ws = float(p_dict[key]['wind_speed'])
                                p_dict[key]['wind_speed_icon'] = owm.wind_speed_to_wi_icon(ws, self.units['wind_speed'])
                except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
                    _log.warning("get_5_days - [{}] connection reset. Traceback:\n{}".format(
                        resp.url, traceback.format_exc()))
                    exit(1)
                    # return None
                first_lang_run = False

            self.locations_5d[i]['city_txt'] = \
                "{}.{}".format(city_names['country_code'], " ".join(
                    [city_names[i] for i in city_names.keys() if len(i) == 2]))
            data_dir = os.path.join(self.OWM_DATA_DIR, "5d_{:03d}_{:08d}_{}".format(
              i + 1, int(self.locations_5d[i]['id']), self.locations_5d[i]['city_txt']))
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            print_ready = os.path.join(data_dir, self.OWM_5D3H_LIBREOFFICE_PRINT_READY)
            if not os.path.exists(print_ready):
                _log.info("get_5_days - copy '{}' '{}'".format(self.OWM_5D3H_LIBREOFFICE_TEMPLATE_IN, print_ready))
                shutil.copy(self.OWM_5D3H_LIBREOFFICE_TEMPLATE_IN, print_ready)

            with open(os.path.join(data_dir, "consolidated.csv"), 'w') as f:
                # writing header titles
                f.write("Sunrise:;{};Sunset:;{};Sun_HHMM:;{};Moonrise:;{};Moonset:;{};Moon Symbol;{}\n".format(
                    sunrise, sunset, sun_time_hhmm, moon_rise, moon_set, moon_wi_icon))
                d_format = "{} {}".format(self.OWM_DATE_FORMAT, self.OWM_TIME_FORMAT)
                # OWM_THAI_BA_DTFORMAT is normaly set to "%A %d %B %Y"
                gen_th = th_date.thai_strftime(datetime.datetime.now(tz=tz), self.OWM_THAI_BA_DTFORMAT)
                f.write("Coordinates:;{};Languages:;{};Generated:;{};Gen. TH:;{};unit_temp:;{};unit_press:;{};".format(
                    "{} {}".format(lat, long), '"{}"'.format(",".join(city_names.keys())),
                    datetime.datetime.now().strftime(d_format), gen_th, self.unit_temp, self.unit_press))
                f.write("unit_precipitation:;{};unit_speed:;{}\n".format(self.unit_len_s, self.unit_speed))

                # f.write("Languages:;{}\n".format(",".join(city_names.keys())))
                f.write("City Names:;{}\n".format("{}/{}".format(
                    "/".join(city_names.values()), resp_json['city']['country'])))
                la_li = [*p_dict[[*p_dict][0]]]  # la_li: short for label_list
                la_li = ["{} ({})".format(i, self.units[i]) if i in self.units else i for i in la_li]
                f.write("{}\n".format(";".join(['date'] + la_li)))
                for idx in p_dict.keys():
                    f.write("{};{}\n".format(idx, ";".join(
                        [value_prep(s) for s in p_dict[idx].values()])))
        log_file, cmd_base = _log.parent.handlers[0].baseFilename, self.OWM_LIBREOFFICE_PNG_CONVERT_CMD
        for i in range(0, len(self.locations_5d)):
            # From: https://pypi.org/project/pyoo/
            data_dir = os.path.join(self.OWM_DATA_DIR, "5d_{:03d}_{:08d}_{}".format(
                i + 1, int(self.locations_5d[i]['id']), self.locations_5d[i]['city_txt']))
            print_ready = os.path.join(data_dir, self.OWM_5D3H_LIBREOFFICE_PRINT_READY)
            _log.info("get_5_days - refreshing data in {}".format(print_ready))
            soft_link_target = os.path.join(self.OWM_DATA_DIR, '5d_000_current_city')
            # delete existing soft link when pointing a wrong directory
            if os.path.exists(soft_link_target) and os.readlink(soft_link_target) != data_dir:
                _log.info("get_5_days - removing softlink '{}'".format(soft_link_target))
                os.remove(soft_link_target)
            # create new softlink, if not already existing
            if not os.path.exists(soft_link_target):
                _log.info("get_5_days - 5d_000_current_city -> '{}' # new softlink".format(data_dir))
                Path(os.path.join(os.path.dirname(data_dir), '5d_000_current_city')).symlink_to(data_dir)
            if not port_in_use(8052):
                restart_libreoffice_service()
            retry = 2
            succeeded = False
            while retry > 0 and not succeeded:
                try:
                    self.desktop = pyoo.Desktop('localhost', 8052)
                    succeeded = True
                except OSError as e:
                    restart_libreoffice_service()
                    time.sleep(5)
                retry -= 1
            # # check path to consolidated.csv inside the LibreCalc document and issue warning when inconsistent
            # zip_arch = os.path.join(data_dir, self.OWM_5D3H_LIBREOFFICE_PRINT_READY)
            # data_link_ok, expected_link = False, os.path.realpath(os.path.join(data_dir, 'consolidated.csv'))
            # effective_link = None
            # with zipfile.ZipFile(zip_arch) as myzip:
            #     with myzip.open('content.xml') as myfile:
            #         content_xml = myfile.read().decode('utf-8')
            #         m = re.search("xlink:type=.simple.\s+xlink:href=.(.*?consolidated.csv). table:filter-name=", content_xml, flags=re.MULTILINE)
            #         if m and m.group(1) == expected_link:
            #             effective_link = os.path.realpath(m.group(1))
            #             data_link_ok = True
            # if not data_link_ok:
            #     msg = "Data probably not up-to-date. Data link in '{}': ".format(zip_arch)
            #     _log.warning("get_5_days - {}'{}'".format(msg, effective_link))
            #     _log.warning("get_5_days - Expected data link: '{}'".format(expected_link))
            #

            expected_link = os.path.realpath(os.path.join(data_dir, 'consolidated.csv'))
            _log.info("get_5_days - opening '{}'".format(print_ready))
            doc = self.desktop.open_spreadsheet(print_ready)
            sheet_name, cell_address = get_sheet_by_name(self.OWM_5D3H_DATA_RANGE, doc)
            cells = read_consolidated_csv(expected_link)
            sheet = doc.sheets[sheet_name]
            _log.info("get_5_days - City: {} Start Date: {} # Values from Libre Calc".format(
                doc.sheets[1][10, 2].value, doc.sheets[1][12, 1].value))
            max_elements = max([len(cells[i]) for i in range(0, len(cells))])
            sheet = doc.sheets[sheet_name]
            sheet[slice(cell_address[0], cell_address[0] + len(cells)), slice(cell_address[1], cell_address[1] + max_elements)].values = cells
            doc.save()
            doc.close()

            cmd = "{} -t 5D3H -c {} -l {}".format(cmd_base, self.locations_5d[i]['id'], log_file)
            _log.info("+ {}".format(cmd))
            rc = os.system("{}".format(cmd))

    def extract_5d(self, data_list, index, top, base):
        try:
            data_list_index = "{}_{}".format(top, base)
            if top in ['tl']:
                try:
                    return data_list[index][base]['3h'] if base in ['snow', 'rain'] else data_list[index][base]
                except KeyError:
                    if base in ['snow', 'rain']:
                        return None
                    else:
                        raise
            elif top in ['weather']:
                if len(data_list[index][top]) != 1:
                    s = len(data_list[index][top])
                    _log.warning("extract_5d - weather array has length={}. {}".format(s, data_list[index][top]))
                return data_list[index][top][0][base]
            elif data_list_index in self.units and self.units[data_list_index] == "km/h":
                ms = data_list[index][top][base]
                kmh = "{:0.2f}".format(ms * 3.6)
                _log.debug("extract_5d - converting [{}] {}m/s to {}km/h".format(data_list_index, ms, kmh))
                return kmh
            else:
                return data_list[index][top][base]
        except KeyError:
            _log.error("extract_5d - element not found: index='{}', top='{}', base='{}'".format(index, top, base))
            if top not in data_list[index].keys():
                _log.info("extract_5d -  top='{}' not in  data_list[{}]={}".format(top, index, data_list[index]))
                exit(1)
            _log.info("extract_5d - data_list[{}][{}]={}".format(index, top, data_list[index][top]))
            exit(1)
        except TypeError:
            # TODO: make better
            pdb.set_trace()
