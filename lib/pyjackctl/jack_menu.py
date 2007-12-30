# pyjackctl - The python jackdbus controller suite
# Copyright (C) 2007, Marc-Olivier Barre and Nedko Arnaudov.
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
import os

# TODO : we need stock icons, nothing else can be used for ImageMenuItems

class jack_menu:
    def __init__(self):
        self.menu = gtk.Menu()
        self.menu_items = [(gtk.ImageMenuItem("Configure"), self.on_menu_launcher, "jackctl_conf"),
            (gtk.ImageMenuItem("Connect"), self.on_menu_launcher, "patchage"),
            (gtk.ImageMenuItem("Logs"), self.on_menu_launcher, "jackctl_logview"),
            (gtk.SeparatorMenuItem(), self.on_menu_start, None),
            (gtk.ImageMenuItem("Reset Xruns"), self.on_menu_reset_xruns, None),
            (gtk.ImageMenuItem("Start JACK"), self.on_menu_start, None),
            (gtk.ImageMenuItem("Stop JACK"), self.on_menu_stop, None),
            (gtk.SeparatorMenuItem(), self.on_menu_start, None),
            (gtk.ImageMenuItem("Reactivate JACK"), self.on_menu_reactivate, None),
            (gtk.ImageMenuItem("Quit"), self.on_menu_destroy, None)]
        for tuples in self.menu_items:
            item, callback, exec_path = tuples
            self.menu.append(item)
            # TODO : SeparatorMenuItems also get "connected". It does nothing but it's ugly.
            item.connect("activate", callback, exec_path)
        self.menu.show_all()

    def on_menu_start(self, widget, data=None):
        self.get_controller().start()

    def on_menu_stop(self, widget, data=None):
        self.get_controller().stop()

    def on_menu_reactivate(self, widget, data=None):
        self.get_controller().kill()

    def on_menu_destroy(self, widget, data=None):
        gtk.main_quit()

    def on_menu_launcher(self, widget, exec_path):
        os.spawnlp(os.P_NOWAIT, exec_path, exec_path)

    def on_menu_reset_xruns(self, widget, data=None):
        self.get_controller().reset_xruns()

    def menu_activate(self):
        self.menu.popup(None, None, None, 3, 0)
        self.menu.reposition()
