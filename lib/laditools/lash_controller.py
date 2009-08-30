# LADITools - Linux Audio Desktop Integration Tools
# Copyright (C) 2007, 2008, 2009, Marc-Olivier Barre and Nedko Arnaudov.
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

name_base = 'org.ladish'
control_interface_name = name_base + '.Control'
studio_interface_name = name_base + '.Studio'
control_object_path = "/org/ladish/Control"
studio_object_path = "/org/ladish/Studio"
service_name = name_base

class ladish_proxy:
    def __init__(self):
        self.bus = dbus.SessionBus()
        self.control_object = self.bus.get_object(service_name, control_object_path)
        self.control_iface = dbus.Interface(self.control_object, control_interface_name)
        self.studio_object = self.bus.get_object(service_name, studio_object_path)
        self.studio_iface = dbus.Interface(self.studio_object, studio_interface_name)

    def is_availalbe(self):
        try:
            self.control_iface.IsStudioLoaded()
            return True
        except Exception, e:
            #print repr(e)
            return False

    def studio_list(self):
        studios = []
        for studio in self.control_iface.GetStudioList():
            studios.append(studio[0])
        return studios

    def studio_new(self, name=""):
        self.control_iface.NewStudio(name)

    def studio_is_loaded(self):
        return self.control_iface.IsStudioLoaded()

    def studio_load(self, name):
        self.control_iface.LoadStudio(name, {})

    def studio_delete(self, name):
        self.control_iface.DeleteStudio(name)

    def kill(self):
        self.control_iface.Exit()

    def studio_start(self):
        self.studio_iface.Start()

    def studio_stop(self):
        self.studio_iface.Stop()

    def studio_rename(self, new_name):
        self.studio_iface.Rename(new_name)

    def studio_save(self):
        self.studio_iface.Save()

    def studio_unload(self):
        self.studio_iface.Unload()

    def studio_name(self):
        return self.studio_iface.GetName()
