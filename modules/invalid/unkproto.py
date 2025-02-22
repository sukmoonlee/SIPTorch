#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import logging
from core.plugrun import runPlugin
from core.requester import buildreq
from core.requester.parser import parseSIPMessage, concatMethodxHeaders

module_info = {
    'category'  :   'Invalid Messages',
    'test'      :   '(3.1.2.16) Unknown Protocol Version',
    'id'        :   'unkproto'
}

def unkproto():
    '''
    Unknown Protocol Version

    To an element implementing RFC 3261, this request is malformed due
    to its high version number.

    The element should respond to the request with a 505 Version Not
    Supported error.
    '''
    log = logging.getLogger('unkproto')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: Change protocol version
    mline = mline.replace('SIP/2.0', 'SIP/7.0')
    head['Via'] = head['Via'].replace('SIP/2.0/UDP', 'SIP/7.0/UDP')
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(unkproto(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
