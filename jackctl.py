# base class for control apps, currently dockapp and tray app

import pygtk
pygtk.require('2.0')
import gtk
import gobject

class jackctl:
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

    # will this work for tray app?
    def menu_activate(self):
        self.menu.popup(None, None, None, 3, 0)
        self.menu.reposition()
