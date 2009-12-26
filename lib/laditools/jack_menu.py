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

import os
import sys
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import subprocess
from config import config
from jack_configure import jack_configure
from jack_controller import jack_controller
from a2j_controller import a2j_controller
from lash_controller import ladish_proxy

# TODO : somehow, we need stock icons. Nothing else can be used for ImageMenuItems

# Default launcher menu :
menu_default = [("Configure...", "ladiconf"),
    ("Logs...", "ladilog")]

class manager:
    def __init__(self, jack_autostart = False):
        self.proxy_jack_controller = None
        self.proxy_jack_configure = None
        self.proxy_a2j_controller = None
        self.proxy_ladish_controller = None
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
            #print "creating jack proxy"
            self.proxy_jack_controller = jack_controller()
        return self.proxy_jack_controller

    def is_jack_controller_available(self):
        return self.proxy_jack_controller != None

    def get_jack_configure(self):
        if not self.proxy_jack_configure:
            self.proxy_jack_configure = jack_configure()
        return self.proxy_jack_configure

    def clear_jack_proxies(self):
        #print "clearing jack proxies"
        self.proxy_jack_controller = None
        self.proxy_jack_configure = None

    def jack_is_available(self):
        try:
            proxy = self.get_jack_controller()
        except:
            return False
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
        self.clear_jack_proxies()

    def jack_reset_xruns(self):
        self.get_jack_controller().reset_xruns()

    def jack_is_started(self):
        #print "jack_is_started"
        return self.get_jack_controller().is_started()

    def jack_is_realtime(self):
        #print "jack_is_realtime"
        return self.get_jack_controller().is_realtime()

    def jack_get_load(self):
        #print "jack_get_load"
        return self.get_jack_controller().get_load()

    def jack_get_xruns(self):
        #print "jack_get_xruns"
        return self.get_jack_controller().get_xruns()

    def jack_get_sample_rate(self):
        #print "jack_get_sample_rate"
        return self.get_jack_controller().get_sample_rate()

    def jack_get_latency(self):
        #print "jack_get_latency"
        return self.get_jack_controller().get_latency()

    def get_a2j_controller(self):
        if not self.proxy_a2j_controller:
            self.proxy_a2j_controller = a2j_controller()
        return self.proxy_a2j_controller

    def clear_a2j_controller(self):
        self.proxy_a2j_controller = None

    def a2j_is_available(self):
        try:
            proxy = self.get_a2j_controller()
        except:
            return False
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

    def get_ladish_controller(self):
        if not self.proxy_ladish_controller:
            self.proxy_ladish = ladish_proxy()
        return self.proxy_ladish

    def clear_ladish_controller(self):
        self.proxy_ladish_controller = None

    def ladish_is_available(self):
        try:
            proxy = self.get_ladish_controller()
        except:
            return False
        if proxy.is_availalbe():
            return True
        self.clear_ladish_controller()
        return False

    def studio_is_loaded(self):
        return self.get_ladish_controller().studio_is_loaded()

    def studio_new(self):
        accept, name = self.name_dialog("New studio", "Studio name", "")
        if accept:
            self.get_ladish_controller().studio_new(name)

    def studio_load(self, item, event, studio):
        self.get_ladish_controller().studio_load(studio)

    def studio_start(self):
        self.get_ladish_controller().studio_start()

    def studio_stop(self):
        self.get_ladish_controller().studio_stop()

    def name_dialog(self, title, label, text):
        dlg = gtk.Dialog(
            title,
            None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
             gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label(label))
        entry = gtk.Entry()
        entry.set_text(text)
        hbox.pack_start(entry)
        dlg.vbox.pack_start(hbox)
        dlg.show_all()
        #entry.set_activates_default(True)
        #dlg.set_default_response(gtk.RESPONSE_OK)
        ret = dlg.run()
        dlg.destroy()
        if ret == gtk.RESPONSE_ACCEPT:
            return True, entry.get_text()
        else:
            return False, text

    def studio_rename(self):
        accept, name = self.name_dialog("Rename studio", "Studio name", self.get_ladish_controller().studio_name())
        if accept:
            self.get_ladish_controller().studio_rename(name)

    def studio_save(self):
        self.get_ladish_controller().studio_save()

    def studio_unload(self):
        self.get_ladish_controller().studio_unload()

    def studio_delete(self, item, event, studio):
        dlg = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_YES_NO, "")
        dlg.set_markup("<b><big>Confirm studio delete</big></b>")
        dlg.format_secondary_text("Studio \"%s\" will be deleted. Are you sure?" % studio)
        ret = dlg.run()
        dlg.destroy()
        if ret == gtk.RESPONSE_YES:
            self.get_ladish_controller().studio_delete(studio)

    def ladish_reactivate(self):
        self.get_ladish_controller().kill()
        self.clear_ladish_controller()

    def on_menu_show_diagnose(self, widget, data=None):
        dlg = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, self.diagnose_text)
        dlg.set_title("Cannot communicate JACK D-Bus")
        dlg.run()
        dlg.destroy()

    def on_menu_command(self, widget, function):
        try:
            function()
        except Exception, e:
            error = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Error executing " + repr(function) + "Unexpected error\n\n" + repr(e))
            error.run()
            error.destroy()

    def on_menu_launcher(self, widget, exec_path):
        self.proc_list.append(subprocess.Popen([exec_path, exec_path]))

    def menu_clear(self, menu):
        menu.foreach(lambda item: menu.remove(item))

    def studio_list_fill(self, widget, function):
        menu = widget.get_submenu()
        self.menu_clear(menu)
        try:
            for studio in self.get_ladish_controller().studio_list():
                item = gtk.MenuItem(studio)
                item.show()
                menu.append(item)
                item.connect("button-release-event", function, studio) # "activate" is not used because of focus bug in pygtk
        except Exception, e:
            print e
            self.menu_clear(menu)
            item = gtk.MenuItem("Error obtaining studio list")
            item.set_sensitive(False)
            item.show()
            menu.append(item)
        if not menu.get_children():
            item = gtk.MenuItem("Empty studio list")
            item.set_sensitive(False)
            item.show()
            menu.append(item)

    def create_menu(self):
        menu_items = []

        if self.diagnose_text:
            menu_items.append((gtk.ImageMenuItem("Diagnose"), self.on_menu_show_diagnose, None))
            menu_items.append((gtk.SeparatorMenuItem(), None, None))

        # Add the laucher entries at the beginning of the menu
        for path, attrib_dict in self.menu_array:
            menu_items.append((gtk.ImageMenuItem(attrib_dict['name']), self.on_menu_launcher, path))

        menu = gtk.Menu()
        menu_items.append((gtk.SeparatorMenuItem(),))
        if self.ladish_is_available():
            menu_items.append((gtk.ImageMenuItem("New studio..."), self.on_menu_command, self.studio_new))
            menu_items.append((gtk.ImageMenuItem("Load studio"), self.studio_list_fill, self.studio_load))
            if self.studio_is_loaded():
                menu_items.append((gtk.SeparatorMenuItem(), None, None))
                menu_items.append((gtk.ImageMenuItem("Start studio"), self.on_menu_command, self.studio_start))
                menu_items.append((gtk.ImageMenuItem("Stop studio"), self.on_menu_command, self.studio_stop))
            menu_items.append((gtk.SeparatorMenuItem(), None, None))
            if self.studio_is_loaded():
                menu_items.append((gtk.ImageMenuItem("Rename studio..."), self.on_menu_command, self.studio_rename))
                menu_items.append((gtk.ImageMenuItem("Save studio"), self.on_menu_command, self.studio_save))
                menu_items.append((gtk.ImageMenuItem("Unload studio"), self.on_menu_command, self.studio_unload))
            menu_items.append((gtk.ImageMenuItem("Delete studio"), self.studio_list_fill, self.studio_delete))
            menu_items.append((gtk.ImageMenuItem("Reactivate ladishd"), self.on_menu_command, self.ladish_reactivate))
            menu_items.append((gtk.SeparatorMenuItem(), None, None))
        if self.jack_is_available():
            if not self.jack_is_started():
                if not self.ladish_is_available():
                    menu_items.append((gtk.ImageMenuItem("Start JACK server"), self.on_menu_command, self.jack_start))
            else:
                menu_items.append((gtk.ImageMenuItem("Reset Xruns"), self.on_menu_command, self.jack_reset_xruns))
                if not self.ladish_is_available():
                    menu_items.append((gtk.ImageMenuItem("Stop JACK server"), self.on_menu_command, self.jack_stop))
            menu_items.append((gtk.ImageMenuItem("Reactivate JACK"), self.on_menu_command, self.jack_reactivate))
            menu_items.append((gtk.SeparatorMenuItem(), None, None))
        if self.a2j_is_available():
            if not self.a2j_is_started():
                menu_items.append((gtk.ImageMenuItem("Start A2J bridge"), self.on_menu_command, self.a2j_start))
            else:
                menu_items.append((gtk.ImageMenuItem("Stop A2J bridge"), self.on_menu_command, self.a2j_stop))
            menu_items.append((gtk.ImageMenuItem("Reactivate A2J"), self.on_menu_command, self.a2j_reactivate))
            menu_items.append((gtk.SeparatorMenuItem(), None, None))
        menu_items.append((gtk.ImageMenuItem("Quit"), self.on_menu_command, gtk.main_quit))

        for menu_tuple in menu_items:
            item = menu_tuple[0]
            if len(menu_tuple) > 1:
                callback = menu_tuple[1]
                exec_path = menu_tuple[2]
            menu.append(item)
            if type(item) is not gtk.SeparatorMenuItem:
                if callback == self.studio_list_fill:
                    item.set_submenu(gtk.Menu())
                item.connect("activate", callback, exec_path)
        menu.show_all()
        return menu

    def menu_activate(self):
        menu = self.create_menu()
        menu.popup(None, None, None, 3, 0)
        menu.reposition()

def find_data_file(path):
    start_dir = os.path.dirname(sys.argv[0])

    if not start_dir:
        start_dir = "."

    paths = [
        start_dir + os.sep + "data" + os.sep + path,
        start_dir + os.sep + ".." + os.sep + "share"+ os.sep + "laditools" + os.sep + "data" + os.sep + path,
        ]

    for path in paths:
        #print 'Checking "%s"...' % path
        if os.path.isfile(path):
            #print 'Found data file in "%s"' % path
            return path

    raise Exception('Data file "%s" not found' % path)
