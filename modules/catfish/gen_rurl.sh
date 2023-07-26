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
# Generate number
################################################################################
for i in $(seq 0 20) $(seq 30 10 100)
do
	id="rurl_num_$i"

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
from mutators.replparam import genCatfishNumber

module_info = {
    'category'  :   'Catfish - Protocol',
    'test'      :   'Request URL number length - $i',
    'id'        :   '$id'
}


def $id():
    '''
    SIP Request URL number length

    SIP Request URL number length
    '''
    log = logging.getLogger('$id')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    mline = mline.replace(mline.split(" ")[1], r"sip:%s" % genCatfishNumber($i))

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
	id="rurl_lstr_$i"

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
from libs import config
from core.requester import buildreq
from core.plugrun import runPlugin
from core.requester.parser import parseSIPMessage, concatMethodxHeaders
from mutators.replparam import genCatfishString

module_info = {
    'category'  :   'Catfish - Protocol',
    'test'      :   'Request URL Left String length - $i',
    'id'        :   '$id'
}


def $id():
    '''
    Request URL Left String length

    Request URL Left String length
    '''
    log = logging.getLogger('$id')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    if $i <= 50:
        mline = mline.replace(mline.split(" ")[1], r"sip:%s@%s" % (genCatfishString($i), config.RHOST))
    else:
        mline = mline.replace(mline.split(" ")[1], r"sip:%s@%s" % (genCatfishString($i, allow_printable=True), config.RHOST))

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
	id="rurl_rstr_$i"

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
from libs import config
from core.requester import buildreq
from core.plugrun import runPlugin
from core.requester.parser import parseSIPMessage, concatMethodxHeaders
from mutators.replparam import genCatfishString

module_info = {
    'category'  :   'Catfish - Protocol',
    'test'      :   'Request URL Right String length - $i',
    'id'        :   '$id'
}


def $id():
    '''
    Request URL Right String length

    Request URL Right String length
    '''
    log = logging.getLogger('$id')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    if $i <= 50:
        mline = mline.replace(mline.split(" ")[1], r"sip:%s@%s" % (config.DEF_EXT, genCatfishString($i)))
    else:
        mline = mline.replace(mline.split(" ")[1], r"sip:%s@%s" % (config.DEF_EXT, genCatfishString($i, allow_printable=True)))

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

