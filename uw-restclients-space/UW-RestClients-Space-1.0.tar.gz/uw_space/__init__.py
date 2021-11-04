# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
import logging
from restclients_core.exceptions import DataFailureException
from uw_space.dao import SPACE_DAO
from uw_space.models import Facility

by_code_path = "/space/v1/facility.json?facility_code={}"
by_number_path = "/space/v1/facility/{}.json"
logger = logging.getLogger(__name__)


class Facilities(object):

    def __init__(self):
        self.dao = SPACE_DAO()
        self._read_headers = {"Accept": "application/json"}

    def search_by_code(self, facility_code):
        """
        facility_code: string
        """
        url = by_code_path.format(facility_code)
        response = self.dao.getURL(url, self._read_headers)
        logger.debug(
            {'url': url, 'status': response.status, 'data': response.data})
        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)
        return self.__process_json(json.loads(response.data))

    def search_by_number(self, facility_number):
        """
        facility_number: string
        """
        url = by_number_path.format(facility_number)
        response = self.dao.getURL(url, self._read_headers)
        logger.debug(
            {'url': url, 'status': response.status, 'data': response.data})
        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)
        return Facility.from_json(json.loads(response.data))

    def __process_json(self, json_data):
        objs = []
        facilitys = json_data.get("Facilitys")
        for facility in facilitys:
            furi = facility.get("FacilityURI")
            if furi:
                url = furi.get("Href")
                building_resp = self.dao.getURL(url, self._read_headers)
                if building_resp.status != 200:
                    raise DataFailureException(
                        url, building_resp.status, building_resp.data)
                objs.append(
                    Facility.from_json(json.loads(building_resp.data)))
        return objs
