#!/usr/bin/python
# LADITools - Linux Audio Desktop Integration Tools
# Copyright (C) 2012 Alessio Treglia <quadrispro@ubuntu.com>
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
import sys

class LadiController(object):
    """Wrap common routines used by D-Bus objects.
    
    It is recommended to use one of the available implementations
    instead of creating instances of this class.
    """

    def __init__(self, dbus_type, service_name, obj_path, iface_name, args = None):
        # Connect to the bus
        self.bus = getattr(dbus, dbus_type)()
        self.controller_obj = self.bus.get_object (service_name, obj_path)
        self.controller_iface = dbus.Interface (self.controller_obj, iface_name)
    
    def is_available (self):
    """Check if the service is available."""
        try:
            self.is_started ()
            return True
        except Exception, err:
            sys.stderr.write(str(err) + '\n')
            sys.stderr.flush()
            return False

    def is_started (self):
    """Check if the service is running."""
        return self.controller_iface.is_started ()

    def start(self):
    """Start the service."""
        self.controller_iface.start()

    def stop(self):
    """Stop the service."""
        self.controller_iface.stop()

    def kill(self):
    """Kill the service."""
        self.controller_iface.exit()
