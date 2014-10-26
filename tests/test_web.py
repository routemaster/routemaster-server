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

def post_journey(app, account_id=1, start_datetime=None, stop_datetime=None):
    if start_datetime is None and stop_datetime is None:
        start_datetime = datetime.datetime.utcnow()
        stop_datetime = start_datetime + datetime.timedelta(seconds=30)

    data = {
        "startTimeUtc": start_datetime.isoformat(),
        "stopTimeUtc": stop_datetime.isoformat(),
        "visibility": "private",
        "waypoints": [
            {
                "timeUtc": start_datetime.isoformat(),
                "accuracyM": 2.71,
                "latitude": 3.1416,
                "longitude": 1.618,
                "heightM": 10,
            },
            {
                "timeUtc": stop_datetime.isoformat(),
                "accuracyM": 2.71,
                "latitude": 3.14159,
                "longitude": 1.618,
                "heightM": 10,
            },
        ],
    }
    r = app.post("/journey", data=json.dumps(data),
                 content_type="application/json", charset="utf-8")
    assert r.status.startswith("2")
    data = json.loads(r.get_data(True))
    return int(data["id"])

class TestAccount(RMTestCase):
    test_account_id = 1

    def setUp(self):
        super().setUp()
        post_journey(self.app, account_id=self.test_account_id)

    def test_get_account(self):
        r = self.app.get("/account/%s" % self.test_account_id)
        self.assertIn("Hermann Dorkschneider", r.get_data(True))

    def test_get_account_recent(self):
        r = self.app.get("/account/%s/recent" % self.test_account_id)
        self.assertIn("startTimeUtc", r.get_data(True))
        self.assertIn("stopPlaceId", r.get_data(True))


class TestHello(RMTestCase):
    def test_hello(self):
        r = self.app.get("/hello")
        self.assertIn("Hello, world!", str(r.data))


class TestJourney(RMTestCase):
    def test_store_and_get_journey(self):
        now = datetime.datetime.utcnow()
        then = now - datetime.timedelta(seconds=30)
        jid = post_journey(self.app, start_datetime=then, stop_datetime=now)

        r = self.app.get("/journey/%s" % jid)
        assert r.status.startswith("2")
        data = r.get_data(True)
        self.assertIn(then.isoformat(), data)
        self.assertIn("private", data)
        # Make sure it includes the waypoints
        self.assertIn("waypoints", data)
        self.assertIn("3.14159", data)
        self.assertIn("3.1416", data)


class TestPlace(RMTestCase):
    def test_get_place(self):
        r = self.app.get("/place/1")
        assert r.status.startswith("2")
        self.assertIn("Café Chan", r.get_data(True))

        r = self.app.get("/place/2")
        assert r.status.startswith("2")
        self.assertIn("Einstein Bagels", r.get_data(True))
