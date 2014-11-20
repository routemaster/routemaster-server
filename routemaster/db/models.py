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

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
    """A person who uses RouteMaster"""
    __tablename__ = "account"
    id = Column(String, primary_key=True)  # This is a UUID
    name = Column(String)
    email = Column(String)
    creation_time_utc = Column(DateTime, default=datetime.datetime.utcnow)
    last_login_time_utc = Column(DateTime)
    total_distance = Column(Integer, default=0)
    journeys = relationship("Journey", back_populates="account")
    external_id = Column(String)

    def __repr__(self):
        return ("<Account id={s.id!r} name={s.name!r} "
                "external_id={s.external_id!r}>"
                .format(s=self))

class Journey(Base):
    """A particular instance of walking from one place to another"""

    def __init__(self, *args, **kwargs):
        if "visibility" in kwargs:
            kwargs["visibility"] = kwargs["visibility"].upper()
        super().__init__(*args, **kwargs)

    __tablename__ = "journey"
    id = Column(String, primary_key=True)  # This is a UUID
    account = relationship("Account", back_populates="journeys")
    account_id = Column(Integer, ForeignKey("account.id"))
    visibility = Column(Enum("PUBLIC", "FRIENDS", "PRIVATE"))
    start_time_utc = Column(DateTime)
    stop_time_utc = Column(DateTime)
    distance_m = Column(Integer)
    efficiency = Column(Integer)
    start_place_id = Column(String)
    stop_place_id = Column(String)
    waypoints = relationship("Waypoint", back_populates="journey")

    _to_list_attrs = ['waypoints']

    def __repr__(self):
        return ("<Journey id={s.id!r} account={s.account!r} "
                "start_time_utc={s.start_time_utc!r}>"
                .format(s=self))

class Route(Base):
    """An oft-journeyed pair of places that has a high score list"""
    __tablename__ = "route"
    id = Column(Integer, primary_key=True)
    start_place_id = Column(String)
    stop_place_id = Column(String)

    def __repr__(self):
        return ("<Route id={s.id} start_place_id={s.start_place_id!r} "
                "stop_place_id={s.stop_place_id!r}>"
                .format(s=self))

class Waypoint(Base):
    """A single datapoint recorded during a Journey"""
    __tablename__ = "waypoint"
    id = Column(Integer, primary_key=True)
    journey_id = Column(Integer, ForeignKey("journey.id"))
    journey = relationship("Journey", back_populates="waypoints")
    time_utc = Column(DateTime)
    accuracy_m = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    height_m = Column(Float)

    def __repr__(self):
        return ("<Waypoint id={s.id} journey={s.journey!r} "
                "time_utc={s.time_utc!r}>"
                .format(s=self))
