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
import json

import routemaster
from routemaster import web
import sqlalchemy

from routemaster.testing import RMTestCase


class TestHello(RMTestCase):
    def test_hello(self):
        r = self.app.get("/hello")
        self.assertIn("Hello, world!", str(r.data))


class TestJourney(RMTestCase):
    def TODO_RENAME_THIS_test_store_journey(self):
        now = datetime.datetime.utcnow()
        then = now - datetime.timedelta(seconds=30)
        data = {
            "userId": 1,
            "startTimeUtc": then.isoformat(),
            "endTimeUtc": now.isoformat(),
            "distanceM": 5,
            "efficiency": 20,
            "waypoints": [
                {
                    "timeUtc": then.isoformat(),
                    "accuracyM": 2.71,
                    "latitude": 3.14159,
                    "longitude": 1.618,
                    "heightM": 10,
                },
                {
                    "timeUtc": now.isoformat(),
                    "accuracyM": 2.71,
                    "latitude": 3.14159,
                    "longitude": 1.618,
                    "heightM": 10,
                },
            ],
        }
        r = self.app.post("/journey", data=json.dumps(data))
        assert r.status.startswith("2")


class TestPlace(RMTestCase):
    def test_get_place(self):
        r = self.app.get("/place/1")
        assert r.status.startswith("2")
        self.assertIn("Café Chan", r.get_data(True))

        r = self.app.get("/place/2")
        assert r.status.startswith("2")
        self.assertIn("Einstein Bagels", r.get_data(True))


class TestUser(RMTestCase):
    def test_get_user(self):
        r = self.app.get("/user/1")
        self.assertIn("Hermann Dorkschneider", r.get_data(True))
