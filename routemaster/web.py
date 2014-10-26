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

import functools
import json

import flask
from flask import g
from flask import request
from sqlalchemy import desc

from .db import Session
from .db.models import Account
from .db.models import Journey
from .db.models import Place
from .db.models import Route
from .db.models import Waypoint
from .db.transform import parse_time
from .db.transform import to_dict
from .db.transform import to_list

app = flask.Flask("routemaster")

def get_account_id(request):
    """Validate the request's session and return the account id.

    If the session is not valid, an exception will be raised.

    Currently this just returns 1 (the test account) every time.
    """
    return 1

def get_or_404(type, **kwargs):
    q = g.db.query(type).filter_by(**kwargs).first()
    if not q:
        flask.abort(404)
    return q

def json_response(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        data = func(*args, **kwargs)
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        response = flask.make_response(json_data)
        response.headers["content-type"] = "application/json; charset=utf-8"
        return response
    return f

@app.before_request
def setup_db_session():
    g.db = Session()


@app.route("/account/<int:aid>")
@json_response
def get_account(aid):
    return to_dict(get_or_404(Account, id=aid))

@app.route("/account/<int:aid>/recent")
@json_response
def get_account_recent(aid):
    query = (g.db.query(Journey).filter_by(account_id=aid)
             .order_by(desc(Journey.start_time_utc)))
    return to_list(query.all())


@app.route("/hello")
@json_response
def hello():
    return {"error": "Hello, world!"}


@app.route("/journey", methods=["POST"])
@json_response
def store_journey():
    data = request.json
    account_id = get_account_id(request)
    journey = Journey(
        account_id=account_id,
        visibility=data['visibility'],
        start_time_utc=parse_time(data['startTimeUtc']),
        stop_time_utc=parse_time(data['stopTimeUtc']),
        start_place_id=data.get('startPlaceId', None),
        stop_place_id=data.get('stopPlaceId', None),
    )
    g.db.add(journey)

    waypoints = []
    for w in data['waypoints']:
        waypoint = Waypoint(
            journey=journey,
            time_utc=parse_time(w['timeUtc']),
            accuracy_m=w['accuracyM'],
            latitude=w['latitude'],
            longitude=w['longitude'],
            height_m=w['heightM'],
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
    return to_dict(journey)

@app.route("/journey/<int:jid>")
@json_response
def get_journey(jid):
    journey = get_or_404(Journey, id=jid)
    journey_dict = to_dict(get_or_404(Journey, id=jid))
    journey_dict['waypoints'] = to_list(journey.waypoints)
    return journey_dict


@app.route("/place/<int:pid>")
@json_response
def get_place(pid):
    return to_dict(get_or_404(Place, id=pid))


@app.route("/route/<int:rid>")
@json_response
def get_route(rid):
    return to_dict(get_or_404(Route, id=rid))
