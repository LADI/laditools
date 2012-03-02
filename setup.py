#!/usr/bin/env python

# LADITools - Linux Audio Desktop Integration Tools
# setup.py - Setup script for the LADITools suite
# Copyright (C) 2011-2012 Alessio Treglia <quadrispro@ubuntu.com>
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

import os
import sys
import subprocess
from distutils.core import setup
from distutils.command.clean import clean
from DistUtilsExtra.command import *

laditools_version = "1.0~rc2"
get_commit_script = "gitcommit.sh"

if not os.getenv("LADI_RELEASE") and \
        os.path.isfile(get_commit_script):
    commit = subprocess.check_output(["sh", get_commit_script]).strip()
    laditools_version += "+" + commit

class clean_extra(clean_i18n.clean_i18n):
    def run(self):
        clean_i18n.clean_i18n.run(self)

        for path, dirs, files in os.walk('.'):
            for f in files:
                f = os.path.join(path, f)
                if f.endswith('.pyc'):
                    self.spawn(['rm', f])

setup(name='laditools',
    version=laditools_version,
    description='Linux Audio Desktop Integration Tools',
    author='Marc-Olivier Barre, Nedko Arnaudov and Alessio Treglia',
    author_email='linux-audio-dev@lists.linuxaudio.org',
    license='GPL-3',
    url='https://launchpad.net/laditools',
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
        'data/ladilog_ui.ui',
        'data/started.svg',
        'data/starting.svg',
        'data/stopped.svg'])],
    cmdclass={
        'build' : build_extra.build_extra,
        'build_i18n' :  build_i18n.build_i18n,
        'clean' : clean_extra}
)
