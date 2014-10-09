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
import re

def camel(s):
    return re.sub(r"_(.)?", lambda m: (m.group(1) or "").upper(), s)

def to_dict(db_object):
    """Transform an object from SQLAlchemy into a dict"""
    obj_dict = {}
    for column in db_object.__table__.columns:
        value = getattr(db_object, column.name)
        if isinstance(value, (datetime.date, datetime.datetime)):
            value = value.isoformat()
        obj_dict[camel(column.name)] = value
    return obj_dict

def to_list(db_objects):
    return list(map(to_dict, db_objects))
