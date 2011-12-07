# LADITools - Linux Audio Desktop Integration Tools
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

import dbus
from dbus.mainloop.glib import DBusGMainLoop

name_base = 'org.jackaudio'
controller_interface_name = name_base + '.Configure'
service_name = name_base + '.service'

def dbus_type_to_python_type (dbus_value):
    if type (dbus_value) == dbus.Boolean:
        return bool(dbus_value)
    if type (dbus_value) == dbus.Int32 or type (dbus_value) == dbus.UInt32:
        return int(dbus_value)
    if type (dbus_value) == dbus.String:
        return str(dbus_value)
    if type (dbus_value) == dbus.Byte:
        return str (dbus_value)
    return dbus_value

class jack_configure:
    def __init__ (self):
        # Connect to the bus
        self.bus = dbus.SessionBus ()
        self.controller = self.bus.get_object (service_name, "/org/jackaudio/Controller")
        self.iface = dbus.Interface (self.controller, controller_interface_name)
#        self.bus.add_signal_receiver (self.name_owner_changed, dbus_interface = controller_interface_name, signal_name = "NameOwnerChanged")

    def name_owner_changed (name = None, old_owner = None, new_owner = None):
        print "Name changed : %r" % name

    def get_selected_driver (self):
        isset, default, value = self.iface.GetParameterValue (['engine', 'driver'])
        return value

    def read_container (self, path):
        is_leaf, children = self.iface.ReadContainer (path)
        if is_leaf:
            return []
        return children

    def get_param_names (self, path):
        is_leaf, children = self.iface.ReadContainer (path)
        if not is_leaf:
            return []
        return children

    def get_param_short_description (self, path):
        type_char, name, short_descr, long_descr = self.iface.GetParameterInfo (path)
        return short_descr

    def get_param_long_description (self, path):
        type_char, name, short_descr, long_descr = self.iface.GetParameterInfo (path)
        return long_descr

    def get_param_type (self, path):
        type_char, name, short_descr, long_descr = self.iface.GetParameterInfo (path)
        return str (type_char)

    def get_param_value (self, path):
        isset, default, value = self.iface.GetParameterValue (path)
        isset = bool (isset)
        default = dbus_type_to_python_type (default)
        value = dbus_type_to_python_type (value)
        return isset, default, value

    def set_param_value (self, path, value):
        typestr = self.get_param_type (path)
        if typestr == "b":
            value = dbus.Boolean (value)
        elif typestr == "y":
            value = dbus.Byte (value)
        elif typestr == "i":
            value = dbus.Int32 (value)	
        elif typestr == "u":
            value = dbus.UInt32 (value)
        self.iface.SetParameterValue (path, value)

    def reset_param_value (self, path):
        self.iface.ResetParameterValue (path)

    def param_has_range (self, path):
        is_range, is_strict, is_fake_value, values = self.iface.GetParameterConstraint (path)
        return bool (is_range)

    def param_get_range (self, path):
        is_range, is_strict, is_fake_value, values = self.iface.GetParameterConstraint (path)
        if not is_range or len (values) != 2:
            return -1, -1
        return dbus_type_to_python_type (values[0][0]), dbus_type_to_python_type (values[1][0])

    def param_has_enum (self, path):
        is_range, is_strict, is_fake_value, values = self.iface.GetParameterConstraint (path)
        return not is_range and len (values) != 0

    def param_is_strict_enum (self, path):
        is_range, is_strict, is_fake_value, values = self.iface.GetParameterConstraint (path)
        return is_strict

    def param_is_fake_value (self, path):
        is_range, is_strict, is_fake_value, values = self.iface.GetParameterConstraint (path)
        return is_fake_value

    def param_get_enum_values (self, path):
        is_range, is_strict, is_fake_value, dbus_values = self.iface.GetParameterConstraint (path)
        values = []

        if not is_range and len (dbus_values) != 0:
            for dbus_value in dbus_values:
                values.append ([dbus_type_to_python_type (dbus_value[0]), dbus_type_to_python_type (dbus_value[1])])
        return values
