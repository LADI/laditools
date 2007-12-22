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

class jack_menu:
    def __init__(self):
        self.menu = gtk.Menu()
        self.start_item = gtk.MenuItem("_Start JACK")
        self.stop_item = gtk.MenuItem("Sto_p JACK")
        self.reactivate_item = gtk.MenuItem("Reactivate JACK")
	self.quit_item = gtk.MenuItem("_Quit")
        self.menu.append(self.start_item)
        self.menu.append(self.stop_item)
        self.menu.append(self.reactivate_item)
        self.menu.append(self.quit_item)
        self.start_item.connect("activate", self.on_menu_start)
        self.stop_item.connect("activate", self.on_menu_stop)
        self.reactivate_item.connect("activate", self.on_menu_reactivate)
        self.quit_item.connect("activate", self.on_menu_destroy)
        self.menu.show_all()

    def on_menu_start(self, widget):
        self.get_controller().start()
	
    def on_menu_stop(self, widget):
        self.get_controller().stop()
	
    def on_menu_reactivate(self, widget):
        self.get_controller().kill()
	
    def on_menu_destroy(self, widget):
        gtk.main_quit()

    def menu_activate(self, widget=None, event=None, data=None):
        self.menu.popup(None, None, None, 3, 0)
        self.menu.reposition()
