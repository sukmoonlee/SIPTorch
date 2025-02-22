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
    'test'      :   '(3.1.2.18) Unknown Method with CSeq Method Mismatch',
    'id'        :   'metmatch'
}

def metmatch():
    '''
    Unknown Method with CSeq Method Mismatch

    This message has an unknown method in the start line, and a CSeq
    method tag that does not match.

    Any element receiving this response should respond with a 501 Not
    Implemented.  A 400 Bad Request is also acceptable, but choosing a
    501 (particularly at proxies) has better future-proof
    characteristics.
    '''
    log = logging.getLogger('metmatch')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('INVITE')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: Modify method line
    line = 'BLABLAMETHOD %s %s' % (
        mline.split(' ')[1], mline.split(' ')[2])
    # NOTE: We are not modifying the CSeq header since it is already
    # set to 1 INVITE, hence not messing up anyway
    # Forming the request message back up
    mg = concatMethodxHeaders(line, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(metmatch(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
