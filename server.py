#!/usr/bin/env python3
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
"""
usage: server.py [--debug] [--host HOST] [--port PORT] DATABASE_FILE

Options:
  --host HOST  [default: localhost]
  --port PORT  [default: 8000]
  --debug      Run with Flask in debug mode
"""
import logging
import os.path

import docopt
import routemaster
import sqlalchemy
import tornado.httpserver
import tornado.wsgi

args = docopt.docopt(__doc__)
host = args['--host']
port = int(args['--port'])
debug = args['--debug']
database_file = args['DATABASE_FILE']

# Configure logging
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt='{levelname}:{name}:{message}',
                                       style='{'))
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Enable log messages from SQLAlchemy engine in debug mode
if debug:
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# The following line does really have the correct number of slashes;
# an absolute path would require four total. See
# http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#sqlite
engine = sqlalchemy.create_engine('sqlite:///{}'.format(database_file))
routemaster.db.SASession.configure(bind=engine)

# Initialize database if it doesn't exist
if not os.path.exists(database_file):
    logger.info("Initializing database {}".format(database_file))
    routemaster.db.SABase.metadata.create_all(engine)
    logger.info("Initalized database")

    db = routemaster.db.SASession()
    test = routemaster.db.User(name="Hermann Dorkschneider",
                               email="fakeaddress@lumeh.org")
    db.add(test)
    db.commit()
    logger.info("Created test user {}".format(test))

if debug:
    logger.info("Starting Flask debug server on {host}:{port}".format(
        host=host, port=port))
    routemaster.web.app.run(host, port, debug=True)
else:
    logger.info("Starting Tornado server on {host}:{port}".format(
        host=host, port=port))
    wsgi_container = tornado.wsgi.WSGIContainer(routemaster.web.app)
    http_server = tornado.httpserver.HTTPServer(wsgi_container)
    http_server.bind(port, host)
    http_server.start(0)
    tornado.ioloop.IOLoop.instance().start()
