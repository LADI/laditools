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

try:
    import xml.dom
    from xml.dom.minidom import parse, getDOMImplementation
    from xml.dom.ext import PrettyPrint
    xml_avalable = True
except:
    xml_avalable = False

# Let's make sure we'll place the file in an existing dir
from os import environ, sep, mkdir
from os.path import exists
config_dir = environ['HOME'] + sep + ".config" + sep + "laditools" + sep
config_filename = config_dir + "config.xml"
if not exists(config_dir):
    mkdir(config_dir, 0755)

class config:
    def __init__(self):
        self.app = {}
        if not xml_avalable:
            return
        try:
            self.doc = parse(config_filename)
            for child in self.doc.documentElement.childNodes:
                if child.nodeType == child.ELEMENT_NODE:
                    self.app[child.tagName] = child
        except:
            self.doc = getDOMImplementation().createDocument(None, "config", None)
            self.save()

    # This will clear an app node from it's children parameters
    def cleanup(self, app_name):
        if not xml_avalable:
            return
        replacement = self.doc.createElement(app_name)
        self.doc.documentElement.replaceChild(replacement, self.app[app_name])
        self.app[app_name] = replacement

    # Use this to create the dictionary that you'll use in your application
    # You can add remove any parameters you wish from it, it'll get saved magically
    def get_as_dict(self, app_name):
        param_dict = {}
        if not xml_avalable:
            return param_dict
        if app_name in self.app:
            for child in self.app[app_name].childNodes:
                if child.nodeType == child.ELEMENT_NODE:
                    attrib_dict = {}
                    text = ''
                    for grandchild_node in child.childNodes:
                        if grandchild_node.nodeType == child.TEXT_NODE:
                            text = grandchild_node.data
                    for i in range(child.attributes.length):
                        attrib_dict[child.attributes.item(i).name] = child.attributes.item(i).nodeValue
                    param_dict[child.tagName] = text, attrib_dict
            return param_dict
        else:
            new_app = self.doc.createElement(app_name)
            self.doc.documentElement.appendChild(new_app)
            self.app[app_name] = new_app
            return param_dict

    # Use this to create the array that you'll use in your application
    # The array is used when you want to take into account the order the items are listed in the file
    # You can add remove any parameters you wish from it, it'll get saved magically
    def get_as_array(self, app_name):
        param_array = []
        if not xml_avalable:
            return param_array
        if app_name in self.app:
            for child in self.app[app_name].childNodes:
                if child.nodeType == child.ELEMENT_NODE:
                    attrib_dict = {}
                    text = ''
                    for grandchild_node in child.childNodes:
                        if grandchild_node.nodeType == child.TEXT_NODE:
                            text = grandchild_node.data
                    for i in range(child.attributes.length):
                        attrib_dict[child.attributes.item(i).name] = child.attributes.item(i).nodeValue
                    param_array.append((text, attrib_dict))
            return param_array
        else:
            new_app = self.doc.createElement(app_name)
            self.doc.documentElement.appendChild(new_app)
            self.app[app_name] = new_app
            return param_array


    # Use this when you want to update the xml doc with the content of the dictionary
    def set_as_dict(self, app_name, param_dict):
        if not xml_avalable:
            return
        # Full cleanup to avoid keeping deprecated entries in the xml file
        self.cleanup(app_name)
        # Fill in the current list of parametters
        for param, value in param_dict.items():
            param_element = self.doc.createElement(param)
            text, attrib_dict = value
            if type(text) is not str:
                text = str(text)
            param_text = self.doc.createTextNode(text)
            for attribute_name, attribute_value in attrib_dict.items():
                if type(attribute_value) is not str:
                    attribute_value = str(attribute_value)
                param_element.setAttribute(attribute_name, attribute_value)
            param_element.appendChild(param_text)
            self.app[app_name].appendChild(param_element)
        self.save()

    # Use this when you want to update the xml doc with the content of the array
    def set_as_array(self, app_name, param_array, element_name):
        if not xml_avalable:
            return
        # Full cleanup to avoid keeping deprecated entries in the xml file
        self.cleanup(app_name)
        # Fill in the current list of parametters
        for text, attrib_dict in param_array:
            param_element = self.doc.createElement(element_name)
            if type(text) is not str:
                text = str(text)
            param_text = self.doc.createTextNode(text)
            for attribute_name, attribute_value in attrib_dict.items():
                if type(attribute_value) is not str:
                    attribute_value = str(attribute_value)
                param_element.setAttribute(attribute_name, attribute_value)
            param_element.appendChild(param_text)
            self.app[app_name].appendChild(param_element)
        self.save()

    # Use this when you want to write the config file to disk
    def save(self):
        if not xml_avalable:
            return
        config_file = open(config_filename, 'w')
        PrettyPrint(self.doc, config_file)
