#!/usr/bin/python

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
import glob
from distutils.core import setup
from distutils.command.clean import clean
from DistUtilsExtra.command import *

laditools_version = "1.0~rc8"
get_commit_script = "gitcommit.sh"
pkg_short_desc = "Linux Audio Desktop Integration Tools"
pkg_long_desc = """LADITools is a set of tools aiming to achieve the goals of the LADI project to improve desktop integration and user workflow of Linux audio system based on JACK and ladish. Those tools take advantage of the D-Bus interfaces recently added to JACK and ladish to ease the configuration and use of those two great softwares.

The following tools are included:
 * g15ladi             - a JACK monitor for g15 keyboards
 * ladi-control-center - graphical configuration tool to setup JACK's configuration
 * ladi-player         - convenient VLC-style application to control JACK and manage studios
 * ladi-system-log     - JACK, ladish and a2jmidid log viewer
 * ladi-system-tray    - system indicator that allows users to start, stop and monitor
                         JACK, as well as start some JACK related applications
 * wmladi              - Window Maker dockapp for controlling the LADI system"""
pkg_data_files = [('share/laditools/data', glob.glob('data/*.ui')),
                  ('share/laditools/data', glob.glob('data/*.svg'))]
pkg_scripts = ['g15ladi',
               'ladi-control-center',
               'ladi-player',
               'ladi-system-log',
               'ladi-system-tray',
               'wmladi',]

os.environ['XGETTEXT_ARGS'] = "--language=Python"

if not os.getenv("LADI_RELEASE") and \
        os.path.isfile(get_commit_script):
    commit = subprocess.check_output(["sh", get_commit_script]).strip()
    laditools_version += "~" + commit

iconsizelist = "16 22 24 32 48 64 96 128 256".split()

class my_build_extra(build_extra.build_extra):
    def run(self):
        data_files = self.distribution.data_files

        for manpage in glob.glob('data/*.[0-9]'):
            filename = os.path.split(manpage)[-1]
            subdir = 'man%s' % filename[-1]
            path = os.path.join('share', 'man', subdir)
            print manpage
            data_files.append((path, (manpage,)))

        build_extra.build_extra.run(self)

class build_icons_extra(build_icons.build_icons):
    def run(self):
        icondir = os.path.join('data', 'icons')
        scalabledir = os.path.join(icondir, "scalable")
        categories = os.listdir(scalabledir)

        for size in iconsizelist:
            sizedir = os.path.join(icondir, "%(size)sx%(size)s" % {'size':size})
            for category in categories:
                sizecategorydir = os.path.join(sizedir, category)
                self.spawn(['mkdir', '-p', sizecategorydir])
                for filename in os.listdir(os.path.join(scalabledir, category)):
                    newfilename = filename.rstrip('svg') + 'png'
                    self.spawn(['rsvg',
                                '-w', size, '-h', size,
                                os.path.join(scalabledir, category, filename),
                                os.path.join(sizecategorydir, newfilename)])

        build_icons.build_icons.run(self)

class clean_extra(clean_i18n.clean_i18n):
    def run(self):
        clean_i18n.clean_i18n.run(self)

        for path, dirs, files in os.walk('.'):
            for f in files:
                f = os.path.join(path, f)
                if f.endswith('.pyc'):
                    self.spawn(['rm', f])
            for d in dirs:
                if d == '__pycache__':
                    self.spawn(['rm', '-r', os.path.join(path,d)])

        for path, dirs, files in os.walk('./data/icons'):
            if path.endswith('icons'):
                for d in dirs:
                    if d != 'scalable':
                        self.spawn(['rm', '-r', os.path.join(path,d)])
                break

setup(name='laditools',
    version=laditools_version,
    author='Marc-Olivier Barre, Nedko Arnaudov and Alessio Treglia',
    author_email='linux-audio-dev@lists.linuxaudio.org',
    license='GPL-3',
    url='https://launchpad.net/laditools',
    download_url='https://launchpad.net/laditools/+download',
    description=pkg_short_desc,
    long_description=pkg_long_desc,
    packages=['laditools', 'laditools.gtk'],
    scripts=pkg_scripts,
    data_files=pkg_data_files,
    cmdclass={
        'build' : my_build_extra,
        'build_i18n' :  build_i18n.build_i18n,
        'build_icons' : build_icons_extra,
        'clean' : clean_extra}
)
