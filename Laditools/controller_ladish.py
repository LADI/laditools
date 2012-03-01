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

from enum import Enum
from controller import LadiController
import dbus

name_base = 'org.ladish'
control_iface_name = name_base + '.Control'
studio_iface_name = name_base + '.Studio'
control_obj_path = "/org/ladish/Control"
studio_obj_path = "/org/ladish/Studio"
service_name = name_base

LadishStatusType = Enum("STUDIO_STOPPED",
                        "NOT_AVAILABLE",
                        "NO_STUDIO_LOADED",
                        "STUDIO_RUNNING")

class LadishProxyError(Exception): pass
class LadishStudioException(Exception): pass

def check_ladish():
    """Connect to ladish and return its current status."""
    try:
        proxy = LadishProxy()
    except Exception as e:
        raise LadishProxyError("ladish proxy creation failed: %s" % e.message)
    if not proxy.is_available():
        return LadishStatusType.NOT_AVAILABLE
    if not proxy.studio_is_loaded():
        return LadishStatusType.NO_STUDIO_LOADED
    #    raise LadishStudioException("JACK can only be configured with a loaded "
    #                                "and stopped studio. Please create a new "
    #                                "studio or load and stop an existing one.")
    else:
        if proxy.studio_is_started():
            return LadishStatusType.STUDIO_ALREADY_RUNNING
#            raise LadishStudioException("JACK can only be configured with "
#            "a stopped studio. Please stop your studio first.")

    return LadishStatusType.STUDIO_STOPPED

class LadishProxy(LadiController):

    def __init__ (self):
        LadiController.__init__(self,
                                dbus_type='SessionBus',
                                service_name=service_name,
                                obj_path=control_obj_path,
                                iface_name=control_iface_name)
        self.studio_obj = self.bus.get_object(service_name, studio_obj_path)
        self.studio_iface = dbus.Interface(self.studio_obj, studio_iface_name)
        LadiController._delete_attr('is_started')

    def is_available(self):
        try:
            self.studio_is_loaded()
            return True
        except Exception, e:
            #print repr(e)
            return False

    def studio_list(self):
        studios = []
        for studio in self.controller_iface.GetStudioList():
            studios.append(studio[0])
        return studios

    def studio_new(self, name=""):
        self.controller_iface.NewStudio(name)

    def studio_is_loaded(self):
        return self.controller_iface.IsStudioLoaded()

    def studio_load(self, name):
        self.controller_iface.LoadStudio(name, {})

    def studio_delete(self, name):
        self.controller_iface.DeleteStudio(name)

    def kill(self):
        self.controller_iface.Exit()

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

    def studio_is_started(self):
        return self.studio_iface.IsStarted()
