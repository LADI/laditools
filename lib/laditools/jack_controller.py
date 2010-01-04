# LADITools - Linux Audio Desktop Integration Tools
# Copyright (C) 2007-2010:
# * Marc-Olivier Barre <marco@marcochapeau.org>
# * Nedko Arnaudov <nedko@arnaudov.name>
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

import dbus

name_base = 'org.jackaudio'
controller_interface_name = name_base + '.JackControl'
service_name = name_base + '.service'

class jack_controller:
    def __init__ (self, mainloop):
        # Connect to the bus
        self.bus = dbus.SessionBus (mainloop)
        self.controller = self.bus.get_object (service_name, "/org/jackaudio/Controller")
        self.iface = dbus.Interface (self.controller, controller_interface_name)
        self.bus.add_signal_receiver (self.name_owner_changed, dbus_interface = controller_interface_name, signal_name = "NameOwnerChanged")

    def name_owner_changed (name = None, old_owner = None, new_owner = None):
        print "Name changed : %r" % name

    def is_available (self):
        try:
            self.iface.IsStarted ()
            return True
        except:
            return False

    def is_started (self):
        return self.iface.IsStarted ()

    def is_realtime (self):
        return self.iface.IsRealtime ()

    def get_load (self):
        return self.iface.GetLoad ()

    def get_xruns (self):
        return self.iface.GetXruns ()

    def get_sample_rate (self):
        return self.iface.GetSampleRate ()

    def get_latency (self):
        return self.iface.GetLatency ()

    def reset_xruns (self):
        return self.iface.ResetXruns ()

    def start (self):
        self.iface.StartServer ()

    def stop (self):
        self.iface.StopServer ()

    def kill (self):
        self.iface.Exit ()
