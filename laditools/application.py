#!/usr/bin/python
# LADITools - Linux Audio Desktop Integration Tools
# Copyright (C) 2011-2012 Alessio Treglia <quadrispro@ubuntu.com>
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

import signal

class LadiApp(object):

    @property
    def appname(self): return self._appname

    @property
    def appname_long(self): return self._appname_long

    @property
    def appid(self): return self._appid

    def connect_signals_quit(self, signals=[], sig_handler=None):
        if not signals:
            signals = [signal.SIGTERM,
                       signal.SIGINT]
        if not sig_handler:
            sig_handler = self.quit

        for sig in signals:
            signal.signal(sig, sig_handler)
            signal.signal(sig, sig_handler)

    def run(self): raise NotImplementedError
    def quit(self): raise NotImplementedError
