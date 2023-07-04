#!/bin/bash
set +o posix
################################################################################
# Generate Catfish Python Code
# 2023.07.03 created by smlee@sk.com
################################################################################
SCRIPT_VERSION="20230703"
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
# Header Name Length
################################################################################
for i in $(seq 0 100 1600) $(seq 2000 1000 9000)
do
	id="hdr_name_$i"

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
    'test'      :   'SIP Header Name length - $i',
    'id'        :   '$id'
}


def $id():
    '''
    SIP Header's Name Length

    use SIP User-Agent Header
    '''
    log = logging.getLogger('$id')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    key = genCatfishString($i)
    head[key] = head.pop('User-Agent')

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
# Header Value Length
################################################################################
for i in $(seq 0 100 1600) $(seq 2000 1000 9000)
do
	id="hdr_value_$i"

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
    'test'      :   'SIP Header Value length - $i',
    'id'        :   '$id'
}


def $id():
    '''
    SIP Header Value Length

    use SIP User-Agent Header
    '''
    log = logging.getLogger('$id')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    if "$i" == "0":
        head['User-Agent'] = ''
    else:
        head['User-Agent'] = '%s' % genCatfishString($i, printable=True)

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
