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
import time
import subprocess
from .controller import LadiController
from . import _gettext_domain
from . import LadiConfiguration
from . import JackConfigProxy
from . import JackController
from . import A2jController
from . import LadishProxy

class LadiManager(LadiController):

    def __init__(self, jack_autostart):
        self.proxy_jack_controller = None
        self.proxy_jack_configure = None
        self.proxy_a2j_controller = None
        self.proxy_ladish_controller = None
        self.jack_autostart = jack_autostart

        self.proc_list = {}

        if jack_autostart:
            self.jack_start()

    def is_available(self):
        return (self.ladish_is_available, self.jack_is_available, self.a2j_is_available)

    def is_started(self):
        return (self.ladish_is_started, self.jack_is_started, self.a2j_is_started)

    def start(self):
        self.studio_start()

    def stop(self):
        self.studio_stop()
    
    def kill(self):
        self.get_ladish_controller().kill()

    def killall(self):
        self.get_ladish_controller().kill()
        self.get_jack_controller().kill()
        self.get_a2j_controller().kill()
            
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

    def jack_start(self, *args, **kwargs):
# This has nothing to do here... I suppose
#        self.set_starting_status()
        self.get_jack_controller().start()

    def jack_stop(self, *args, **kwargs):
        self.get_jack_controller().stop()

    def jack_reactivate(self, *args, **kwargs):
        self.get_jack_controller().kill()
        self.clear_jack_proxies()

    def jack_reset_xruns(self, *args, **kwargs):
        self.get_jack_controller().reset_xruns()

    def jack_is_started(self, *args, **kwargs):
        return self.get_jack_controller().is_started()

    def jack_is_realtime(self, *args, **kwargs):
        return self.get_jack_controller().is_realtime()

    def jack_get_load(self, *args, **kwargs):
        return self.get_jack_controller().get_load()

    def jack_get_xruns(self, *args, **kwargs):
        return self.get_jack_controller().get_xruns()

    def jack_get_sample_rate(self, *args, **kwargs):
        return self.get_jack_controller().get_sample_rate()

    def jack_get_latency(self, *args, **kwargs):
        return self.get_jack_controller().get_latency()

    def get_a2j_controller(self, *args, **kwargs):
        if not self.proxy_a2j_controller:
            self.proxy_a2j_controller = A2jController()
        return self.proxy_a2j_controller

    def clear_a2j_controller(self, *args, **kwargs):
        self.proxy_a2j_controller = None

    def a2j_is_available(self, *args, **kwargs):
        try:
            proxy = self.get_a2j_controller()
        except:
            return False
        if proxy.is_available():
            return True
        self.clear_a2j_controller()
        return False

    def a2j_is_started(self, *args, **kwargs):
        return self.get_a2j_controller().is_started()

    def a2j_start(self, *args, **kwargs):
        self.get_a2j_controller().start()

    def a2j_stop(self, *args, **kwargs):
        self.get_a2j_controller().stop()

    def a2j_reactivate(self, *args, **kwargs):
        self.get_a2j_controller().kill()
        self.clear_a2j_controller()

    def get_ladish_controller(self, *args, **kwargs):
        if not self.proxy_ladish_controller:
            self.proxy_ladish_controller = LadishProxy()
        return self.proxy_ladish_controller

    def clear_ladish_controller(self, *args, **kwargs):
        self.proxy_ladish_controller = None

    def ladish_is_available(self, *args, **kwargs):
        try:
            proxy = self.get_ladish_controller()
        except:
            return False
        if proxy.is_available():
            return True
        self.clear_ladish_controller()
        return False

    def studio_is_loaded(self, *args, **kwargs):
        return self.get_ladish_controller().studio_is_loaded()

    def studio_is_started(self, *args, **kwargs):
        return self.get_ladish_controller().studio_is_started()

    def studio_new(self, *args, **kwargs):
        if 'name' in kwargs:
            name = kwargs['name']
            self.get_ladish_controller().studio_new(name)
            return True
        return False

    def studio_load(self, *args, **kwargs):
        if 'studio' in kwargs:
            studio = kwargs['studio']
            self.get_ladish_controller().studio_load(studio)
            return True
        return False

    def studio_start(self, *args, **kwargs):
        self.get_ladish_controller().studio_start()

    def studio_stop(self, *args, **kwargs):
        self.get_ladish_controller().studio_stop()

    def studio_name(self, *args, **kwargs):
        return self.get_ladish_controller().studio_name()

    def studio_rename(self, *args, **kwargs):
        if 'name' in kwargs:
            name = kwargs['name']
            if self.get_ladish_controller().studio_name() != name:
                self.get_ladish_controller().studio_rename(name)
                return True
        return False

    def studio_save(self, *args, **kwargs):
        self.get_ladish_controller().studio_save()

    def studio_unload(self, *args, **kwargs):
        self.get_ladish_controller().studio_unload()

    def studio_delete(self, *args, **kwargs):
        if 'studio' in kwargs:
            studio = kwargs['studio']
            self.get_ladish_controller().studio_delete(studio)
            return True
        return False

    def ladish_reactivate(self, *args, **kwargs):
        self.get_ladish_controller().kill()
        self.clear_ladish_controller()

    def launcher_exec(self, *args, **kwargs):
        if 'command' in kwargs:
            commandline = kwargs['command']
            command = commandline[0]
            if command not in self.proc_list.keys():
                self.proc_list[command] = subprocess.Popen(commandline)
            return True
        return False

    def launcher_kill(self, *args, **kwargs):
        if 'command' in kwargs:
            command = kwargs['command'][0]
            if command in self.proc_list:
                proc = self.proc_list[command]
                try:
                    proc.terminate()
                    time.sleep(0.5)
                    proc.kill()
                except OSError:
                    pass
        return False

    def update(self, *args, **kwargs):
        if self.__class__ == LadiManager:
            raise NotImplementedError("This is a virtual method")
        else:
            # Take a look at the processes we've started so we don't get any zombies
            for i in self.proc_list.keys():
                if self.proc_list[i].poll () != None:
                    self.proc_list.pop(i)
            return True

    def studio_list(self, *args, **kwargs):
        return self.get_ladish_controller().studio_list()
