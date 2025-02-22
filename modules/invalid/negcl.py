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
    'category'  :   'Invalid Messages',
    'test'      :   '(3.1.2.3) Negative Content-Length',
    'id'        :   'negcl'
}

def negcl():
    '''
    Negative Content-Length

    This request has a negative value for Content-Length.

    An element receiving this message should respond with an error.  This
    request appeared over UDP, so the remainder of the datagram can
    simply be discarded.
    '''
    log = logging.getLogger('negcl')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('INVITE')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: Modify the content length header
    head['Content-Length'] = '-%s' % random.getrandbits(10)
    # Forming the message up back again
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(negcl(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
