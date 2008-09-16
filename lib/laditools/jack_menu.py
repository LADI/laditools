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

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import subprocess
from config import config
from jack_configure import jack_configure
from jack_controller import jack_controller
from a2j_controller import a2j_controller
from lash_controller import lash_controller

# TODO : somehow, we need stock icons. Nothing else can be used for ImageMenuItems

# Default launcher menu :
menu_default = [("Configure", "ladiconf"),
    ("Logs", "ladilog")]

class manager:
    def __init__(self, jack_autostart = False):
        self.proxy_jack_controller = None
        self.proxy_jack_configure = None
        self.proxy_a2j_controller = None
        self.proxy_lash_controller = None
        self.diagnose_text = ""
        # Handle the configuration and grab custom menu items
        self.jack_menu_config = config()
        self.menu_array = self.jack_menu_config.get_as_array('jack_menu')
        # Add some defaults if we don't already have a menu
        if self.menu_array == []:
            for name, path in menu_default:
                self.menu_array.append((path, {'name' : name}))
            self.jack_menu_config.set_as_array('jack_menu', self.menu_array, 'menuitem')

        self.proc_list = []

        if jack_autostart:
            self.jack_start()

    def set_diagnose_text(self, text):
        self.diagnose_text = text

    def clear_diagnose_text(self):
        self.diagnose_text = ""
            
    def get_jack_controller(self):
        if not self.proxy_jack_controller:
            self.proxy_jack_controller = jack_controller()
        return self.proxy_jack_controller

    def is_jack_controller_available(self):
        return self.proxy_jack_controller != None

    def clear_jack_controller(self):
        self.proxy_jack_controller = None

    def get_jack_configure(self):
        if not self.proxy_jack_configure:
            self.proxy_jack_configure = jack_configure()
        return self.proxy_jack_configure

    def jack_is_available(self):
        proxy = self.get_jack_controller()
        return proxy and proxy.is_availalbe()

    def jack_start(self):
        if not self.get_jack_configure().get_selected_driver():
             dlg = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "JACK has no driver selected. Configure JACK first!")
             dlg.set_title("Cannot start JACK server")
             dlg.run()
             dlg.destroy()
             return
        self.set_starting_status()
        self.get_jack_controller().start()

    def jack_stop(self):
        self.get_jack_controller().stop()

    def jack_reactivate(self):
        self.get_jack_controller().kill()
        self.clear_jack_controller()

    def jack_reset_xruns(self):
        self.get_jack_controller().reset_xruns()

    def jack_is_started(self):
        return self.get_jack_controller().is_started()

    def jack_is_realtime(self):
        return self.get_jack_controller().is_realtime()

    def jack_get_load(self):
        return self.get_jack_controller().get_load()

    def jack_get_xruns(self):
        return self.get_jack_controller().get_xruns()

    def jack_get_sample_rate(self):
        return self.get_jack_controller().get_sample_rate()

    def jack_get_latency(self):
        return self.get_jack_controller().get_latency()

    def get_a2j_controller(self):
        if not self.proxy_a2j_controller:
            self.proxy_a2j_controller = a2j_controller()
        return self.proxy_a2j_controller

    def clear_a2j_controller(self):
        self.proxy_a2j_controller = None

    def a2j_is_available(self):
        proxy = self.get_a2j_controller()
        if proxy.is_availalbe():
            return True
        self.clear_a2j_controller()
        return False

    def a2j_is_started(self):
        return self.get_a2j_controller().is_started()

    def a2j_start(self):
        self.get_a2j_controller().start()

    def a2j_stop(self):
        self.get_a2j_controller().stop()

    def a2j_reactivate(self):
        self.get_a2j_controller().kill()
        self.clear_a2j_controller()

    def get_lash_controller(self):
        if not self.proxy_lash_controller:
            self.proxy_lash_controller = lash_controller()
        return self.proxy_lash_controller

    def clear_lash_controller(self):
        self.proxy_lash_controller = None

    def lash_is_available(self):
        proxy = self.get_lash_controller()
        if proxy.is_availalbe():
            return True
        self.clear_lash_controller()
        return False

    def lash_projects_save_all(self):
        self.get_lash_controller().projects_save_all()

    def lash_projects_close_all(self):
        self.get_lash_controller().projects_close_all()

    def lash_reactivate(self):
        self.get_lash_controller().kill()
        self.clear_lash_controller()

    def on_menu_show_diagnose(self, widget, data=None):
        dlg = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, self.diagnose_text)
        dlg.set_title("Cannot communicate JACK D-Bus")
        dlg.run()
        dlg.destroy()

    def on_menu_jack_start(self, widget, data=None):
        self.jack_start()

    def on_menu_jack_stop(self, widget, data=None):
        self.jack_stop()

    def on_menu_jack_reactivate(self, widget, data=None):
        self.jack_reactivate()

    def on_menu_jack_reset_xruns(self, widget, data=None):
        self.jack_reset_xruns()

    def on_menu_a2j_start(self, widget, data=None):
        self.a2j_start()

    def on_menu_a2j_stop(self, widget, data=None):
        self.a2j_stop()

    def on_menu_a2j_reactivate(self, widget, data=None):
        self.a2j_reactivate()

    def on_menu_lash_projects_save_all(self, widget, data=None):
        self.lash_projects_save_all()

    def on_menu_lash_projects_close_all(self, widget, data=None):
        self.lash_projects_close_all()

    def on_menu_lash_reactivate(self, widget, data=None):
        self.lash_reactivate()

    def on_menu_destroy(self, widget, data=None):
        gtk.main_quit()

    def on_menu_launcher(self, widget, exec_path):
        self.proc_list.append(subprocess.Popen([exec_path, exec_path]))

    def create_menu(self):
        menu_items = []

        if self.diagnose_text:
            menu_items.append((gtk.ImageMenuItem("Diagnose"), self.on_menu_show_diagnose, None))
            menu_items.append((gtk.SeparatorMenuItem(), None, None))

        # Add the laucher entries at the beginning of the menu
        for path, attrib_dict in self.menu_array:
            menu_items.append((gtk.ImageMenuItem(attrib_dict['name']), self.on_menu_launcher, path))

        menu = gtk.Menu()
        menu_items.append((gtk.SeparatorMenuItem(), None, None))
        if self.jack_is_available():
            if not self.jack_is_started():
                menu_items.append((gtk.ImageMenuItem("Start JACK server"), self.on_menu_jack_start, None))
            else:
                menu_items.append((gtk.ImageMenuItem("Reset Xruns"), self.on_menu_jack_reset_xruns, None))
                menu_items.append((gtk.ImageMenuItem("Stop JACK server"), self.on_menu_jack_stop, None))
            menu_items.append((gtk.ImageMenuItem("Reactivate JACK"), self.on_menu_jack_reactivate, None))
            menu_items.append((gtk.SeparatorMenuItem(), None, None))
        if self.a2j_is_available():
            if not self.a2j_is_started():
                menu_items.append((gtk.ImageMenuItem("Start A2J bridge"), self.on_menu_a2j_start, None))
            else:
                menu_items.append((gtk.ImageMenuItem("Stop A2J bridge"), self.on_menu_a2j_stop, None))
            menu_items.append((gtk.ImageMenuItem("Reactivate A2J"), self.on_menu_a2j_reactivate, None))
            menu_items.append((gtk.SeparatorMenuItem(), None, None))
        if self.lash_is_available():
            menu_items.append((gtk.ImageMenuItem("Save all LASH projects"), self.on_menu_lash_projects_save_all, None))
            menu_items.append((gtk.ImageMenuItem("Close all LASH projects"), self.on_menu_lash_projects_close_all, None))
            menu_items.append((gtk.ImageMenuItem("Reactivate LASH"), self.on_menu_lash_reactivate, None))
            menu_items.append((gtk.SeparatorMenuItem(), None, None))
        menu_items.append((gtk.ImageMenuItem("Quit"), self.on_menu_destroy, None))

        for menu_tuple in menu_items:
            item, callback, exec_path = menu_tuple
            menu.append(item)
            if type(item) is not gtk.SeparatorMenuItem:
                item.connect("activate", callback, exec_path)
        menu.show_all()
        return menu

    def menu_activate(self):
        menu = self.create_menu()
        menu.popup(None, None, None, 3, 0)
        menu.reposition()
