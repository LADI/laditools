# LADITools - Linux Audio Desktop Integration Tools
# Copyright (C) 2007-2009, Marc-Olivier Barre and Nedko Arnaudov.
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

import yaml

# Let's make sure we'll place the file in an existing dir
from os import environ, sep, mkdir
from os.path import exists
config_dir = environ['HOME'] + sep + ".config" + sep + "laditools" + sep
config_filename = config_dir + "laditools.conf"
if not exists(config_dir):
    mkdir(config_dir, 0755)

class config:
    def __init__(self):
        try:
            self.appdict = yaml.load(config_filename)
        except:
            self.appdict = {}

    # Use this to create the dictionary that you'll use in your application
    # You can add remove any parameters you wish from it, it'll get saved magically
    def get_as_dict(self, app_name):
        if app_name in self.appdict:
            return self.appdict[app_name]
        else:
            return {}

    # Use this to create the array that you'll use in your application
    # The array is used when you want to take into account the order the items are listed in the file
    # You can add remove any parameters you wish from it, it'll get saved magically
    def get_as_array(self, app_name):
        if app_name in self.appdict:
            return self.appdict[app_name]
        else:
            return []

    # Use this when you want to update the yaml config with the content of the dictionary
    def set_as_dict(self, app_name, param_dict):
	self.appdict[app_name] = param_dict
        self.save()

    # Use this when you want to update the yaml config with the content of the array
    def set_as_array(self, app_name, param_array, element_name):
        self.appdict[app_name] = param_array, element_name
        self.save()

    # Use this when you want to write the config file to disk
    def save(self):
        config_file = open(config_filename, 'w')
        yaml.dump(self.appdict, config_file)
