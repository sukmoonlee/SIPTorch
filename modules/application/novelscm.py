#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import logging
from libs import config
from core.plugrun import runPlugin
from core.requester import buildreq
from core.requester.parser import parseSIPMessage, concatMethodxHeaders

module_info = {
    'category'  :   'Application Layer Semantics',
    'test'      :   '(3.3.3) Request-URI with Known but Atypical Scheme',
    'id'        :   'novelscm'
}

def novelscm():
    '''
    OPTIONS Request-URI with Known but Atypical Scheme

    This OPTIONS contains an Request-URI with an IANA-registered scheme
    that does not commonly appear in Request-URIs of SIP requests.  A
    parser must accept this as a well-formed SIP request.

    If an element will never accept this scheme as meaningful in a
    Request-URI, it is appropriate to treat it as unknown and return a
    416 Unsupported URI Scheme response.  If the element might accept
    some URIs with this scheme, then a 404 Not Found is appropriate for
    those URIs it doesn't accept.
    '''
    log = logging.getLogger('novelscm')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseSIPMessage(msg)
    requri = 'beep.boop://%s:%s' % (config.IP, config.RPORT)
    # Tweak 1: Remove the following required headers
    mline = mline.replace(mline.split(' ')[1], requri)
    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(novelscm(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
