#!/usr/bin/python
# LADITools - Linux Audio Desktop Integration Tools
# Copyright (C) 2011-2012 Alessio Treglia <quadrispro@ubuntu.com>
# Copyright (C) 2007-2010:
# * Marc-Olivier Barre <marco@marcochapeau.org>
# * Nedko Arnaudov <nedko@arnaudov.name>
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
import subprocess
from gi.repository import Gtk
from gi.repository import GObject
from laditools import _gettext_domain
from laditools import LadiConfiguration
from laditools import JackConfigProxy
from laditools import JackController
from laditools import A2jController
from laditools import LadishProxy

# Default launcher menu :
menu_default = [{"Logs": "ladilog"}]

class LadiManager(object):
    def __init__(self, menu_config_array, jack_autostart = False):
        self.proxy_jack_controller = None
        self.proxy_jack_configure = None
        self.proxy_a2j_controller = None
        self.proxy_ladish_controller = None
        self.diagnose_text = ""
        # Handle the configuration and grab custom menu items
        self.menu_array = menu_config_array
        # Add some defaults if we don't already have a menu
        if self.menu_array == None:
            self.menu_array = []
            for element in menu_default:
                self.menu_array.append(element)

        self.proc_list = []

        if jack_autostart:
            self.jack_start ()

    def set_diagnose_text(self, text):
        self.diagnose_text = text

    def clear_diagnose_text(self):
        self.diagnose_text = ""
            
    def get_jack_controller(self):
        if not self.proxy_jack_controller:
            self.proxy_jack_controller = JackController()
        return self.proxy_jack_controller

    def is_jack_controller_available(self):
        return self.proxy_jack_controller != None

    def get_jack_configure(self):
        if not self.proxy_jack_configure:
            self.proxy_jack_configure = JackConfigProxy()
        return self.proxy_jack_configure

    def clear_jack_proxies(self):
        self.proxy_jack_controller = None
        self.proxy_jack_configure = None

    def jack_is_available(self):
        try:
            proxy = self.get_jack_controller()
        except:
            return False
        return proxy and proxy.is_available()

    def jack_start(self):
