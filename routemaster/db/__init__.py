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

After initializing, create an instance of Session to access the
database.
"""
import logging
import os.path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import models

logger = logging.getLogger("routemaster.db")
Session = sessionmaker()
engine = None

def _populate():
    """Insert some default objects into the database.

    This function will throw errors if the database has already been
    populated, so avoid calling it multiple times.
    """
    models.Base.metadata.create_all(engine)
    logger.info("Initalized database")
    db = Session()
    café_chan = models.Place(name="Café Chan",
                             latitude=29.65782,
                             longitude=-82.34215)
    einstein = models.Place(name="Einstein Bagels",
                            latitude=29.64814,
                            longitude=-82.34524)
    hermann = models.Account(name="Hermann Dorkschneider",
                          email="fakeaddress@lumeh.org")
    db.add(café_chan)
    db.add(einstein)
    db.add(hermann)
    db.commit()
    logger.info("Created Place {}".format(café_chan))
    logger.info("Created Place {}".format(einstein))
    logger.info("Created Account {}".format(hermann))

def initialize_sqlite(database_file):
    """Initialize this module to use an on-disk sqlite database."""
    global engine
    if engine is None:
        # The following line does really have the correct number of slashes;
        # an absolute path would require four total. See
        # http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#sqlite
        engine = create_engine("sqlite:///{}".format(database_file))
        Session.configure(bind=engine)

        # Populate the database if it doesn't already exist on disk
        if not os.path.exists(database_file):
            _populate()

def initialize_sqlite_memory():
    """Initialize this module to use an in-memory sqlite database."""
    global engine
    if engine is None:
        engine = create_engine("sqlite://")
        Session.configure(bind=engine)
        _populate()
