#!/usr/bin/python
# LADITools - Linux Audio Desktop Integration Tools
# Copyright (C) 2011-2012 Alessio Treglia <quadrispro@ubuntu.com>
# Copyright (C) 2007-2010, Marc-Olivier Barre <marco@marcochapeau.org>
# Copyright (C) 2007-2009, Nedko Arnaudov <nedko@arnaudov.name>
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

# Let's make sure we'll place the file in an existing dir
from os import environ, sep, mkdir, path
from os.path import exists
from xdg import BaseDirectory as basedir
from ConfigParser import SafeConfigParser, MissingSectionHeaderError
import sys

try:
    import yaml
except:
    yaml = None

config_dir = path.join(basedir.xdg_config_home, 'laditools')
config_filename = path.join(config_dir, 'laditools.conf')
if not exists (config_dir):
    mkdir (config_dir, 0o755)

class MalformedConfigError(Exception):
    def __init__(self):
        Exception.__init__(self, """Malformed configuration file, \
delete the file '%s' and let me create a new one.""" % config_filename)

# Note to users of the config class. Only applications should create an instance
# of the config object. The ladimenu is *NOT* an application...
class LadiConfiguration(SafeConfigParser):
    """Convenient class for parsing and updating configuration files.
    
    It is recommended to avoid abuses of these objects, only applications
    should create instances of this class.
    """

    def _migrate_configuration(self):
        """Migrate configuration from old YAML coding style to the new one."""
        try:
            with open (config_filename, 'r') as config_file:
                appdict = yaml.load (config_file)
        except:
            sys.stderr.write("Config file doesn't exist, creating a new one...\n")
            sys.stderr.flush()
            return 1

        for section in appdict:
            if not section in self.sections():
                self.add_section(section)
            for opt in appdict[section]:
                if not isinstance(opt, dict):
                    self.set(section, opt, str(appdict[section][opt]))
                else:
                    for k in opt:
                        self.set(section, k, opt[k])

        self.appdict = appdict
        return 0

    def __init__ (self, args = None):

        SafeConfigParser.__init__(self)
        self.appdict = {}

        try:
            self.read(config_filename)
            for section in self.sections():
                self.appdict[section] = dict(self.items(section))
        except MissingSectionHeaderError:
            if yaml:
                self._migrate_configuration()
            # go on otherwise
        except:
            raise MalformedConfigError()

    def get_config_section (self, app_name):
        """Returns the section named <app_name> from the global configuration.
        
        If the section doesn't exist, returns an empty dictionary."""
        try:
            if app_name in self.appdict:
                return self.appdict[app_name]
            else:
                return {}
        except:
            return {}

    # Saves the section named <app_name> into the global config
    def set_config_section (self, app_name, param_dict):
        """Save the section named <app_name> into the global configuration."""
        self.appdict[app_name] = param_dict

    # This writes the config file to the disk
    def save (self):
        """Write configuration to file."""
        config_file = open (config_filename, 'w')
        self.write(config_file)
        config_file.close ()
