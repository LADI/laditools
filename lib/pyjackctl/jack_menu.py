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

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import subprocess
from config import config

# TODO : somehow, we need stock icons. Nothing else can be used for ImageMenuItems

# Default launcher menu :
menu_default = [("Configure", "/usr/bin/jackconf"),
    ("Connect", "/usr/bin/patchage"),
    ("Logs", "/usr/bin/jacklog")]

class jack_menu:
    def __init__(self):
        self.menu_items = []
        # Handle the configuration and grab custom menu items
        self.jack_menu_config = config()
        self.menu_array = self.jack_menu_config.get_as_array('jack_menu')
        # Add some defaults if we don't already have a menu
        if self.menu_array == []:
            for name, path in menu_default:
                self.menu_array.append((path, {'name' : name}))
            self.jack_menu_config.set_as_array('jack_menu', self.menu_array, 'menuitem')
        # Add the laucher entries at the beginning of the menu
        for path, attrib_dict in self.menu_array:
            self.menu_items.append((gtk.ImageMenuItem(attrib_dict['name']), self.on_menu_launcher, path))
        #Create the rest of the menu
        self.menu = gtk.Menu()
        self.menu_items.append((gtk.SeparatorMenuItem(), self.on_menu_start, None))
        self.menu_items.append((gtk.ImageMenuItem("Reset Xruns"), self.on_menu_reset_xruns, None))
        self.menu_items.append((gtk.ImageMenuItem("Start JACK"), self.on_menu_start, None))
        self.menu_items.append((gtk.ImageMenuItem("Stop JACK"), self.on_menu_stop, None))
        self.menu_items.append((gtk.SeparatorMenuItem(), self.on_menu_start, None))
        self.menu_items.append((gtk.ImageMenuItem("Reactivate JACK"), self.on_menu_reactivate, None))
        self.menu_items.append((gtk.ImageMenuItem("Quit"), self.on_menu_destroy, None))
        for menu_tuple in self.menu_items:
            item, callback, exec_path = menu_tuple
            self.menu.append(item)
            if type(item) is not gtk.SeparatorMenuItem:
                item.connect("activate", callback, exec_path)
        self.menu.show_all()
        self.proc_list = []

    def on_menu_start(self, widget, data=None):
        self.set_starting_status()
        self.get_controller().start()

    def on_menu_stop(self, widget, data=None):
        self.get_controller().stop()

    def on_menu_reactivate(self, widget, data=None):
        self.get_controller().kill()

    def on_menu_destroy(self, widget, data=None):
        gtk.main_quit()

    def on_menu_launcher(self, widget, exec_path):
        self.proc_list.append(subprocess.Popen([exec_path, exec_path]))

    def on_menu_reset_xruns(self, widget, data=None):
        self.get_controller().reset_xruns()

    def menu_activate(self):
        self.menu.popup(None, None, None, 3, 0)
        self.menu.reposition()