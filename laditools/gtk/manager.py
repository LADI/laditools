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
from .. import _gettext_domain
from .. import LadiManager

# Default launcher menu :
menu_default = {"Logs": "ladilog"}

class LadiManagerGtk(LadiManager):
    def __init__(self, jack_autostart):
        LadiManager.__init__(self, jack_autostart)

    def set_diagnose_text(self, text):
        self.diagnose_text = text

    def clear_diagnose_text(self):
        self.diagnose_text = ""

    def name_dialog(self, title, label, oldname):
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
        entry.set_text(oldname)
        hbox.pack_start(entry, True, True, 0)
        dlg.vbox.pack_start(hbox, True, True, 0)
        dlg.show_all()
        #entry.set_activates_default(True)
        #dlg.set_default_response(Gtk.ResponseType.OK)
        ret = dlg.run()
        newname = entry.get_text().strip()
        dlg.destroy()
        if ret == Gtk.ResponseType.ACCEPT and newname and (not newname in self.studio_list()) and newname != oldname:
            return True, newname
        else:
            return False, oldname

    def studio_new(self, *args, **kwargs):
        accept, name = self.name_dialog(_("New studio"), _("Studio name"), "")
        if accept:
            LadiManager.studio_new(self, name=name)

    def studio_rename(self, *args, **kwargs):
        accept, name = self.name_dialog(_("Rename studio"),
                                        _("Studio name"),
                                        self.studio_name())
        if accept:
            return LadiManager.studio_rename(self, name=name)
        return False

    def studio_delete(self, *args, **kwargs):
        if not 'studio' in kwargs:
            return False
        studio = kwargs['studio']
        dlg = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL, Gtk.MessageType.ERROR, Gtk.ButtonsType.YES_NO, "")
        dlg.set_markup(_("<b><big>Confirm studio delete</big></b>"))
        dlg.format_secondary_text(_("Studio \"%s\" will be deleted. Are you sure?") % studio)
        ret = dlg.run()
        dlg.destroy()
        if ret == Gtk.ResponseType.YES:
            LadiManager.studio_delete(self, studio=studio)
            return True
        return False

    def studio_configure(self, item, event, module):
        LadiManager.launcher_exec(self, command=['ladiconf', '-m', module])
