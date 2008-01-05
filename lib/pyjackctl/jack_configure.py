# pyjackctl - The python jackdbus controller suite
# Copyright (C) 2007-2008, Marc-Olivier Barre and Nedko Arnaudov.
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
controller_interface_name = name_base + '.JackConfigure'
service_name = name_base + '.service'

class jack_configure:
    def __init__(self):
        self.bus = dbus.SessionBus()
        self.controller = self.bus.get_object(service_name, "/org/jackaudio/Controller")
        self.iface = dbus.Interface(self.controller, controller_interface_name)

    def get_available_driver(self):
        return self.iface.GetAvailableDrivers()

    def get_selected_driver(self):
        return self.iface.GetSelectedDriver()
    
    def select_driver(self, driver):
        self.iface.SelectDriver(driver)

    def get_driver_param_names(self):
        return self.iface.GetDriverParameterNames()

    def get_driver_short_description(self, param):
        return self.iface.GetDriverParameterShortDescription(param)

    def get_driver_long_description(self, param):
        return self.iface.GetDriverParameterLongDescription(param)

    def get_driver_param_type(self, param):
        return self.iface.GetDriverParameterTypeString(param)

    def get_driver_param_value(self, param):
        typestr = self.get_driver_param_type(param)
        if typestr == "str":
            return self.iface.GetDriverParameterValueString(param)
        elif typestr == "bool":
            return self.iface.GetDriverParameterValueBool(param)
        elif typestr == "char":
            return self.iface.GetDriverParameterValueChar(param)
        elif typestr == "sint":
            return self.iface.GetDriverParameterValueInt(param)
        elif typestr == "uint":
            return self.iface.GetDriverParameterValueUint(param)
        else:
            return None

    def set_driver_param_value(self, param, value):
        typestr = self.get_driver_param_type(param)
        if typestr == "str":
            self.iface.SetDriverParameterValueString(param, value)
        elif typestr == "bool":
            self.iface.SetDriverParameterValueBool(param, value)
        elif typestr == "char":
            self.iface.SetDriverParameterValueChar(param, value)
        elif typestr == "sint":
            self.iface.SetDriverParameterValueInt(param, value)
        elif typestr == "uint":
            self.iface.SetDriverParameterValueUint(param, value)

    def get_engine_param_names(self):
        return self.iface.GetEngineParameterNames()

    def get_engine_short_description(self, param):
        return self.iface.GetEngineParameterShortDescription(param)

    def get_engine_long_description(self, param):
        return self.iface.GetEngineParameterLongDescription(param)

    def get_engine_param_type(self, param):
        return self.iface.GetEngineParameterTypeString(param)

    def get_engine_param_value(self, param):
        typestr = self.get_engine_param_type(param)
        if typestr == "str":
            return self.iface.GetEngineParameterValueString(param)
        elif typestr == "bool":
            return self.iface.GetEngineParameterValueBool(param)
        elif typestr == "char":
            return self.iface.GetEngineParameterValueChar(param)
        elif typestr == "sint":
            return self.iface.GetEngineParameterValueInt(param)
        elif typestr == "uint":
            return self.iface.GetEngineParameterValueUint(param)
        else:
            return None

    def set_engine_param_value(self, param, value):
        typestr = self.get_engine_param_type(param)
        if typestr == "str":
            self.iface.SetEngineParameterValueString(param, value)
        elif typestr == "bool":
            self.iface.SetEngineParameterValueBool(param, value)
        elif typestr == "char":
            self.iface.SetEngineParameterValueChar(param, value)
        elif typestr == "sint":
            self.iface.SetEngineParameterValueInt(param, value)
        elif typestr == "uint":
            self.iface.SetEngineParameterValueUint(param, value)