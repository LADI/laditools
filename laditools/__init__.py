#!/usr/bin/python
# LADITools - Linux Audio Desktop Integration Tools
# Copyright (C) 2011-2012 Alessio Treglia <quadrispro@ubuntu.com>
# Copyright (C) 2007-2010, Marc-Olivier Barre <marco@marcochapeau.org>
# Copyright (C) 2007-2010, Nedko Arnaudov <nedko@arnaudov.name>
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

__version__ = (1, 0)
_gettext_domain = 'laditools'

get_version_string = lambda: '.'.join((str(comp)) for comp in __version__)

from .config import LadiConfiguration
from .a2j import A2jController
from .ladish import LadishProxy, LadishStatusType, LadishProxyError, check_ladish
from .jack import JackController, JackConfigProxy, JackConfigParameter
from .manager import LadiManager

from . import gtk

__all__ = ["gtk",
           "LadiConfiguration",
           "LadiManager",
           "A2jController",
           "LadishProxy",
           "LadishStatusType",
           "LadishProxyError",
           "check_ladish",
           "JackController",
           "JackConfigProxy",
           "JackConfigParameter"]
