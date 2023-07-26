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
    'test'      :   'Via header branch length - 3',
    'id'        :   'via_branch_3'
}


def via_branch_3():
    '''
    SIP Via header branch length

    SIP Via header branch length
    '''
    log = logging.getLogger('via_branch_3')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseSIPMessage(msg)

    srchost = socket.gethostbyname(socket.gethostname()) if not config.SRC_HOST else config.SRC_HOST
    if 3 <= 50:
        head['Via'] = 'SIP/2.0/UDP %s:%s;branch=%s' % (srchost, config.LPORT, genCatfishString(3))
    else:
        head['Via'] = 'SIP/2.0/UDP %s:%s;branch=%s' % (srchost, config.LPORT, genCatfishString(3, allow_printable=True))

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(via_branch_3(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
