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

"""Database models and helper functions for the RouteMaster server.

Before using this module, one of the initialize_* methods needs to be
called. (Only the first initialize_* method called will have an effect,
so you can safely call them multiple times if you want to.)

After initializing, create an instance of SASession to access the
database.
"""
import datetime
import logging
import os.path

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger("routemaster.db")
SABase = declarative_base()
SASession = sessionmaker()
engine = None

class Journey(SABase):
    """A particular instance of walking from one Place to another"""
    __tablename__ = "journey"
    id = Column(Integer, primary_key=True)
    user = relationship("User", back_populates="journeys")
    user_id = Column(Integer, ForeignKey("user.id"))
    visibility = Column(Enum("public", "friends", "private"))
    start_time_utc = Column(DateTime)
    end_time_utc = Column(DateTime)
    distance_m = Column(Integer)
    efficiency = Column(Integer)
    start_place_id = Column(Integer, ForeignKey("place.id"))
    start_place = relationship("Place", foreign_keys=start_place_id)
    end_place_id = Column(Integer, ForeignKey("place.id"))
    end_place = relationship("Place", foreign_keys=end_place_id)
    waypoints = relationship("Waypoint", back_populates="journey")

    def __repr__(self):
        return ("<Journey id={s.id} user={s.user!r} "
                "start_time_utc={s.start_time_utc!r}>"
                .format(s=self))

class Place(SABase):
    """A named place on the map from which a Journey can start or end"""
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

class Route(SABase):
    """An oft-journeyed pair of Places that has a high score list"""
    __tablename__ = "route"
    id = Column(Integer, primary_key=True)
    start_place_id = Column(Integer, ForeignKey("place.id"))
    start_place = relationship("Place", foreign_keys=start_place_id)
    end_place_id = Column(Integer, ForeignKey("place.id"))
    end_place = relationship("Place", foreign_keys=end_place_id)

    def __repr__(self):
        return ("<Route id={s.id} start_place={s.start_place!r} "
                "end_place={s.end_place!r}>"
                .format(s=self))

class User(SABase):
    """A person who uses RouteMaster"""
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    creation_time_utc = Column(DateTime, default=datetime.datetime.utcnow)
    last_login_time_utc = Column(DateTime)
    total_distance = Column(Integer, default=0)
    journeys = relationship("Journey", back_populates="user")
    external_id = Column(String)

    def __repr__(self):
        return ("<User id={s.id} name={s.name!r} external_id={s.external_id!r}>"
                .format(s=self))

class Waypoint(SABase):
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

def _populate():
    """Insert some default objects into the database.

    This function will throw errors if the database has already been
    populated, so avoid calling it multiple times.
    """
    SABase.metadata.create_all(engine)
    logger.info("Initalized database")
    db = SASession()
    café_chan = Place(name="Café Chan",
                      latitude=29.65782,
                      longitude=-82.34215)
    einstein = Place(name="Einstein Bagels",
                     latitude=29.64814,
                     longitude=-82.34524)
    hermann = User(name="Hermann Dorkschneider",
                   email="fakeaddress@lumeh.org")
    db.add(café_chan)
    db.add(einstein)
    db.add(hermann)
    db.commit()
    logger.info("Created Place {}".format(café_chan))
    logger.info("Created Place {}".format(einstein))
    logger.info("Created User {}".format(hermann))

def initialize_sqlite(database_file):
    """Initialize this module to use an on-disk sqlite database."""
    global engine
    if engine is None:
        # The following line does really have the correct number of slashes;
        # an absolute path would require four total. See
        # http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#sqlite
        engine = create_engine("sqlite:///{}".format(database_file))
        SASession.configure(bind=engine)

        # Populate the database if it doesn't already exist on disk
        if not os.path.exists(database_file):
            _populate()

def initialize_sqlite_memory():
    """Initialize this module to use an in-memory sqlite database."""
    global engine
    if engine is None:
        engine = create_engine("sqlite://")
        SASession.configure(bind=engine)
        _populate()
