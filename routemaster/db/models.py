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
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    creation_time_utc = Column(DateTime, default=datetime.datetime.utcnow)
    last_login_time_utc = Column(DateTime)
    total_distance = Column(Integer, default=0)
    journeys = relationship("Journey", back_populates="account")
    external_id = Column(String)

    def __repr__(self):
        return ("<Account id={s.id} name={s.name!r} "
                "external_id={s.external_id!r}>"
                .format(s=self))

class Journey(Base):
    """A particular instance of walking from one Place to another"""
    __tablename__ = "journey"
    id = Column(Integer, primary_key=True)
    account = relationship("Account", back_populates="journeys")
    account_id = Column(Integer, ForeignKey("account.id"))
    visibility = Column(Enum("public", "friends", "private"))
    start_time_utc = Column(DateTime)
    stop_time_utc = Column(DateTime)
    distance_m = Column(Integer)
    efficiency = Column(Integer)
    start_place_id = Column(Integer, ForeignKey("place.id"))
    start_place = relationship("Place", foreign_keys=start_place_id)
    stop_place_id = Column(Integer, ForeignKey("place.id"))
    stop_place = relationship("Place", foreign_keys=stop_place_id)
    waypoints = relationship("Waypoint", back_populates="journey")

    _to_list_attrs = ['waypoints']

    def __repr__(self):
        return ("<Journey id={s.id} account={s.account!r} "
                "start_time_utc={s.start_time_utc!r}>"
                .format(s=self))

class Place(Base):
    """A named place on the map from which a Journey can start or stop"""
    __tablename__ = "place"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Float)
    external_id = Column(String)

    def __repr__(self):
        return ("<Place id={s.id} name={s.name!r} "
                "external_id={s.external_id!r}>"
                .format(s=self))

class Route(Base):
    """An oft-journeyed pair of Places that has a high score list"""
    __tablename__ = "route"
    id = Column(Integer, primary_key=True)
    start_place_id = Column(Integer, ForeignKey("place.id"))
    start_place = relationship("Place", foreign_keys=start_place_id)
    stop_place_id = Column(Integer, ForeignKey("place.id"))
    stop_place = relationship("Place", foreign_keys=stop_place_id)

    def __repr__(self):
        return ("<Route id={s.id} start_place={s.start_place!r} "
                "stop_place={s.stop_place!r}>"
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