# This has nothing to do here... I suppose
#        self.set_starting_status()
        self.get_jack_controller().start()

    def jack_stop(self):
        self.get_jack_controller().stop()

    def jack_reactivate(self):
        self.get_jack_controller().kill()
        self.clear_jack_proxies()

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
            self.proxy_a2j_controller = A2jController()
        return self.proxy_a2j_controller

    def clear_a2j_controller(self):
        self.proxy_a2j_controller = None

    def a2j_is_available(self):
        try:
            proxy = self.get_a2j_controller()
        except:
            return False
        if proxy.is_available():
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
            self.proxy_ladish_controller = LadishProxy()
        return self.proxy_ladish_controller

    def clear_ladish_controller(self):
        self.proxy_ladish_controller = None

    def ladish_is_available(self):
        try:
            proxy = self.get_ladish_controller()
        except:
            return False
        if proxy.is_available():
            return True
        self.clear_ladish_controller()
        return False

    def studio_is_loaded(self):
        return self.get_ladish_controller().studio_is_loaded()

    def studio_new(self):
        accept, name = self.name_dialog(_("New studio"), _("Studio name"), "")
        if accept:
            self.get_ladish_controller().studio_new(name)

    def studio_load(self, item, event, studio):
        self.get_ladish_controller().studio_load(studio)

    def studio_start(self):
        self.get_ladish_controller().studio_start()

    def studio_stop(self):
        self.get_ladish_controller().studio_stop()

    def name_dialog(self, title, label, text):
        dlg = Gtk.Dialog(
            title,
            None,
            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT)
        dlg.add_buttons (Gtk.STOCK_CANCEL,
                         Gtk.ResponseType.REJECT,
                         Gtk.STOCK_OK,
                         Gtk.ResponseType.ACCEPT)

        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label(label), True, True, 0)
        entry = Gtk.Entry()
        entry.set_text(text)
        hbox.pack_start(entry, True, True, 0)
        dlg.vbox.pack_start(hbox, True, True, 0)
        dlg.show_all()
        #entry.set_activates_default(True)
        #dlg.set_default_response(Gtk.ResponseType.OK)
        ret = dlg.run()
        dlg.destroy()
        if ret == Gtk.ResponseType.ACCEPT:
            return True, entry.get_text()
        else:
            return False, text

    def studio_rename(self):
        accept, name = self.name_dialog(_("Rename studio"),
                                        _("Studio name"),
                                        self.get_ladish_controller().studio_name())
        if accept:
            self.get_ladish_controller().studio_rename(name)

    def studio_save(self):
        self.get_ladish_controller().studio_save()

    def studio_unload(self):
        self.get_ladish_controller().studio_unload()

    def studio_delete(self, item, event, studio):
        dlg = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, Gtk.MessageType.ERROR, Gtk.ButtonsType.YES_NO, "")
        dlg.set_markup(_("<b><big>Confirm studio delete</big></b>"))
        dlg.format_secondary_text(_("Studio \"%s\" will be deleted. Are you sure?") % studio)
        ret = dlg.run()
        dlg.destroy()
        if ret == Gtk.ResponseType.YES:
            self.get_ladish_controller().studio_delete(studio)

    def ladish_reactivate(self):
        self.get_ladish_controller().kill()
        self.clear_ladish_controller()

    def on_menu_show_diagnose(self, widget, data=None):
        dlg = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, Gtk.MessageType.ERROR, Gtk.ButtonsType.CLOSE, self.diagnose_text)
        dlg.set_title(_("Cannot communicate JACK D-Bus"))
        dlg.run()
        dlg.destroy()

    def on_menu_command(self, widget, function):
        try:
            function()
        except Exception, e:
            error = Gtk.MessageDialog(None,
                                      Gtk.DialogFlags.MODAL,
                                      Gtk.MessageType.ERROR,
                                      Gtk.ButtonsType.OK,
                                      _("Error executing ") +
                                      repr(function) +
                                      _("Unexpected error\n\n") + repr(e))
            error.run()
            error.destroy()

    def on_menu_launcher(self, widget, exec_path):
        self.proc_list.append(subprocess.Popen([exec_path]))

    def menu_clear(self, menu):
        menu.foreach(lambda item,none: menu.remove(item), None)

    def studio_configure(self, item, event, module):
        self.proc_list.append(subprocess.Popen(["ladiconf", "-m", module]))

    def configure_list_fill(self, widget, function):
        menu = widget.get_submenu()
        self.menu_clear(menu)
        try:
            jack = self.get_jack_configure()
            # 'engine' item
            item = Gtk.MenuItem(_("JACK engine"))
            item.show()
            menu.append(item)
            item.connect("button-release-event", function, "engine")
            # 'params' item
            item = Gtk.MenuItem(_('JACK "%s" driver') % jack.get_selected_driver())
            item.show()
            menu.append(item)
            item.connect("button-release-event", function, "params")
            for internal in jack.read_container(['internals']):
                module = str(internal)
                item = Gtk.MenuItem(_('JACK "%s"') % module)
                item.show()
                menu.append(item)
                item.connect("button-release-event", function, module)
        except Exception, err:
            print str(err)
        if not menu.get_children():
            item = Gtk.MenuItem(_("Empty config list"))
            item.set_sensitive(False)
            item.show()
            menu.append(item)

    def studio_list_fill(self, widget, function):
        menu = widget.get_submenu()
        self.menu_clear(menu)
        try:
            for studio in self.get_ladish_controller().studio_list():
                item = Gtk.MenuItem(studio)
                item.show()
                menu.append(item)
                item.connect("button-release-event", function, studio) # "activate" is not used because of focus bug in pygtk
        except Exception, e:
            self.menu_clear(menu)
            item = Gtk.MenuItem(_("Error obtaining studio list"))
            item.set_sensitive(False)
            item.show()
            menu.append(item)
        if not menu.get_children():
            item = Gtk.MenuItem(_("Empty studio list"))
            item.set_sensitive(False)
            item.show()
            menu.append(item)

    def create_menu(self):
        menu_items = []

        if self.diagnose_text:
            menu_items.append((Gtk.ImageMenuItem(_("Diagnose")), self.on_menu_show_diagnose, None))
            menu_items.append((Gtk.SeparatorMenuItem.new(), None, None))

        if self.ladish_is_available():
            menu_items.append((Gtk.ImageMenuItem(_("Start gladish")), self.on_menu_launcher, "gladish"))

        # Add the laucher entries at the beginning of the menu
        for item in self.menu_array:
            # Replace "Configure" static item with the new sub-menu
            if item == 'configure':
                menu_items.append((Gtk.ImageMenuItem("Configure ..."), self.configure_list_fill, self.studio_configure))
                continue
            menu_label = item.capitalize() + "..."
            path = self.menu_array[item]
            menu_items.append((Gtk.ImageMenuItem(menu_label), self.on_menu_launcher, path))

        menu = Gtk.Menu()
        menu_items.append((Gtk.SeparatorMenuItem.new(),))
        if self.ladish_is_available():
            menu_items.append((Gtk.ImageMenuItem(_("New studio...")), self.on_menu_command, self.studio_new))
            menu_items.append((Gtk.ImageMenuItem(_("Load studio")), self.studio_list_fill, self.studio_load))
            if self.studio_is_loaded():
                menu_items.append((Gtk.SeparatorMenuItem.new(), None, None))
                menu_items.append((Gtk.ImageMenuItem(_("Start studio")), self.on_menu_command, self.studio_start))
                menu_items.append((Gtk.ImageMenuItem(_("Stop studio")), self.on_menu_command, self.studio_stop))
            menu_items.append((Gtk.SeparatorMenuItem.new(), None, None))
            if self.studio_is_loaded():
                menu_items.append((Gtk.ImageMenuItem(_("Rename studio...")), self.on_menu_command, self.studio_rename))
                menu_items.append((Gtk.ImageMenuItem(_("Save studio")), self.on_menu_command, self.studio_save))
                menu_items.append((Gtk.ImageMenuItem(_("Unload studio")), self.on_menu_command, self.studio_unload))
            menu_items.append((Gtk.ImageMenuItem(_("Delete studio")), self.studio_list_fill, self.studio_delete))
            menu_items.append((Gtk.ImageMenuItem(_("Reactivate ladishd")), self.on_menu_command, self.ladish_reactivate))
            menu_items.append((Gtk.SeparatorMenuItem.new(), None, None))
        if self.jack_is_available():
            if not self.jack_is_started():
                if not self.ladish_is_available():
                    menu_items.append((Gtk.ImageMenuItem(_("Start JACK server")), self.on_menu_command, self.jack_start))
            else:
                menu_items.append((Gtk.ImageMenuItem(_("Reset Xruns")), self.on_menu_command, self.jack_reset_xruns))
                if not self.ladish_is_available():
                    menu_items.append((Gtk.ImageMenuItem(_("Stop JACK server")), self.on_menu_command, self.jack_stop))
            menu_items.append((Gtk.ImageMenuItem(_("Reactivate JACK")), self.on_menu_command, self.jack_reactivate))
            menu_items.append((Gtk.SeparatorMenuItem.new(), None, None))
        if self.a2j_is_available():
            # when a2jmidid is used in used with ladish, a2j script should be used
            # for managing bridge "active" lifetime
            if not self.ladish_is_available():
                if not self.a2j_is_started():
                    menu_items.append((Gtk.ImageMenuItem(_("Start A2J bridge")), self.on_menu_command, self.a2j_start))
                else:
                    menu_items.append((Gtk.ImageMenuItem(_("Stop A2J bridge")), self.on_menu_command, self.a2j_stop))
            menu_items.append((Gtk.ImageMenuItem(_("Reactivate A2J")), self.on_menu_command, self.a2j_reactivate))
            menu_items.append((Gtk.SeparatorMenuItem.new(), None, None))
        if hasattr(self, 'on_about'):
            menu_items.append((Gtk.ImageMenuItem(_("About")), self.on_about, None))
        menu_items.append((Gtk.ImageMenuItem(_("Quit")), self.on_menu_command, Gtk.main_quit))

        for menu_tuple in menu_items:
            item = menu_tuple[0]
            if len(menu_tuple) > 1:
                callback = menu_tuple[1]
                exec_path = menu_tuple[2]
            menu.append(item)
            if type(item) is not Gtk.SeparatorMenuItem:
                if callback in (self.studio_list_fill, self.configure_list_fill):
                    item.set_submenu(Gtk.Menu())
                item.connect("activate", callback, exec_path)
        menu.show_all()
        return menu

    def menu_activate(self):
        menu = self.create_menu()
        menu.popup(parent_menu_shell=None,
                   parent_menu_item=None,
                   func=None,
                   data=None,
                   button=3,
                   activate_time=0)
        menu.reposition()
