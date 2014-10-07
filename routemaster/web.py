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
import re

import flask
from flask import g
from flask import request

from .db import Journey
from .db import Place
from .db import Route
from .db import SASession
from .db import User
from .db import Waypoint

app = flask.Flask("routemaster")

def camel(s):
    return re.sub(r"_(.)?", lambda m: (m.group(1) or "").upper(), s)

def db_response(db_objects):
    return json_response(db_to_json(db_objects))

def db_to_json(objects):
    is_a_list = isinstance(objects, list)
    if not is_a_list:
        objects = [objects]
    data = []
    for obj in objects:
        obj_dict = {}
        for column in obj.__table__.columns:
            value = getattr(obj, column.name)
            if isinstance(value, (datetime.date, datetime.datetime)):
                value = value.isoformat()
            obj_dict[camel(column.name)] = value
        data.append(obj_dict)
    return json.dumps(data[0] if not is_a_list else data,
                      indent=2, ensure_ascii=False)

def get_or_404(type, **kwargs):
    q = g.db.query(type).filter_by(**kwargs).first()
    if not q:
        flask.abort(404)
    return q

def json_response(s):
    response = flask.make_response(s)
    response.headers["content-type"] = "application/json; charset=utf-8"
    return response

@app.before_request
def setup_db_session():
    g.db = SASession()


@app.route("/hello")
def hello():
    return json_response(json.dumps({"error": "Hello, world!"}))


@app.route("/journey", methods=["POST"])
def store_journey():
    data = request.json
    journey = Journey(
        user_id=data['userId'],
        start_time_utc=data['startTimeUtc'],
        end_time_utc=data['endTimeUtc'],
        start_place_id=data['startPlaceId'],
        end_place_id=data['endPlaceId'],
    )
    g.db.add(journey)

    waypoints = []
    for w in data['waypoints']:
        waypoint = Waypoint(
            journey=journey,
            time_utc=w['timeUtc'],
            accuracy_m=w['accuracyM'],
            latitude=w['latitude'],
            longitude=w['longitude'],
            height_m=w['height_m'],
        )
        g.db.add(waypoint)
        waypoints.append(waypoint)

    if len(waypoints) < 3:
        # return 400 Bad Request?
        ...
    g.db.commit()

    # TODO: Calculate journey scores and distance
    for w1, w2 in zip(waypoints, waypoints[1:]):
        ...

    g.db.commit()
    return db_response(journey)

@app.route("/journey/<int:jid>")
def get_journey(jid):
    return db_response(get_or_404(Journey, id=jid))


@app.route("/place/<int:pid>")
def get_place(pid):
    return db_response(get_or_404(Place, id=pid))


@app.route("/route/<int:rid>")
def get_route(rid):
    return db_response(get_or_404(Route, id=rid))


@app.route("/user/<int:uid>")
def get_user(uid):
    return db_response(get_or_404(User, id=uid))

@app.route("/user/<int:uid>/recent")
def get_user_recent_journeys(uid):
    query = (g.db.query(Journey).filter_by(user_id=uid)
             .order_by(desc(Journey.start_time_utc)))
    return db_response(query.all())
