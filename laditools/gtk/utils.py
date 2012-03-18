#!/usr/bin/python
# LADITools - Linux Audio Desktop Integration Tools
# Copyright (C) 2011-2012 Alessio Treglia <quadrispro@ubuntu.com>
# Copyright (C) 2007-2010, Marc-Olivier Barre <marco@marcochapeau.org>
# Copyright (C) 2007-2010, Nedko Arnaudov <nedko@arnaudov.name>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

def find_data_file(path):
    start_dir = os.path.dirname(sys.argv[0])

    if not start_dir:
        start_dir = "."

    paths = [
        os.path.join(sys.path[0], 'data', path),
        os.path.join(sys.path[0], 'data', 'icons', path),
        os.path.join(sys.prefix, 'share', 'icons', 'hicolor', path),
        os.path.join(sys.prefix, 'share', 'laditools', path),
        os.path.join(sys.prefix, 'share', 'laditools', 'data', path),
        ]

    for path in paths:
        #print 'Checking "%s"...' % path
        if os.path.isfile(path):
            #print 'Found data file in "%s"' % path
            return path

    raise Exception('Data file "%s" not found' % path)
