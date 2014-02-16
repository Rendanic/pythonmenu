#!/usr/bin/python
#
# Version 0.1
# $Id$
#
# Hilfe http://www.wanware.com/tsgdocs/snack.html
# http://sharats.me/the-ever-useful-and-neat-subprocess-module.html

from snack import *
import time, sys, os
import ConfigParser
version = '$Id: sshmenu.py 998 2013-10-05 09:29:25Z tbr $'

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
                    listitem, default = defaultitem)

    # We start the ssh-session only when None or OK is returned.
    # a simple 'return' on the list give None and is ok in this situation
    if lbcw[0] in (None, 'ok'):
        sshhost = Config.get(configsections[lbcw[1]], 'hostname')
        sshuser = Config.get(configsections[lbcw[1]], 'username')
        screen.suspend()
        oscmd = "ssh " + sshuser + "@" + sshhost
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
