# LADITools - Linux Audio Desktop Integration Tools
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

name_base = 'org.ladish'
control_interface_name = name_base + '.Control'
service_name = name_base

class lash_controller:
    def __init__(self):
        self.bus = dbus.SessionBus()
        self.controller = self.bus.get_object(service_name, "/")
        self.iface = dbus.Interface(self.controller, control_interface_name)

    def is_availalbe(self):
        try:
            self.iface.ProjectsGetAvailable()
            return True
        except Exception, e:
            #print repr(e)
            return False

    def projects_save_all(self):
        self.iface.ProjectsSaveAll()

    def projects_close_all(self):
        self.iface.ProjectsCloseAll()

    def kill(self):
        self.iface.Exit()
