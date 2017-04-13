#!/usr/bin/python
#
# Copyright 2013 (c) Thorsten Bruhns (tbruhns@gmx.de)
#

# Version: 0.2

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# Hilfe http://www.wanware.com/tsgdocs/snack.html
# http://sharats.me/the-ever-useful-and-neat-subprocess-module.html

from snack import *
import time, sys, os, getpass
import ConfigParser
version = '13.042017'

_hostlistcfgfile = 'hostlist.cfg'


def menuhostlist(screen, defaultitem = 0):
    global _hostlistcfgfile
    lbcw = []
    listitem = []

    Config = ConfigParser.ConfigParser()
    cfgfile = Config.read(_hostlistcfgfile)
    if cfgfile == []:
        screen.finish()
        print "hostlist.cfg not found!"
        sys.exit(1)
    configsections = sorted(Config.sections())

    for item in configsections:
        if Config.has_option(item, 'description'):
            vmdescription  = Config.get(item, 'description')
            listitem.append(item.ljust(20) + " " + vmdescription)
        else:
            listitem.append(item.ljust(20))

    lbcw = ListboxChoiceWindow(screen, 'Hostlist',
                    'Choose Target for SSH-Connection:',
                    listitem, default = defaultitem,  height = 10)

    # We start the ssh-session only when None or OK is returned.
    # a simple 'return' on the list give None and is ok in this situation
    if lbcw[0] in (None, 'ok'):
        sshhost = Config.get(configsections[lbcw[1]], 'hostname')

        try:
            sshuser = Config.get(configsections[lbcw[1]], 'username')
        except:
            sshuser = getpass.getuser()

        screen.suspend()
        oscmd = "ssh -X " + sshuser + "@" + sshhost
        os.system(oscmd)
        screen.resume()
        menuhostlist(screen, lbcw[1])

print "(c) Thorsten Bruhns <thorsten.bruhns@opitz-consulting.com>"
print version

if len(sys.argv) != 2:
    print "sshmenu <configfile>"
    sys.exit(-1)
_hostlistcfgfile = sys.argv[1]

screen = SnackScreen()
menuhostlist(screen)
screen.finish()
