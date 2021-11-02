# interface for below fonts:
#   http://erikflowers.github.io/weather-icons/
#   https://github.com/erikflowers/weather-icons
import pdb
import shutil
import urllib.request
import os
import json
import re
import time
import datetime
import sys
import string
import zipfile
# import suncalc
import threading
from pi3dpf_ns.pi3dpf_owm.owm_org import pythainlp_util_date as pythainlp_util_date  # local copy in /opt/pf/lib
from pi3dpf_ns.pi3dpf_common import pf_common as pfc
# from ..common import pf_common as pfc
from decimal import Decimal, ROUND_HALF_UP
from pi3dpf_ns.pi3dpf_owm.owm_org import suncalc as suncalc


class owm4pf:

    def __init__(self, config, pi3d_log):
        self.config = config
        self.log = pi3d_log
        self.wstring = ""
        self.get_config(self)  # this is were all config parameters get initialized
        self.warn_cache = True
        self.warn_count = 1000
        self.weather = {}
        self.wthrloader = threading.Thread(target=self.update_weather_info_background, daemon=True)
        self.loaderStarted = False
        self.last_run = datetime.datetime.now() - datetime.timedelta(minutes=int(self.OWM_NOW_REFRESH_RATE + 10))
        self.template = None
        self.weather_template_values = {}
        self.info = None
        self.city_ids_by_lang = {}

        if self.OWM_NOW_RETRIEVE_LOCAL_WEATHER:
            mtime_owm_now_formatstring = datetime.datetime.now() - datetime.timedelta(
                minutes=int(self.OWM_NOW_REFRESH_RATE + 30))
            if self.OWM_NOW_FORMATSTRING_USE:
                fname_owm_now_formatstring = os.path.join(self.OWM_SCIS_BMP_DIR, 'owm_now_formatstring_0.png')
                mtime_owm_now_formatstring = datetime.datetime.fromtimestamp(
                    os.path.getmtime(fname_owm_now_formatstring)) if os.path.isfile(
                    fname_owm_now_formatstring) else self.last_run
                if datetime.datetime.fromtimestamp(self.max_age_config_files(self.config.cfg_fname)[
                                                       0]) > mtime_owm_now_formatstring and os.path.isfile(
                    fname_owm_now_formatstring):
                    mtime_owm_now_formatstring = self.last_run

            mtime_OWM_NOW_LIBREOFFICE_BITMAP_OUT = datetime.datetime.now() - datetime.timedelta(
                minutes=int(self.OWM_NOW_REFRESH_RATE + 30))
            md, cf = self.max_age_config_files(self.config.cfg_fname)
            if self.OWM_NOW_LIBREOFFICE_TEMPLATE_USE:
                mtime_OWM_NOW_LIBREOFFICE_BITMAP_OUT = datetime.datetime.fromtimestamp(
                    os.path.getmtime(self.OWM_NOW_LIBREOFFICE_BITMAP_OUT)) if os.path.isfile(
                    self.OWM_NOW_LIBREOFFICE_BITMAP_OUT) else self.last_run
                if datetime.datetime.fromtimestamp(md) > mtime_OWM_NOW_LIBREOFFICE_BITMAP_OUT and os.path.isfile(
                        fname_owm_now_formatstring):
                    # config file pf.config has changed since last generation of OWM_NOW_LIBREOFFICE_BITMAP_OUT,
                    # force updateWeatherInfo() to be executed
                    mtime_OWM_NOW_LIBREOFFICE_BITMAP_OUT = self.last_run
            self.log.info("config file: {} last modified: {} ".format(
                cf, datetime.datetime.fromtimestamp(md).strftime('%Y-%m-%d %H:%M:%S')))
            self.log.info("show  scrolling  weather info: {:>3s} last modified: {}".format(
                'yes' if self.OWM_NOW_FORMATSTRING_USE else 'no', mtime_owm_now_formatstring.strftime('%Y-%m-%d %H:%M:%S')))
            self.log.info("show libreoffice weather info: {:>3s} last modified: {}".format(
                'yes' if self.OWM_NOW_FORMATSTRING_USE else 'no',
                mtime_OWM_NOW_LIBREOFFICE_BITMAP_OUT.strftime('%Y-%m-%d %H:%M:%S')))
            self.last_run = mtime_owm_now_formatstring if mtime_owm_now_formatstring > self.last_run else self.last_run
            self.last_run = mtime_OWM_NOW_LIBREOFFICE_BITMAP_OUT if mtime_OWM_NOW_LIBREOFFICE_BITMAP_OUT > self.last_run else self.last_run

    def clear_for_owm_update(self):
        if not self.OWM_NOW_RETRIEVE_LOCAL_WEATHER:
            return False
        if datetime.datetime.now() < self.last_run + datetime.timedelta(minutes=int(self.OWM_NOW_REFRESH_RATE)):
            self.warn_count += 1
            if self.warn_count > 1000:
                self.log.warning("returning cached weather info")
                self.log.info("weather info scheduled for refresh at: {}. (Governed by OWM_NOW_REFRESH_RATE)".format(
                    (self.last_run + datetime.timedelta(minutes=int(self.OWM_NOW_REFRESH_RATE))).strftime(
                        '%Y-%m-%d %H:%M:%S')))
                self.warn_count = 0
                self.warn_cache = False
            return False
        return True

    def augment_template(self):  # , template
        self.getWeatherTemplateFromLibreOffice()  # read template from libreoffice document
        self.order_cities_by_lang()
        self.weather_template_values = {}

        for lang in self.city_ids_by_lang.keys():
            self.log.info("language: {}".format(lang))
            req_url = "{}&id={}&lang={}&APPID={}".format(self.OWM_NOW_BASE_URL,
                                                         ','.join(map(str, self.city_ids_by_lang[lang])), lang,
                                                         self.OWM_API_KEY)
            self.log.info("owm url: {}".format(req_url))
            req = urllib.request.Request(req_url)
            r = urllib.request.urlopen(req).read()
            self.info = json.loads(r.decode('utf-8'))
            if re.match('^http://api.openweathermap.org/data/2.5/group', self.OWM_NOW_BASE_URL):
                self.log_owm_group(lang)
            else:
                self.log.error("{} is not implemented".format(self.OWM_NOW_BASE_URL))
                exit(1)

        # display available tokens and if they are matched in template
        self.log.info("expanded tokens while using template OWM_NOW_LIBREOFFICE_TEMPLATE_IN='{}'.".format(
            self.OWM_NOW_LIBREOFFICE_TEMPLATE_IN))
        unexpanded_list = ""
        for k in self.weather_template_values.keys():
            search_stat = "expanded" if re.search(r'\${}'.format(k), self.template) else "not expanded"
            if search_stat == "expanded":
                if re.sub(r'\d+$|_\d+$', '', k) in ['wift']:
                    self.log.info(
                        "{:>25} - {:>12} - 0x{:X}".format("$" + k, search_stat, ord(self.weather_template_values[k])))
                elif re.sub(r'\d+$|_\d+$', '', k) in ['moon_icon']:
                    self.log.info(
                        "{:>25} - {:>12} - 0x{:0X}".format("$" + k, search_stat, ord(self.weather_template_values[k])))
                else:
                    self.log.info("{:>25} - {:>12} - {}".format("$" + k, search_stat, self.weather_template_values[k]))
            else:
                unexpanded_list += k + ' '
        self.log.info("The following tokens were not expanded: {}".format(unexpanded_list))

        self.check_and_change_template_tokens()
        self.log.info("  OWM_NOW_FORMATSTRING specification: {}".format(self.OWM_NOW_FORMATSTRING))
        for c in self.OWM_CITY_IDS:
            c = int(re.sub(r':.*', '', c))
            # expanding {city}, {local_time}, {local_time_thba}, {description}, {icon_only}, {sunrise}, {sunset}, {tz},
            # {temp}, {temp_felt}, {temp_min}, {temp_max}, {pressure}, {humidity}
            weather_template = string.Template(self.template)
            self.template = weather_template.safe_substitute(self.weather_template_values)
        self.wstring = self.wstring.replace('\\n', chr(0x0a))
        #   self.log.info("  OWM_NOW_FORMATSTRING      expanded: {}".format(self.wstring.replace('\n', '\\n')))

        # loop through all cities in all requested languages. Need to complete before we can compose the output string
        # as the weather description is specific to each requested language
        # self.addWeatherToTemplate() # add contents.xml to self template
        # self.template = template
        self.putOwmInfoToLibreOfficeTemplate()
        # self.log.parent.handlers[0].baseFilename instead of self.log.HANDLER.baseFilename
        # log_fn = self.log.parent.handlers[0].baseFilename
        cmd = "{} -t now -l {}".format(self.OWM_LIBREOFFICE_PNG_CONVERT_CMD, self.log.parent.handlers[0].baseFilename)
        self.log.info("+ {}".format(cmd))
        rc = os.system("{}".format(cmd))

        self.last_run = datetime.datetime.now()
        self.warn_cache = True
        # return self.template

    def update_weather_info(self):
        if self.clear_for_owm_update() and not self.loaderStarted:
            self.augment_template()
            self.getWeather()
        if not self.loaderStarted:
            self.wthrloader.start()
            self.loaderStarted = True
        return self.wstring.split('\n')

    def update_weather_info_background(self):
        while True:
            if self.clear_for_owm_update():
                self.augment_template()
                self.getWeather()
            else:
                time.sleep(60)

    def check_and_change_template_tokens(self):
        tokens = ['city', 'temp', 'temp_felt', 'temp_min', 'temp_max', 'pressure', 'humidity', 'sunrise', 'sunset',
                  'description', 'icon_only', 'local_time', 'tz', 'local_time_thba']
        for token in tokens:
            m = re.search('{' + token + '(|:.+?)}', self.template)
            if m:
                #       import pdb; pdb.set_trace()
                self.log.info("found token '{}' with extensions '{}'.".format(token, m.group(1)))
                if m.group(1) != "":
                    rest = m.group(1)
                    m = re.search(r'(\d{6})', rest)
                    if m:
                        self.log.info("detected city id '{}'.".format(m.group(1)))

    def max_age_config_files(self, config_files):
        mdate = 0
        fname = ''
        for cf in config_files:
            md = os.path.getmtime(cf)
            #     mdate =  md if md > mdate else mdate
            if md > mdate:
                mdate = os.path.getmtime(cf)
                fname = cf
        return mdate, fname

    def log_owm_group(self, req_lang):
        cs = ""
        wi_icons_inuse = {'wi-baro': chr(0xf079), 'wi-sunrise': chr(0xf051), 'wi-sunset': chr(0xf052),
                          'wi-thermo': chr(0xf053), 'wi-humidity': chr(0xf07a),
                          'wi-moonrise': chr(0xf0c9), 'wi-moonset': chr(0xf0ca)}
        wi_icons_empty = {'wi-baro': '', 'wi-sunrise': '', 'wi-sunset': '', 'wi-thermo': '', 'wi-humidity': ''}
        ico = wi_icons_inuse
        tmp_unit = "°C" if self.OWM_UNITS == 'metric' else "°F"

        # todo: check format string for wrong input labels and remove them after warning
        # todo: self.info['list'][0]['wind']
        # todo: self.info['list'][0]['clouds']

        for i in range(0, len(self.info['list'])):
            ciid = self.info['list'][i]['id']
            city = self.info['list'][i]['name']
            temp = "{}{:.1f}{}".format(ico['wi-thermo'], self.info['list'][i]['main']['temp'], tmp_unit)
            felt = "{:.1f}{}".format(self.info['list'][i]['main']['feels_like'], tmp_unit)
            tmin = "{:.1f}{}".format(self.info['list'][i]['main']['temp_min'], tmp_unit)
            tmax = "{:.1f}{}".format(self.info['list'][i]['main']['temp_max'], tmp_unit)
            pres = "{}{}hPa".format(ico['wi-baro'], self.info['list'][i]['main']['pressure'])
            humi = "{}{}%".format(ico['wi-humidity'], self.info['list'][i]['main']['humidity'])
            tztx = "GMT{:+d}".format(self.info['list'][i]['sys']['timezone'] // 3600)
            # display sunrise/sunset in local time of given city
            oset = datetime.timedelta(seconds=self.info['list'][i]['sys']['timezone'])
            tz = datetime.timezone(oset)
            sris = "{}{}".format(ico['wi-sunrise'],
                                 datetime.datetime.fromtimestamp(self.info['list'][i]['sys']['sunrise'],
                                                                 tz=tz).strftime(self.OWM_SUNRISE_SUNSET_DTFORMAT))
            sset = "{}{}".format(ico['wi-sunset'],
                                 datetime.datetime.fromtimestamp(self.info['list'][i]['sys']['sunset'], tz=tz).strftime(
                                     self.OWM_SUNRISE_SUNSET_DTFORMAT))
            long = float(self.info['list'][i]['coord']['lon'])
            lati = float(self.info['list'][i]['coord']['lat'])
            # cool site to validate output: https://www.mooncalc.org/
            MoonTimes = suncalc.getMoonTimes(datetime.datetime.now(), lati, long)  # tz=tz
            if 'alwaysUp' in MoonTimes.keys() or 'alwaysDown' in MoonTimes.keys():
                self.log.warning("Moon in state {}, which is not yet properly implemented".format(
                    list(k for k in MoonTimes.keys() if k[0:6] == 'always')[0]))
            tz_zulu = datetime.timezone(datetime.timedelta(seconds=0))
            mris = "{}{}".format(ico['wi-moonrise'], MoonTimes['rise'].astimezone(tz_zulu).astimezone(tz).strftime(
                self.OWM_SUNRISE_SUNSET_DTFORMAT)) if 'rise' in MoonTimes.keys() else "{} -".format(ico['wi-moonrise'])
            mset = "{}{}".format(ico['wi-moonset'], MoonTimes['set'].astimezone(tz_zulu).astimezone(tz).strftime(
                self.OWM_SUNRISE_SUNSET_DTFORMAT)) if 'set' in MoonTimes.keys() else "{} -".format(ico['wi-moonset'])
            moon_phase = suncalc.getMoonIllumination(datetime.datetime.now(tz=tz))['phase']
            moff = int(Decimal(moon_phase * 27).quantize(0, ROUND_HALF_UP))
            mico = chr(0xf095 + moff)  # 0xf0d0...: when font is white, these icons look confusing. Better use 0xf095
            desc = self.info['list'][i]['weather'][0]['description']
            lclt = datetime.datetime.now(tz=tz).strftime(self.OWM_NOW_CITY_DTFORMAT)
            wift = self.map_owm_wi(self.info['list'][i]['weather'][0]['id'], self.info['list'][i]['weather'][0]['icon'])

            # convert local time to thai time with buddhist era:
            #  - https://gist.github.com/bact/b8afe49cb1ae62913e6c1e899dcddbdb and
            #  - https://thainlp.org/pythainlp/docs/2.0/api/util.html#pythainlp.util.thai_strftime
            ltba = pythainlp_util_date.thai_strftime(datetime.datetime.now(tz=tz),
                                                     self.OWM_THAI_BA_DTFORMAT)  # "%A %d %B %Y"

            self.log.info("   OWM City ID: {}".format(self.info['list'][i]['id']))
            self.log.info(
                "        {{city}}: {}, {{local_time}}: {}, {{local_time_thba}}: {} {{tz}}: {} {{longitude}}: {} {{latitude}}: {}".format(
                    city, lclt, ltba, tztx, long, lati))
            self.log.info(
                "     {{sunrise}}: {}, {{sunset}}: {} {{moonrise}}: {}, {{moonset}}: {}, {{moon_icon}}: 0x{:0X}, moon-phase: {:5.3f}".format(
                    sris, sset, mris, mset, ord(mico), moon_phase))
            self.log.info(
                "        {{temp}}: {}, {{temp_felt}}: {}, {{temp_min}}: {}, {{temp_max}}: {}, unit: {}".format(
                    temp, felt, tmin, tmax, tmp_unit))
            self.log.info("    {{pressure}}: {}, {{humidity}}: {}".format(pres, humi))
            # there are more than one entries possible for ['weather'].
            # Ignore the ones > 0 in the hope the 1st is the most important.
            self.log.info(" {{description}}: {}".format(self.info['list'][i]['weather'][0]['description']))
            self.log.info("      OWM-Icon: {}".format(self.info['list'][i]['weather'][0]['icon']))
            self.log.info("        OWM-ID: {}".format(self.info['list'][i]['weather'][0]['id']))
            self.log.info("       WI-Font: 0x{:X}".format(wift))

            # preparing data for character based display using pi3d.PointText, controlled by OWM_NOW_FORMATSTRING
            if ciid not in self.weather.keys():
                self.weather[ciid] = {}
                self.weather[ciid]['desc'] = {}
            self.weather[ciid]['city'] = city
            self.weather[ciid]['temp'] = temp
            self.weather[ciid]['felt'] = felt
            self.weather[ciid]['tmin'] = tmin
            self.weather[ciid]['tmax'] = tmax
            self.weather[ciid]['pres'] = pres
            self.weather[ciid]['humi'] = humi
            self.weather[ciid]['tztx'] = tztx
            self.weather[ciid]['oset'] = oset
            self.weather[ciid]['sris'] = sris
            self.weather[ciid]['sset'] = sset
            self.weather[ciid]['desc'][req_lang] = desc
            self.weather[ciid]['lclt'] = lclt
            self.weather[ciid]['ltba'] = ltba
            self.weather[ciid]['wift'] = wift
            self.weather[ciid]['long'] = long
            self.weather[ciid]['lati'] = lati
            self.weather[ciid]['mris'] = mris
            self.weather[ciid]['mset'] = mset
            self.weather[ciid]['mico'] = mico

            # preparing data for expansion into libreoffice based .odt templates using pi3d.Texture,
            # controlled by PIC_LIBREOFFICE_TEMPLATE_NOW_*
            # expanding {city}, {local_time}, {local_time_thba}, {description}, {icon_only}, {sunrise}, {sunset},
            # {tz}, {temp}, {temp_felt}, {temp_min}, {temp_max}, {pressure}, {humidity}
            idx_list = {'city': 'city', 'temp': 'temp', 'temp_felt': 'felt', 'temp_min': 'tmin', 'temp_max': 'tmax',
                        'pressure': 'pres',
                        'humidity': 'humi', 'sunrise': 'sris', 'sunset': 'sset', 'local_time': 'lclt',
                        'local_time_thba': 'ltba', 'wift': 'wift',
                        'moon_icon': 'mico', 'moonrise': 'mris', 'moonset': 'mset', 'longitude': 'long',
                        'latitude': 'lati'}
            # fill in form city123456, temp123456, ... has disadvantage that template needs to be modified when
            # city ID (123456) is changing
            for idx in idx_list.keys():
                ind_cid = '{}{:06d}'.format(idx, ciid)  # fill old fashioned style: city123456, temp123456
                # fill more flexible style: city_0, temp_0 for 1st place, city_1, temp_1, ... for 2nd place
                ind_seq = '{}_{}'.format(idx, self.libroffice_num_order.index(str(ciid)))
                self.weather_template_values[ind_cid] = chr(self.weather[ciid][idx_list[idx]]) if idx in ['wift'] else \
                    self.weather[ciid][idx_list[idx]]
                self.weather_template_values[ind_seq] = chr(self.weather[ciid][idx_list[idx]]) if idx in ['wift'] else \
                    self.weather[ciid][idx_list[idx]]

    # request url1: http://api.openweathermap.org/data/2.5/group?units=metric&id=1120449&lang=th&APPID=xxx
    # request url2:  https://api.openweathermap.org/data/2.5/forecast?id=2657896&appid=xxx&units=metric&lang=de
    # url1: get current weather from city_id, url2: get 5d weather in 3h intervals
    # both url return json with (among other things) the below weather information
    # map_owm_wi takes both id and icon information to return a corresponding erikflowers/weather-icons
    # return:
    #   "weather": [
    #       {
    #           "main": "Clouds",
    #           "id": 804,
    #           "icon": "04d",
    #           "description": "whatever"
    #       }
    def map_owm_wi(self, id, icon):
        owm2wi = {
            'wi-owm-200': 0xf01e, 'wi-owm-201': 0xf01e, 'wi-owm-202': 0xf01e, 'wi-owm-210': 0xf016,
            'wi-owm-211': 0xf016, 'wi-owm-212': 0xf016, 'wi-owm-221': 0xf016, 'wi-owm-230': 0xf01e,
            'wi-owm-231': 0xf01e, 'wi-owm-232': 0xf01e, 'wi-owm-300': 0xf01c, 'wi-owm-301': 0xf01c,
            'wi-owm-302': 0xf019, 'wi-owm-310': 0xf017, 'wi-owm-311': 0xf019, 'wi-owm-312': 0xf019,
            'wi-owm-313': 0xf01a, 'wi-owm-314': 0xf019, 'wi-owm-321': 0xf01c, 'wi-owm-500': 0xf01c,
            'wi-owm-501': 0xf019, 'wi-owm-502': 0xf019, 'wi-owm-503': 0xf019, 'wi-owm-504': 0xf019,
            'wi-owm-511': 0xf017, 'wi-owm-520': 0xf01a, 'wi-owm-521': 0xf01a, 'wi-owm-522': 0xf01a,
            'wi-owm-531': 0xf01d, 'wi-owm-600': 0xf01b, 'wi-owm-601': 0xf01b, 'wi-owm-602': 0xf0b5,
            'wi-owm-611': 0xf017, 'wi-owm-612': 0xf017, 'wi-owm-615': 0xf017, 'wi-owm-616': 0xf017,
            'wi-owm-620': 0xf017, 'wi-owm-621': 0xf01b, 'wi-owm-622': 0xf01b, 'wi-owm-701': 0xf014,
            'wi-owm-711': 0xf062, 'wi-owm-721': 0xf0b6, 'wi-owm-731': 0xf063, 'wi-owm-741': 0xf014,
            'wi-owm-761': 0xf063, 'wi-owm-762': 0xf063, 'wi-owm-771': 0xf011, 'wi-owm-781': 0xf056,
            'wi-owm-800': 0xf00d, 'wi-owm-801': 0xf011, 'wi-owm-802': 0xf011, 'wi-owm-803': 0xf012,
            'wi-owm-804': 0xf013, 'wi-owm-900': 0xf056, 'wi-owm-901': 0xf01d, 'wi-owm-902': 0xf073,
            'wi-owm-903': 0xf076, 'wi-owm-904': 0xf072, 'wi-owm-905': 0xf021, 'wi-owm-906': 0xf015,
            'wi-owm-957': 0xf050, 'wi-owm-day-200': 0xf010, 'wi-owm-day-201': 0xf010, 'wi-owm-day-202': 0xf010,
            'wi-owm-day-210': 0xf005, 'wi-owm-day-211': 0xf005, 'wi-owm-day-212': 0xf005, 'wi-owm-day-221': 0xf005,
            'wi-owm-day-230': 0xf010, 'wi-owm-day-231': 0xf010, 'wi-owm-day-232': 0xf010, 'wi-owm-day-300': 0xf00b,
            'wi-owm-day-301': 0xf00b, 'wi-owm-day-302': 0xf008, 'wi-owm-day-310': 0xf008, 'wi-owm-day-311': 0xf008,
            'wi-owm-day-312': 0xf008, 'wi-owm-day-313': 0xf008, 'wi-owm-day-314': 0xf008, 'wi-owm-day-321': 0xf00b,
            'wi-owm-day-500': 0xf00b, 'wi-owm-day-501': 0xf008, 'wi-owm-day-502': 0xf008, 'wi-owm-day-503': 0xf008,
            'wi-owm-day-504': 0xf008, 'wi-owm-day-511': 0xf006, 'wi-owm-day-520': 0xf009, 'wi-owm-day-521': 0xf009,
            'wi-owm-day-522': 0xf009, 'wi-owm-day-531': 0xf00e, 'wi-owm-day-600': 0xf00a, 'wi-owm-day-601': 0xf0b2,
            'wi-owm-day-602': 0xf00a, 'wi-owm-day-611': 0xf006, 'wi-owm-day-612': 0xf006, 'wi-owm-day-615': 0xf006,
            'wi-owm-day-616': 0xf006, 'wi-owm-day-620': 0xf006, 'wi-owm-day-621': 0xf00a, 'wi-owm-day-622': 0xf00a,
            'wi-owm-day-701': 0xf003, 'wi-owm-day-711': 0xf062, 'wi-owm-day-721': 0xf0b6, 'wi-owm-day-731': 0xf063,
            'wi-owm-day-741': 0xf003, 'wi-owm-day-761': 0xf063, 'wi-owm-day-762': 0xf063, 'wi-owm-day-781': 0xf056,
            'wi-owm-day-800': 0xf00d, 'wi-owm-day-801': 0xf000, 'wi-owm-day-802': 0xf000, 'wi-owm-day-803': 0xf000,
            'wi-owm-day-804': 0xf00c, 'wi-owm-day-900': 0xf056, 'wi-owm-day-902': 0xf073, 'wi-owm-day-903': 0xf076,
            'wi-owm-day-904': 0xf072, 'wi-owm-day-906': 0xf004, 'wi-owm-day-957': 0xf050, 'wi-owm-night-200': 0xf02d,
            'wi-owm-night-201': 0xf02d, 'wi-owm-night-202': 0xf02d, 'wi-owm-night-210': 0xf025,
            'wi-owm-night-211': 0xf025, 'wi-owm-night-212': 0xf025, 'wi-owm-night-221': 0xf025,
            'wi-owm-night-230': 0xf02d, 'wi-owm-night-231': 0xf02d,
            'wi-owm-night-232': 0xf02d, 'wi-owm-night-300': 0xf02b, 'wi-owm-night-301': 0xf02b,
            'wi-owm-night-302': 0xf028, 'wi-owm-night-310': 0xf028, 'wi-owm-night-311': 0xf028,
            'wi-owm-night-312': 0xf028, 'wi-owm-night-313': 0xf028,
            'wi-owm-night-314': 0xf028, 'wi-owm-night-321': 0xf02b, 'wi-owm-night-500': 0xf02b,
            'wi-owm-night-501': 0xf028, 'wi-owm-night-502': 0xf028, 'wi-owm-night-503': 0xf028,
            'wi-owm-night-504': 0xf028, 'wi-owm-night-511': 0xf026,
            'wi-owm-night-520': 0xf029, 'wi-owm-night-521': 0xf029, 'wi-owm-night-522': 0xf029,
            'wi-owm-night-531': 0xf02c, 'wi-owm-night-600': 0xf02a, 'wi-owm-night-601': 0xf0b4,
            'wi-owm-night-602': 0xf02a, 'wi-owm-night-611': 0xf026,
            'wi-owm-night-612': 0xf026, 'wi-owm-night-615': 0xf026, 'wi-owm-night-616': 0xf026,
            'wi-owm-night-620': 0xf026, 'wi-owm-night-621': 0xf02a, 'wi-owm-night-622': 0xf02a,
            'wi-owm-night-701': 0xf04a, 'wi-owm-night-711': 0xf062,
            'wi-owm-night-721': 0xf0b6, 'wi-owm-night-731': 0xf063, 'wi-owm-night-741': 0xf04a,
            'wi-owm-night-761': 0xf063, 'wi-owm-night-762': 0xf063, 'wi-owm-night-781': 0xf056,
            'wi-owm-night-800': 0xf02e, 'wi-owm-night-801': 0xf022,
            'wi-owm-night-802': 0xf022, 'wi-owm-night-803': 0xf022, 'wi-owm-night-804': 0xf086,
            'wi-owm-night-900': 0xf056, 'wi-owm-night-902': 0xf073, 'wi-owm-night-903': 0xf076,
            'wi-owm-night-904': 0xf072, 'wi-owm-night-906': 0xf024,
            'wi-owm-night-957': 0xf050}

        owm_gen = list(filter(lambda x: re.search('wi-owm-.*{:d}'.format(id), x), owm2wi.keys()))
        owm_night = list(filter(lambda x: re.search('wi-owm-night-.*{:d}'.format(id), x), owm2wi.keys()))
        owm_day = list(filter(lambda x: re.search('wi-owm-day-.*{:d}'.format(id), x), owm2wi.keys()))
        self.log.debug("owm_gen: {}, owm_night: {}, owm_day: {}".format(owm_gen, owm_night, owm_day))
        wi_icon = -1
        if len(owm_gen) == 1:
            self.log.warning('found matching icon')
        elif len(owm_gen) > 1:
            hint = 'weather icons (icons indicated in owm_gen, owm_night and owm_day)'
            self.log.debug("must choose from {} {}".format(len(owm_gen), hint))
            if icon[-1] == 'n' and len(owm_night) == 1:
                #       owm_night = list(filter(lambda x: re.search('night', x), owm_gen))
                wi_icon = owm_night[0]
            if icon[-1] == 'd' and len(owm_day) == 1:
                wi_icon = owm_day[0]
        self.log.debug("selected wi-weather icon code: {}".format(wi_icon))
        return owm2wi[wi_icon]

    def order_cities_by_lang(self):
        self.city_ids_by_lang = {}
        for c in self.OWM_CITY_IDS:
            m = re.search(r'(^\d{7}):(.*)', c)
            if m:
                city = int(m.group(1))
                for lang in m.group(2).split('+'):
                    if lang in self.city_ids_by_lang.keys():
                        self.city_ids_by_lang[lang].append(city)  # = cities_by_lang[lang].append(city)
                    else:
                        self.city_ids_by_lang[lang] = [city]

    def get_config(self, config):
        self.OWM_NOW_RETRIEVE_LOCAL_WEATHER = pfc.get_config_param(self.config, 'OWM_NOW_RETRIEVE_LOCAL_WEATHER')
        self.OWM_NOW_FORMATSTRING = pfc.get_config_param(self.config, 'OWM_NOW_FORMATSTRING')
        self.OWM_NOW_LIBREOFFICE_TEMPLATE_USE = pfc.get_config_param(self.config, 'OWM_NOW_LIBREOFFICE_TEMPLATE_USE')
        if self.OWM_NOW_FORMATSTRING == 'off' and self.OWM_NOW_LIBREOFFICE_TEMPLATE_USE == 'off':
            self.OWM_NOW_RETRIEVE_LOCAL_WEATHER = False
            self.log.warning(
                "OWM_NOW_FORMATSTRING and OWM_NOW_LIBREOFFICE_TEMPLATE_USE set to 'off', setting OWM_NOW_RETRIEVE_LOCAL_WEATHER=False")

        if self.OWM_NOW_RETRIEVE_LOCAL_WEATHER:
            self.OWM_CITY_IDS = pfc.get_config_param(self.config, 'OWM_CITY_IDS')
            if isinstance(self.OWM_CITY_IDS, str):
                self.OWM_CITY_IDS = [self.OWM_CITY_IDS]
            self.OWM_NOW_BASE_URL = pfc.get_config_param(self.config, 'OWM_NOW_BASE_URL')
            self.OWM_API_KEY = pfc.get_config_param(self.config, 'OWM_API_KEY')
            self.OWM_UNITS = pfc.get_config_param(self.config, 'OWM_UNITS')
            self.OWM_NOW_BASE_URL = pfc.get_config_param(self.config, 'OWM_NOW_BASE_URL')
            self.OWM_NOW_CITY_DTFORMAT = pfc.get_config_param(self.config, 'OWM_NOW_CITY_DTFORMAT')
            self.OWM_SUNRISE_SUNSET_DTFORMAT = pfc.get_config_param(self.config, 'OWM_SUNRISE_SUNSET_DTFORMAT')
            self.OWM_THAI_BA_DTFORMAT = pfc.get_config_param(self.config, 'OWM_THAI_BA_DTFORMAT')
            self.OWM_NOW_REFRESH_RATE = pfc.get_config_param(self.config, 'OWM_NOW_REFRESH_RATE')
            self.OWM_NOW_LIBREOFFICE_TEMPLATE_IN = pfc.get_config_param(self.config, 'OWM_NOW_LIBREOFFICE_TEMPLATE_IN')
            self.OWM_NOW_LIBREOFFICE_PRINT_READY = pfc.get_config_param(self.config, 'OWM_NOW_LIBREOFFICE_PRINT_READY')
            self.OWM_NOW_REFRESH_RATE = pfc.get_config_param(self.config, 'OWM_NOW_REFRESH_RATE')
            self.OWM_LIBREOFFICE_PNG_CONVERT_CMD = pfc.get_config_param(self.config, 'OWM_LIBREOFFICE_PNG_CONVERT_CMD')
            self.OWM_NOW_FORMATSTRING_CONCATENATE = pfc.get_config_param(self.config, 'OWM_NOW_FORMATSTRING_CONCATENATE')
            self.OWM_NOW_LIBREOFFICE_BITMAP_OUT = pfc.get_config_param(self.config, 'OWM_NOW_LIBREOFFICE_BITMAP_OUT')
            self.OWM_SCIS_BMP_DIR = pfc.get_config_param(self.config, 'OWM_SCIS_BMP_DIR')
            self.OWM_NOW_FORMATSTRING_USE = pfc.get_config_param(self.config, 'OWM_NOW_FORMATSTRING_USE')
            self.libroffice_num_order = list(
                map(lambda x: x[:7], self.OWM_CITY_IDS))  # assign _0, _1 to city_0, temp_0,...
            if not os.path.isfile(self.OWM_NOW_LIBREOFFICE_PRINT_READY):
                dir_path = os.path.dirname(self.OWM_NOW_LIBREOFFICE_PRINT_READY)
                if not os.path.isdir(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                shutil.copy(self.OWM_NOW_LIBREOFFICE_TEMPLATE_IN, self.OWM_NOW_LIBREOFFICE_PRINT_READY)
        else:
            self.log.warning("OWM_NOW_RETRIEVE_LOCAL_WEATHER set to false, quit openweathermap.org retrieval")

    def getWeatherTemplateFromLibreOffice(self):
        # extract 'content.xml' from self.OWM_NOW_LIBREOFFICE_TEMPLATE_IN
        with zipfile.ZipFile(self.OWM_NOW_LIBREOFFICE_TEMPLATE_IN, "r") as liboff_doc:
            with liboff_doc.open('content.xml') as myfile:
                # expanding {city}, {local_time}, {local_time_thba}, {description}, {icon_only}, {sunrise}, {sunset},
                # {tz}, {temp}, {temp_felt}, {temp_min}, {temp_max}, {pressure}, {humidity}
                self.template = myfile.read().decode('utf-8')
        #       template = self.owm.augmentTemplate(template)
        liboff_doc.close()

    def putOwmInfoToLibreOfficeTemplate(self):
        # remove 'content.xml' from within self.OWM_NOW_LIBREOFFICE_PRINT_READY
        try:
            with zipfile.ZipFile(self.OWM_NOW_LIBREOFFICE_TEMPLATE_IN, 'r') as zipread:
                with zipfile.ZipFile(self.OWM_NOW_LIBREOFFICE_PRINT_READY, 'w') as zipwrite:
                    for item in zipread.infolist():
                        if item.filename not in 'content.xml':
                            data = zipread.read(item.filename)
                            zipwrite.writestr(item, data)
        finally:
            self.log.info("successfully updated template OWM_NOW_LIBREOFFICE_PRINT_READY='{}')".format(
                self.OWM_NOW_LIBREOFFICE_PRINT_READY))

        # add content.xml with expansions
        with zipfile.ZipFile(self.OWM_NOW_LIBREOFFICE_PRINT_READY, 'a') as z:
            z.writestr('content.xml', "{}".format(self.template))
        z.close()

    def getWeather(self):
        self.order_cities_by_lang()
        # loop through all cities in all requested languages. Need to complete before we can compose the output string
        # as the weather description is specific to each requested language
        self.weather = {}
        for lang in self.city_ids_by_lang.keys():
            self.log.info("language: {}".format(lang))
            req_url = "{}&id={}&lang={}&APPID={}".format(self.OWM_NOW_BASE_URL,
                                                         ','.join(map(str, self.city_ids_by_lang[lang])), lang,
                                                         self.OWM_API_KEY)
            self.log.info("owm url: {}".format(req_url))
            req = urllib.request.Request(req_url)
            r = urllib.request.urlopen(req).read()
            self.info = json.loads(r.decode('utf-8'))
            if re.match('http://api.openweathermap.org/data/2.5/group', self.OWM_NOW_BASE_URL):
                self.log_owm_group(lang)
            else:
                self.log.error("{} is not implemented".format(self.OWM_NOW_BASE_URL))
                exit(1)
        self.wstring = ""
        self.log.info("  OWM_NOW_FORMATSTRING specification: {}".format(self.OWM_NOW_FORMATSTRING))
        for c in self.OWM_CITY_IDS:
            c = int(re.sub(':.*', '', c))
            self.wstring += "\n" if len(self.wstring) > 0 else ""
            # expanding {city}, {local_time}, {local_time_thba}, {description}, {icon_only}, {sunrise}, {sunset},
            # {tz}, {temp}, {temp_felt}, {temp_min}, {temp_max}, {pressure}, {humidity}
            self.wstring += self.OWM_NOW_FORMATSTRING.format(
                city=self.weather[c]['city'],
                temp=self.weather[c]['temp'],
                temp_felt=self.weather[c]['felt'],
                temp_min=self.weather[c]['tmin'],
                temp_max=self.weather[c]['tmax'],
                pressure=self.weather[c]['pres'],
                humidity=self.weather[c]['humi'],
                sunrise=self.weather[c]['sris'],
                sunset=self.weather[c]['sset'],
                description=chr(self.weather[c]['wift']) + ", ".join(self.weather[c]['desc'].values()),
                icon_only=chr(self.weather[c]['wift']),
                local_time=self.weather[c]['lclt'],
                tz=self.weather[c]['tztx'],
                local_time_thba=self.weather[c]['ltba'],
                moonrise=self.weather[c]['mris'],
                moonset=self.weather[c]['mset'],
                moon_icon=self.weather[c]['mico'])
        if not self.OWM_NOW_FORMATSTRING_CONCATENATE:
            self.wstring = self.wstring.replace('\\n', chr(0x0a))
        else:
            self.wstring = self.wstring.replace('\n', self.OWM_NOW_FORMATSTRING_CONCATENATE)
        self.log.info("  OWM_NOW_FORMATSTRING      expanded: {}".format(self.wstring.replace('\n', '\\n')))
        self.last_run = datetime.datetime.now()
        #   print("xlastrun: {}".format(self.lastrun))
        self.warn_cache = True
        return self.wstring.split('\n')


def wind_speed_to_wi_icon(speed: float, unit: string):
    if unit == 'm/s':
        return wind_speed_to_wi_icon_ms(speed)
    elif unit == 'km/h':
        return wind_speed_to_wi_icon_ms(speed / 3.6)
    elif unit == 'miles/h':
        return wind_speed_to_wi_icon_ms(speed / 2.23694)
    else:
        return None


def wind_speed_to_wi_icon_ms(wind_speed: float):
    # ! Beaufort scale in m/s
    if wind_speed < 0.5:
        return chr(61623)  # 61623 wi-wind-beaufort-0
    elif (wind_speed >= 0.5) and (wind_speed < 1.5):
        return chr(61624)  # 61624 wi-wind-beaufort-1
    elif (wind_speed >= 1.5) and (wind_speed < 3.3):
        return chr(61625)  # 61625 wi-wind-beaufort-2
    elif (wind_speed >= 3.3) and (wind_speed < 5.5):
        return chr(61626)  # 61626 wi-wind-beaufort-3
    elif (wind_speed >= 5.5) and (wind_speed < 7.9):
        return chr(61627)  # 61627 wi-wind-beaufort-4
    elif (wind_speed >= 7.9) and (wind_speed < 10.7):
        return chr(61628)  # 61628 wi-wind-beaufort-5
    elif (wind_speed >= 10.7) and (wind_speed < 13.8):
        return chr(61629)  # 61629 wi-wind-beaufort-6
    elif (wind_speed >= 13.8) and (wind_speed < 17.1):
        return chr(61630)  # 61630 wi-wind-beaufort-7
    elif (wind_speed >= 17.1) and (wind_speed < 20.7):
        return chr(61631)  # 61631 wi-wind-beaufort-8
    elif (wind_speed >= 20.7) and (wind_speed < 24.4):
        return chr(61632)  # 61632 wi-wind-beaufort-9
    elif (wind_speed >= 24.4) and (wind_speed < 28.4):
        return chr(61633)  # 61633 wi-wind-beaufort-10
    elif (wind_speed >= 28.4) and (wind_speed < 32.6):
        return chr(61634)  # 61634 wi-wind-beaufort-11
    elif wind_speed >= 32.6:
        return chr(61635)  # 61635 wi-wind-beaufort-12
    else:
        return None
