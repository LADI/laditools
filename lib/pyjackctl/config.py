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

from xml.dom.minidom import parse, getDOMImplementation
from xml.dom.ext import PrettyPrint

# Let's make sure we'll place the file in an existing dir
from os import environ, sep, mkdir
from os.path import exists
config_dir = environ['HOME'] + sep + ".config" + sep + "pyjackctl" + sep
config_filename = config_dir + "config.xml"
if not exists(config_dir):
    mkdir(config_dir, 0755)

class config:
    def __init__(self):
        self.app = {}
        try:
            self.doc = parse(config_file)
            for child in self.doc.documentElement.childNodes:
                self.app[child.tagName] = child
        except:
            self.doc = getDOMImplementation().createDocument(None, "config", None)
            self.save()

    # This will clear an app node from it's children parameters
    def cleanup(self, app_name):
        for child in self.app[app_name].childNodes:
            self.app[app_name].removeChild(child)

    # Use this to create the dictionary that you'll use in your application
    # You can add remove any parameters you wish from it, it'll get saved magically
    def get(self, app_name):
        param_dict = {}
        if app_name in self.app:
            for child in self.app[app_name].childNodes:
                param_dict[child.tagName] = child.nodeValue
            return param_dict
        else:
            new_app = self.doc.createElement(app_name)
            self.doc.documentElement.appendChild(new_app)
            self.app[app_name] = new_app
            return param_dict

    # Use this when you want to update the xml doc with the content of your dictionary
    def set(self, app_name, param_dict):
        # Full cleanup to avoid keeping deprecated entries in the xml file
        self.cleanup(app_name)
        # Fill in the current list of parametters
        for param, value in param_dict.items():
            param_node = self.doc.createElement(param)
            self.app[app_name].appendChild(param_node)

    # Use this when you want to write the config file to disk
    def save(self):
        config_file = open(config_filename, 'w')
        PrettyPrint(self.doc, config_file)