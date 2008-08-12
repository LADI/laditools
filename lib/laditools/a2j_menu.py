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

# TODO : somehow, we need stock icons. Nothing else can be used for ImageMenuItems

class a2j_menu:
    def __init__(self):
        self.menu_items = []
        self.menu_items.append((gtk.ImageMenuItem("Start bridging"), self.on_menu_start))
        self.menu_items.append((gtk.ImageMenuItem("Stop bridging"), self.on_menu_stop))
        self.menu_items.append((gtk.SeparatorMenuItem(), None))
        self.menu_items.append((gtk.ImageMenuItem("Reactivate"), self.on_menu_reactivate))
        self.menu_items.append((gtk.ImageMenuItem("Quit"), self.on_menu_destroy))

        self.menu = gtk.Menu()
        for menu_tuple in self.menu_items:
            item, callback = menu_tuple
            self.menu.append(item)
            if callback:
                item.connect("activate", callback)
        self.menu.show_all()

    def on_menu_start(self, widget):
        self.set_starting_status()
        self.get_controller().start()

    def on_menu_stop(self, widget):
        self.get_controller().stop()

    def on_menu_reactivate(self, widget):
        self.get_controller().kill()

    def on_menu_destroy(self, widget):
        gtk.main_quit()

    def menu_activate(self):
        self.menu.popup(None, None, None, 3, 0)
        self.menu.reposition()
