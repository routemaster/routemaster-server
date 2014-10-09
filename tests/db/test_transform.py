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
        now2 = datetime.datetime.utcnow()
        w2 = Waypoint(
            id=6,
            journey_id=8,
            time_utc=now2,
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
        self.assertEqual(d2["timeUtc"], now2.isoformat())
        self.assertEqual(d2["accuracyM"], 10.04)
        self.assertEqual(d2["latitude"], 8.3)
        self.assertEqual(d2["longitude"], 3.0)
        self.assertEqual(d2["heightM"], 159255231)
