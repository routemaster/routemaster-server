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

from routemaster import algorithm
from routemaster.db.models import Waypoint
from routemaster.testing import RMTestCase

class TestAlgorithms(RMTestCase):
    w0 = Waypoint(latitude=0, longitude=0)
    w1 = Waypoint(latitude=0, longitude=1)
    w2 = Waypoint(latitude=2, longitude=3)
    ll01 = (0, 0, 0, 1)
    ll12 = (0, 1, 2, 3)
    distance12 = 314474
    efficiency012 = 78

    def test_distance_between_m(self):
        self.assertEqual(int(algorithm.distance_between_m(0, 0, 0, 0)), 0)
        self.assertEqual(int(algorithm.distance_between_m(*self.ll12)),
                         self.distance12)

    def test_path_length_m(self):
        self.assertEqual(algorithm.path_length_m(self.w1, self.w2),
                         algorithm.distance_between_m(*self.ll12))
        self.assertEqual(algorithm.path_length_m(self.w0, self.w1, self.w2),
                         (algorithm.distance_between_m(*self.ll01) +
                          algorithm.distance_between_m(*self.ll12)))

    def test_journey_scores(self):
        self.assertEqual(algorithm.journey_scores([self.w0, self.w0]),
                         (0, 0.0))
        self.assertEqual(algorithm.journey_scores([self.w1, self.w2])[0], 100)
        self.assertEqual(int(algorithm.journey_scores([self.w1, self.w2])[1]),
                         self.distance12)
        self.assertEqual(algorithm.journey_scores([self.w0, self.w1, self.w2])[0],
                         self.efficiency012)
