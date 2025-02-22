#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import logging
from core.requester import buildreq
from core.plugrun import runPlugin
from core.requester.parser import parseSIPMessage, concatMethodxHeaders

module_info = {
    'category'  :   'Application Layer Semantics',
    'test'      :   '(3.3.11) Zero Value in Max-Forwards Header',
    'id'        :   'mfzero'
}

def mfzero():
    '''
    Zero Value in Max-Forwards Header

    A proxy should not forward the request and should respond 483 (Too
    Many Hops).  An endpoint should process the request as if the Max-
    Forwards field value were still positive.
    '''
    log = logging.getLogger('reqpreq')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: Add zero to max-forwards
    head['Max-Forwards'] = '0'
    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(mfzero(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
