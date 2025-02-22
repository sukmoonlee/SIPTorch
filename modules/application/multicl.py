#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import logging, random
from core.plugrun import runPlugin
from core.requester import buildreq
from core.requester.parser import parseSIPMessage, concatMethodxHeaders

module_info = {
    'category'  :   'Application Layer Semantics',
    'test'      :   '(3.3.9) OPTIONS with Multiple Content-Length Values',
    'id'        :   'multicl'
}

def multicl():
    '''
    OPTIONS with Multiple Content-Length Values

    If this request appeared over UDP, so the remainder of the datagram
    can simply be discarded.  If a request like this arrives over TCP,
    the framing error is not recoverable, and the connection should be
    closed.
    '''
    log = logging.getLogger('multicl')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: Add multiple content-length values
    head['content-length'] = random.getrandbits(6)
    # Recompiling our message
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(multicl(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
