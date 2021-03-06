#!/usr/bin/python
#
# Copyright 2008-2011 Red Hat, Inc.
#
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Refer to the README and COPYING files for full details of the license
#

import sys
import getopt
import logging
from time import strftime

import deployUtil

log_filename = '/tmp/vds_bootstrap_complete.' + strftime("%Y%m%d_%H%M%S") + \
               '.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(module)s '
                           '%(lineno)d %(message)s',
                    filename=log_filename,
                    filemode='w')

VDSM_CONF_FILE = '/etc/vdsm/vdsm.conf'

def Reboot(act=1):
    """
        Reboot.
    """
    if act:
        print "<BSTRAP component='Reboot' status='OK'/>"
        deployUtil.reboot()
    else:
        print "<BSTRAP component='Reboot' status='FAIL'/>"
    sys.stdout.flush()

def main():
    """Usage: vds_bootstrap_complete.py  [-c vds_config_str] <random_num> [reboot]"""
    try:
        vds_config_str = None
        opts, args = getopt.getopt(sys.argv[1:], "c:")
        for o,v in opts:
            if o == "-c":
                # it should looks like: 'ssl=true;ksm_nice=5;images=/images/irsd'
                # without white spaces in it.
                vds_config_str = v

        rnum = args[0]
    except:
        print main.__doc__
        return 0
    try:
        arg = args[1]
    except:
        arg = 1

    res = True
    try:
        res = deployUtil.instCert(rnum, VDSM_CONF_FILE)
        if res:
            res = deployUtil.setCoreDumpPath()

        if res:
            res = deployUtil.cleanAll(rnum)

        if res:
            res = deployUtil.setVdsConf(vds_config_str, VDSM_CONF_FILE)

        deployUtil.setService("vdsmd", "reconfigure")

        Reboot(arg)
    except:
        logging.error('bootstrap complete failed', exc_info=True)
        res = False

    if res:
        print "<BSTRAP component='RHEV_INSTALL' status='OK'/>"
    else:
        print "<BSTRAP component='RHEV_INSTALL' status='FAIL'/>"
    sys.stdout.flush()

if __name__ == "__main__":
    sys.exit(main())
