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
import sys

from os.path import basename
from shutil import which
from subprocess import call, PIPE

from pako.package_format import PackageFormat
from pako.package_manager_data import load_package_manager_data


class PakoManager:
    def __init__(self):
        self.exe, self.config = self._find_package_manager()
        if not self.exe:
            raise RuntimeError('Package manager not found!')

        if self.config['sudo'] and not sys.stdout.isatty():
            raise RuntimeError('Sudo required (and script not launched interactively)')
        self.has_sudo = False

    @staticmethod
    def _find_package_manager():
        for exe, config in load_package_manager_data().items():
            if which(exe):
                return which(exe), config
        return None, {}

    def call(self, args):
        sudo_args = []
        if self.config['sudo']:
            sudo_args = ['sudo']
            if not self.has_sudo:
                if call(['sudo', '-n', 'true'], stderr=PIPE) == 0:  # Check if we have sudo access
                    self.has_sudo = True
                else:
                    print('Requesting sudo to run command: {}...'.format(
                        ' '.join([basename(self.exe)] + args)
                    ))
        return call(sudo_args + [self.exe] + args)

    def update(self):
        return self.call(self.config['update'].split()) == 0

    def install(self, package, fmt=None):
        if not fmt:
            package, fmt = PackageFormat.parse(package)
        if fmt not in PackageFormat.all:
            raise ValueError('Invalid package format: {}. Should be one of: {}'.format(
                fmt, PackageFormat.all
            ))

        possible_names = []
        for format_name, formats in self.config['formats'].items():
            if not fmt or format_name == fmt:
                for f in formats:
                    if f not in possible_names:
                        possible_names.append(f)

        for name in possible_names:
            if self.call(self.config['install'].split() + [name.format(package)]) == 0:
                return True
        return False
