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
  --debug
  --host HOST  [default: localhost]
  --port PORT  [default: 8000]
"""
import logging

import docopt
import routemaster

args = docopt.docopt(__doc__)
debug = args['--debug']
host = args['--host']
port = int(args['--port'])
database_file = args['DATABASE_FILE']

if debug:
    # Enable log messages from SQLAlchemy engine
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

logger = logging.getLogger()

logger.info("Initializing database {}".format(database_file))
routemaster.db.initialize_sqlite(database_file)

logger.info("Starting Flask debug server on {host}:{port}".format(
    host=host, port=port))
routemaster.web.app.run(host, port, debug=debug)
