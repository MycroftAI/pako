# Copyright (c) 2019 Mycroft AI, Inc.
#
# This file is part of Mycroft Skills Manager
# (see https://github.com/MatthewScholefield/mycroft-light).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import appdirs
import json
from logging import getLogger
from os import makedirs
from os.path import join, isfile


def recursive_merge(a, b):
    """Returns a generator for the merged dict of a and b"""
    for k in set(a.keys()) | set(b.keys()):
        if k in a and k in b:
            if isinstance(a[k], dict) and isinstance(b[k], dict):
                yield k, dict(recursive_merge(a[k], b[k]))
            else:
                yield k, b[k]
        elif k in a:
            yield k, a[k]
        else:
            yield k, b[k]


def load_package_managers_overrides() -> dict:
    """Load the optional package manager data overrides from disk"""
    pako_config = appdirs.user_config_dir('pako')
    config_file = join(pako_config, 'pako.conf')
    makedirs(pako_config, exist_ok=True)

    if not isfile(config_file):
        from pako.package_manager_data import get_package_manager_names
        with open(config_file, 'w') as f:
            json.dump({i: {} for i in get_package_manager_names()}, f)
    try:
        with open(config_file) as f:
            custom_config = json.load(f)
    except ValueError:
        getLogger(__name__).warning('Failed to load config file')
        custom_config = {}

    return custom_config
