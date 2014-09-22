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
import unittest

import routemaster
from routemaster import web
import sqlalchemy

db_initialized = False


class RMTestCase(unittest.TestCase):
    def setUp(self):
        global db_initialized
        if not db_initialized:
            engine = sqlalchemy.create_engine("sqlite://")
            routemaster.db.SASession.configure(bind=engine)
            routemaster.db.SABase.metadata.create_all(engine)

            # Add a test user
            db = routemaster.db.SASession()
            test = routemaster.db.User(name="Hermann Dorkschneider",
                                       email="fakeaddress@lumeh.org")
            db.add(test)
            db.commit()

        self.app = routemaster.web.app.test_client()


class TestHello(RMTestCase):
    def test_hello(self):
        r = self.app.get("/hello")
        self.assertIn("Hello, world!", str(r.data))


class TestJourney(RMTestCase):
    def test_store_journey(self):
        now = datetime.datetime.utcnow()
        then = now - datetime.timedelta(seconds=30)
        data = {
            "userId": 1,
            "startTime": then.isoformat(),
            "endTime": now.isoformat(),
            "distanceM": 5,
            "efficiency": 20,
            "waypoints": [
                {
                    "time": then.isoformat(),
                    "accuracyM": 2.71,
                    "latitude": 3.14159,
                    "longitude": 1.618,
                    "heightM": 10,
                },
                {
                    "time": now.isoformat(),
                    "accuracyM": 2.71,
                    "latitude": 3.14159,
                    "longitude": 1.618,
                    "heightM": 10,
                },
            ],
        }
        r = self.app.post("/journey", data=data)
        self.assertTrue(r.status.startswith("2"), msg="non-2xx response")


class TestJsonFunctions(RMTestCase):
    def test_camel(self):
        self.assertEqual(web.camel("pepperoni_pizza"), "pepperoniPizza")
        self.assertEqual(web.camel("iphones_are_weird"), "iphonesAreWeird")
        not_a_string = 5
        self.assertRaises(TypeError, web.camel, not_a_string)

    def test_db_to_json(self):
        now = datetime.datetime.utcnow()
        w = routemaster.db.Waypoint(
            id=5,
            journey_id=7,
            time=now,
            accuracy_m=9.04,
            latitude=7.3,
            longitude=2.0,
            height_m=159255230,
        )
        data = json.loads(routemaster.web.db_to_json(w))
        self.assertEqual(data["id"], 5)
        self.assertEqual(data["journeyId"], 7)
        self.assertEqual(data["time"], now.isoformat())
        self.assertEqual(data["accuracyM"], 9.04)
        self.assertEqual(data["latitude"], 7.3)
        self.assertEqual(data["longitude"], 2.0)
        self.assertEqual(data["heightM"], 159255230)
