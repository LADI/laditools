#!/usr/bin/python
# LADITools - Linux Audio Desktop Integration Tools
# Copyright (C) 2011-2012 Alessio Treglia <quadrispro@ubuntu.com>
# Copyright (C) 2007-2010, Marc-Olivier Barre <marco@marcochapeau.org>
# Copyright (C) 2007-2009, Nedko Arnaudov <nedko@arnaudov.name>
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

from controller import LadiController

name_base = 'org.jackaudio'
iface_name = name_base + '.JackControl'
service_name = name_base + '.service'
obj_path = '/org/jackaudio/Controller'

class JackController(LadiController):
    def __init__ (self):
        LadiController.__init__(self,
                                dbus_type='SessionBus',
                                service_name=service_name,
                                obj_path=obj_path,
                                iface_name=iface_name)

    def is_started (self):
        return self.controller_iface.IsStarted ()

    def name_owner_changed (name = None, old_owner = None, new_owner = None):
        sys.stderr.write("Name changed : %r\n" % name)
        sys.stderr.flush()

    def is_realtime (self):
        return self.controller_iface.IsRealtime ()

    def get_load (self):
        return self.controller_iface.GetLoad ()

    def get_xruns (self):
        return self.controller_iface.GetXruns ()

    def get_sample_rate (self):
        return self.controller_iface.GetSampleRate ()

    def get_latency (self):
        return self.controller_iface.GetLatency ()

    def reset_xruns (self):
        return self.controller_iface.ResetXruns ()

    def start (self):
        self.controller_iface.StartServer ()

    def stop (self):
        self.controller_iface.StopServer ()

    def kill (self):
        self.controller_iface.Exit ()
