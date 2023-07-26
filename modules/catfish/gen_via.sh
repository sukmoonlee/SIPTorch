#!/bin/bash
set +o posix
################################################################################
# Generate Telecom SIP Test Python Code
# 2023.07.10 created by smlee@sk.com
################################################################################
SCRIPT_VERSION="20230710"
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8
HOSTNAME=$(hostname)

while [ "$#" -gt 0 ] ; do
case "$1" in
	-v|--version)
		echo "$0 $SCRIPT_VERSION"
		exit 0
		;;
	*)
		echo "Unknown option: $1"
		exit 1
esac
done

if [ "$FLAG_OS" != "FreeBSD" ] && [ -f "/usr/bin/readlink" ] ; then
	SCRIPT=$(/usr/bin/readlink -f "$0")
	SCRIPTPATH=$(/usr/bin/dirname "$SCRIPT")
	cd "$SCRIPTPATH" || exit 1
else
	SCRIPTPATH=$(/usr/bin/dirname "$0")
	cd "$SCRIPTPATH" || exit 1
fi
################################################################################
# Generate string
################################################################################
for i in $(seq 0 20) $(seq 30 10 100)
do
	id="via_branch_$i"

	{
		cat << EOF
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: smlee@sk.com
# This module requires SIPTorch
# https://github.com/sukmoonlee/SIPTorch

import logging
import socket
from libs import config
from core.requester import buildreq
from core.plugrun import runPlugin
from core.requester.parser import parseSIPMessage, concatMethodxHeaders
from mutators.replparam import genCatfishString

module_info = {
    'category'  :   'Catfish - Protocol',
    'test'      :   'Via header branch length - $i',
    'id'        :   '$id'
}


def $id():
    '''
    SIP Via header branch length

    SIP Via header branch length
    '''
    log = logging.getLogger('$id')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseSIPMessage(msg)

    srchost = socket.gethostbyname(socket.gethostname()) if not config.SRC_HOST else config.SRC_HOST
    if $i <= 50:
        head['Via'] = 'SIP/2.0/UDP %s:%s;branch=%s' % (srchost, config.LPORT, genCatfishString($i))
    else:
        head['Via'] = 'SIP/2.0/UDP %s:%s;branch=%s' % (srchost, config.LPORT, genCatfishString($i, allow_printable=True))

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin($id(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
EOF
} > "$id.py"
done

################################################################################
# Generate string
################################################################################
for i in $(seq 0 20) $(seq 30 10 100)
do
	id="via_lstr_$i"

	{
		cat << EOF
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: smlee@sk.com
# This module requires SIPTorch
# https://github.com/sukmoonlee/SIPTorch

import logging
from core.requester import buildreq
from core.plugrun import runPlugin
from core.requester.parser import parseSIPMessage, concatMethodxHeaders
from mutators.replparam import genCatfishString

module_info = {
    'category'  :   'Catfish - Protocol',
    'test'      :   'Via header left string length - $i',
    'id'        :   '$id'
}


def $id():
    '''
    SIP Via header left string length

    SIP Via header left string length
    '''
    log = logging.getLogger('$id')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseSIPMessage(msg)

    if $i <= 50:
        head['Via'] = '%s %s' % (genCatfishString($i), head['Via'].split(" ", 1)[1])
    else:
        head['Via'] = '%s %s' % (genCatfishString($i, allow_printable=True), head['Via'].split(" ", 1)[1])

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin($id(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
EOF
} > "$id.py"
done

################################################################################
# Generate string
################################################################################
for i in $(seq 0 20) $(seq 30 10 100)
do
	id="via_rstr_$i"

	{
		cat << EOF
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: smlee@sk.com
# This module requires SIPTorch
# https://github.com/sukmoonlee/SIPTorch

import logging
from core.requester import buildreq
from core.plugrun import runPlugin
from core.requester.parser import parseSIPMessage, concatMethodxHeaders
from mutators.replparam import genCatfishString

module_info = {
    'category'  :   'Catfish - Protocol',
    'test'      :   'Via header right string length - $i',
    'id'        :   '$id'
}


def $id():
    '''
    SIP Via header right string length

    SIP Via header right string length
    '''
    log = logging.getLogger('$id')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseSIPMessage(msg)

    if $i <= 50:
        head['Via'] = '%s %s' % (head['Via'].split(" ", 1)[0], genCatfishString($i))
    else:
        head['Via'] = '%s %s' % (head['Via'].split(" ", 1)[0], genCatfishString($i, allow_printable=True))

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin($id(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
EOF
} > "$id.py"
done

