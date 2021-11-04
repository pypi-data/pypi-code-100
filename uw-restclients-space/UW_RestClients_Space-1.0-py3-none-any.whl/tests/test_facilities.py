# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from restclients_core.exceptions import DataFailureException
from uw_space import Facilities
from uw_space.utils import fdao_space_override

data = {
    'code': 'MEB',
    'last_updated': '2021-03-27 04:53:09',
    'latitude': '47.653693',
    'longitude': '-122.304747',
    'name': 'Mechanical Engineering Building',
    'number': '1347',
    'site': 'Seattle Main Campus',
    'type': 'Building'
    }


@fdao_space_override
class TestSpace(TestCase):
    def test_search_by_code(self):
        fac = Facilities().search_by_code("MEB")
        self.assertEqual(len(fac), 1)
        self.assertEqual(fac[0].json_data(), data)

        self.assertRaises(
            DataFailureException,
            Facilities().search_by_code, "None"
        )

    def test_search_by_number(self):
        fac = Facilities().search_by_number("1347")
        self.assertEqual(fac.json_data(), data)

        self.assertRaises(
            DataFailureException,
            Facilities().search_by_number, "0"
        )
