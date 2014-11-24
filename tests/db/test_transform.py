# Copyright 2014 Benjamin Woodruff, Colin Chan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime

from routemaster.db import transform
from routemaster.db.models import Waypoint
from routemaster.testing import RMTestCase


class TestDbTransform(RMTestCase):
    def test_camel(self):
        self.assertEqual(transform.camel("pepperoni_pizza"), "pepperoniPizza")
        self.assertEqual(transform.camel("iphones_are_weird"), "iphonesAreWeird")
        not_a_string = 5
        self.assertRaises(TypeError, transform.camel, not_a_string)

    def test_parse_time(self):
        self.assertEqual(transform.parse_time("2014-10-14T15:03:01.123456"),
                         datetime.datetime(2014, 10, 14, 15, 3, 1, 123456))
        self.assertEqual(transform.parse_time("1776-07-04T00:00:00.000000"),
                         datetime.datetime(1776, 7, 4))

    def test_to_dict_and_to_list(self):
        now1 = datetime.datetime.utcnow()
        w1 = Waypoint(
            id=5,
            journey_id=7,
            time_utc=now1,
            accuracy_m=9.04,
            latitude=7.3,
            longitude=2.0,
            height_m=159255230,
        )
        time2 = "2014-11-17T00:00:00.000000"
        w2 = Waypoint(
            id=6,
            journey_id=8,
            time_utc=transform.parse_time(time2),
            accuracy_m=10.04,
            latitude=8.3,
            longitude=3.0,
            height_m=159255231,
        )
        d1, d2 = transform.to_list([w1, w2])

        self.assertEqual(d1["id"], 5)
        self.assertEqual(d1["journeyId"], 7)
        self.assertEqual(d1["timeUtc"], now1.isoformat())
        self.assertEqual(d1["accuracyM"], 9.04)
        self.assertEqual(d1["latitude"], 7.3)
        self.assertEqual(d1["longitude"], 2.0)
        self.assertEqual(d1["heightM"], 159255230)

        self.assertEqual(d2["id"], 6)
        self.assertEqual(d2["journeyId"], 8)
        self.assertEqual(d2["timeUtc"], time2)
        self.assertEqual(d2["accuracyM"], 10.04)
        self.assertEqual(d2["latitude"], 8.3)
        self.assertEqual(d2["longitude"], 3.0)
        self.assertEqual(d2["heightM"], 159255231)
