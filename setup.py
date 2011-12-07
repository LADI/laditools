#!/usr/bin/env python

# LADITools - Linux Audio Desktop Integration Tools
# setup.py - Setup script for the LADITools suite
# Copyright (C) 2007-2008, Marc-Olivier Barre <marco@marcochapeau.org>
# Copyright (C) 2007-2008, Nedko Arnaudov <nedko@arnaudov.name>
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

from distutils.core import setup

setup(name='laditools',
    version='1.0~rc2',
    description='Linux Audio Desktop Integration Tools',
    author='Marc-Olivier Barre and Nedko Arnaudov',
    author_email='marco@marcochapeau.org',
    url='http://www.marcochapeau.org/software/laditools',
    packages=['laditools'],
    scripts=['bin/laditray',
             'bin/wmladi',
             'bin/g15ladi',
             'bin/ladilog',
             'bin/ladiconf'],
    data_files=[('share/doc/laditools', ['README', 'COPYING', 'INSTALL']),
        ('share/pixmaps', ['data/ladilog.svg', 'data/laditray.svg', 'data/ladiconf.svg']),
	('share/applications', ['data/laditray.desktop']),
	('share/applications', ['data/ladiconf.desktop']),
        ('share/laditools/data', ['data/laditools_logo.svg',
        'data/ladilog_ui.glade',
        'data/started.svg',
        'data/starting.svg',
        'data/stopped.svg'])]
)
