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
    'test'      :   '(3.1.2.5) Response Scalar Fields with Overlarge Values',
    'id'        :   'respsclarg'
}

def respsclarg():
    '''
    Response Scalar Fields with Overlarge Values

    This response contains several scalar header field values outside
    their legal range (>2**32-1). Note that the Warning header too has 
    value greater than 3 digits. An element receiving this response will 
    simply discard it.
    '''
    log = logging.getLogger('respsclarg')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: Modify the method line
    mline = 'SIP/2.0 503 Service Unavailable'
    # Tweak 2: Add retry after header
    head['Retry-After'] = '%s' % random.getrandbits(100)
    # Tweak 3: Add warning header
    head['Warning'] = '%s overture "In Progress"' % \
            random.randint(1000, 9999)
    # Tweak 4: Add large scalar value in cseq
    head['CSeq'] = head.get('CSeq').replace(
        head.get('CSeq').split(' ')[0], str(random.getrandbits(100)))
    # Forming the message up back again
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(respsclarg(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
