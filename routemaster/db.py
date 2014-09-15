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

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SABase = declarative_base()
SASession = sessionmaker()

class Journey(SABase):
    """A particular instance of walking from one location to another"""
    __tablename__ = "journey"
    id = Column(Integer, primary_key=True)
    user = relationship("User", back_populates="journeys")
    user_id = Column(Integer, ForeignKey("user.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    distance_m = Column(Integer)
    efficiency = Column(Integer)
    start_location_id = Column(Integer, ForeignKey("location.id"))
    start_location = relationship("Location", foreign_keys=start_location_id)
    end_location_id = Column(Integer, ForeignKey("location.id"))
    end_location = relationship("Location", foreign_keys=end_location_id)
    waypoints = relationship("Waypoint", back_populates="journey")

    def __repr__(self):
        return ("<Journey id={s.id} user={s.user!r} "
                "start_time={s.start_time!r}>"
                "".format(s=self))

class Location(SABase):
    """A named place on the map from which a journey can start or end"""
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Float)
    external_id = Column(String)

    def __repr__(self):
        return ("<Location id={s.id} name={s.name!r} "
                "external_id={s.external_id!r}>"
                "".format(s=self))

class Route(SABase):
    """An oft-journeyed pair of locations that has a high score list"""
    __tablename__ = "route"
    id = Column(Integer, primary_key=True)
    start_location_id = Column(Integer, ForeignKey("location.id"))
    start_location = relationship("Location", foreign_keys=start_location_id)
    end_location_id = Column(Integer, ForeignKey("location.id"))
    end_location = relationship("Location", foreign_keys=end_location_id)

    def __repr__(self):
        return ("<Route id={s.id} start_location={s.start_location!r} "
                "end_location={s.end_location!r}>"
                "".format(s=self))

class User(SABase):
    """A person who uses RouteMaster"""
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    creation_time = Column(DateTime, default=datetime.datetime.utcnow)
    last_login_time = Column(DateTime)
    total_distance = Column(Integer, default=0)
    journeys = relationship("Journey", back_populates="user")
    external_id = Column(String)

    def __repr__(self):
        return ("<User id={s.id} name={s.name!r} external_id={s.external_id!r}>"
                "".format(s=self))

class Waypoint(SABase):
    """A single datapoint recorded during a journey"""
    __tablename__ = "waypoint"
    id = Column(Integer, primary_key=True)
    journey_id = Column(Integer, ForeignKey("journey.id"))
    journey = relationship("Journey", back_populates="waypoints")
    time = Column(DateTime)
    accuracy_m = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    height_m = Column(Float)

    def __repr__(self):
        return ("<Waypoint id={s.id} journey={s.journey!r} time={s.time!r}>"
                "".format(s=self))
