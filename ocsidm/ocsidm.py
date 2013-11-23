#!/usr/bin/python
"""
 $Id: ocsidm.py 1022 2013-10-06 18:57:21Z tbr $

 We check for an exisiting clusterware or oracle restart
 clusterware = no
  scan oratab for all ORACLE_SIDs
  clusteware is special in this situation. ORACLE_SID in oratab = DB_NAME

 clusterware = yes (Clusterware 11.2 or newer required!)

"""

from snack import *
import time, sys, os, commands

version = '$Id: ocsidm.py 1022 2013-10-06 18:57:21Z tbr $'
#orasidlist = []

# Dictionary with ORACLE_SID and ORACLE_HOME as value
ORACLE_SID_list = {}

# save current environment for later use
env_PATH = os.getenv('PATH')
env_LD_LIBRARY_PATH  = os.getenv('LD_LIBRARY_PATH')


def checkRequirements():
    if sys.platform not in ('linux2'):
        print "This script is only tested on Linux atm"
        print "current Platform: " + sys.platform
        return 'false'
    return 'true'


def execbash(orasid, orahome):
    print "Usind Envinronment in Shell:"
    print "ORACLE_SID      ", orasid
    print "ORACLE_HOME     ", orahome

    if orasid == None or orahome == None:
        print "Required Parameter are None"
        print "Returning to menu in 5 seconds"
        time.sleep(5)
        return

    if os.path.isdir(orahome) == False :
        print "ORACLE_HOME not exisitng!"
        print "Returning to menu in 5 seconds"
        time.sleep(5)
    else:
        if env_LD_LIBRARY_PATH == None:
            # we had no LD_LIBRARY_PATH at startup
            LD_LIBRARY_PATH = orahome + '/lib'
        else:
            LD_LIBRARY_PATH = orahome + '/lib:' + env_LD_LIBRARY_PATH

        os.putenv('ORACLE_HOME', orahome)
        os.putenv('LD_LIBRARY_PATH', LD_LIBRARY_PATH)
        os.putenv('ORACLE_SID', orasid)
        os.putenv('PATH', orahome + '/bin:' + env_PATH)

        # ORACLE_BASE is a complicated thing. :-(
        orabase = ''
        orabaseexe = orahome + '/bin/orabase'
        if os.path.isfile(orabaseexe):
            (result,orabase) = commands.getstatusoutput(orabaseexe)
            print "ORACLE_BASE     ", orabase

        print "Type: exit to go back to menu"
        # PS1 must be set with 'env' before starting the bash
        result = os.system('env PS1="[\u@\h \W] ("\$\{ORACLE_SID\}") \$ " bash  --noprofile --norc')
        if (result >> 8 ) != 0:
            print "Returncode != 0. Waiting 5 seconds before returning back to menu"
            time.sleep(5)


def menuorasidlist(screen, defaultitem = 0):
    global ORACLE_SID_list

    orasidlist = []
    # we built the menu when running Instances are found
    for ORACLE_SID in sorted(ORACLE_SID_list.keys()):
        orasidlist.append(ORACLE_SID)

    if orasidlist != []:
        lbcw = ListboxChoiceWindow(screen, 'Instances',
                    'Set Environment for Instance:',
                    orasidlist, default = defaultitem,
                    help = "")
        if lbcw[0] in (None, 'ok'):
            orasid =  orasidlist[lbcw[1]]
            orahome = ORACLE_SID_list[orasid]
            screen.suspend()
            execbash(orasid, orahome)
            screen.resume()
            # Restart screen with last selection
            menuorasidlist(screen, lbcw[1])


def check_oraclesid(ORACLE_SID, ORACLE_HOME):
    """
    check if pfile or spfile is existing for ORACLE_SID and ORACLE_HOME
    returncode 'True', 'False'

    ASM is a special situation. GridInfrastructure has no pfile or spfile for AsM
    => ORACLE_SID = +ASM* => True
    """

    # We don't have an init.ora or spfile.ora for ASM in CRS_HOME
    # We don't need to check for a valid home
    # => return True
    if ORACLE_SID[0:4] == '+ASM':
        return 'True'

    orapfile=ORACLE_HOME + '/dbs/'  + 'init'   + ORACLE_SID + '.ora'
    oraspfile=ORACLE_HOME + '/dbs/' + 'spfile' + ORACLE_SID + '.ora'
    if os.path.exists(orapfile):
        return 'True'
    elif os.path.exists(oraspfile):
        return 'True'
    return 'False'


def check_orasiddict():
    """
    check every entry in dictionary and removes invalid entries
    """
    global ORACLE_SID_list

    # check4clusterware = True
    # => We have a Grid-Infrastructure
    # => ORACLE_SID=db_name in oratab
    # => ORACLE_SID is not the real ORACLE_SID
    # we need to find the real ORACLE_SID
    if check4clusterware() == 'True':
        check_subsid = 'yes'
    else:
        check_subsid = 'no'

    for ORACLE_SID in ORACLE_SID_list.keys():
        # Do we have a cluster?
        # We need to ignore +ASM here, otherwise check_oraclesid will result in wrong results
        if check_subsid == 'yes' and ORACLE_SID[0:4] != '+ASM':
            # we try to find 4 SIDs in ORACLE_HOME/dbs
            # We add 4 entries for the Instance and check every entry
            for SIDid in range(1,5):
                # create dummy_ORACLE_SID
                dummy_ORACLE_SID = ORACLE_SID + str(SIDid)
                # Is that entry valid?
                # We check with ORACLE_HOME from ORACLE_SID for dummy_ORACLE_SID
                if check_oraclesid(dummy_ORACLE_SID, ORACLE_SID_list[ORACLE_SID]) == 'True':
                    # we add the new entry to dictionary!
                    ORACLE_SID_list[dummy_ORACLE_SID] = ORACLE_SID_list[ORACLE_SID]

        # We could have single instances on RAC-Cluster. Check is needed to find these instances
        # This check must come after the RAC-Check. Otherwise we will remove the needed entry from ORACLE_SID_list
        if check_oraclesid(ORACLE_SID, ORACLE_SID_list[ORACLE_SID]) == 'False':
            del ORACLE_SID_list[ORACLE_SID]


def check4clusterware():
    """
    return 'true'  when clusterware is found
    return 'false' when no clusterware is found

    clusterware = true when:
    /etc/oracle/ocr.loc is existing and local_only=FALSE
    """
    ocrcfg = '/etc/oracle/ocr.loc'
    if os.path.exists(ocrcfg) == True:
        # read the file
        ocrcfg = open(ocrcfg, 'r')
        for line in ocrcfg:
            if line.rstrip() == 'local_only=FALSE':
                # we have a real clusterware!
                return 'True'
    return 'False'


def readoratab():
    """
    Fill the dictionary from oratab ORACLE_SID_list
    """
    oratabfile='/etc/oratab'
    if os.path.exists(oratabfile) == False:
        print "no oratab found. Exiting script!"
        sys.exit(99)

    oratab = open(oratabfile, 'r')
    for line in oratab:
        linestr = line.rstrip()
        # filter all lines starting with '#'
        if linestr != '' and linestr[0] != '#':
            oratabline = line.split(':')
            # Fill Dictionary with ORACLE_SID as key and ORACLE_HOME as value
            ORACLE_SID_list[oratabline[0]] = oratabline[1]


print "(c) Thorsten Bruhns <thorsten.bruhns@opitz-consulting.com>"
print version

if checkRequirements() != 'true':
    sys.exit(1)
readoratab()
check_orasiddict()

screen = SnackScreen()
menuorasidlist(screen)
screen.finish()
