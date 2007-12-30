#!/usr/bin/env python

# pyjackctl - The python jackdbus controller suite
# Copyright (C) 2007, Marc-Olivier Barre and Nedko Arnaudov.
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

setup(name='pyjackctl',
    version='0.1',
    description='The pyjackctl controller suite',
    author='Marc-Olivier Barre and Nedko Arnaudov',
    author_email='mobarre@gmail.com',
    url='http://www.marcochapeau.org/software/1',
    packages=['pyjackctl'],
    package_dir={'pyjackctl': 'lib/pyjackctl'},
    scripts=['jackctl_trayicon', 'wmjackctl', 'g15jackmon', 'jackctl_logview', 'jackctl_conf'],
    data_files=[('share/doc/pyjackctl', ['README', 'COPYING']),
        ('share/pixmaps', ['data/pyjackctl.svg']),
        ('share/pyjackctl/data', ['data/pyjackctl.svg']),
        ('share/pyjackctl/data', ['data/pyjackctl_logo.svg',
        'data/jackctl_logview_ui.glade',
        'data/jackctl_conf_ui.glade',
        'data/started.svg',
        'data/stopped.svg'])]
)
