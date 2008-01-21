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

import xml.dom
from xml.dom.minidom import parse
from xml.dom.ext import PrettyPrint

class config:
    def __init__(self, filename):
        self.load(filename)
        node_list = self.doc.getElementsByTagName('config')
        if node_list.length == 1:
            self.root = node_list[0]
        else:
            print "your XML file is fracked up"

    def load(self, filename):
        self.doc = parse('c:\\temp\\mydata.xml')

    def save(self, filename):
        PrettyPrint(self.doc, filename)

    def get_module_config(self, module_name):
        node_list = self.root.getElementsByTagName(module_name)
        if node_list.length == 1:
            return node_list[0].

    def append(self, section, name, value):
        self.doc.createElement(name)