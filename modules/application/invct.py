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
from mutators.replparam import genRandStr

module_info = {
    'category'  :   'Application Layer Semantics',
    'test'      :   '(3.3.6) Unknown/Invalid Content Type',
    'id'        :   'invct'
}

def invct():
    '''
    Unknown/Invalid Content Type

    This INVITE request contains a body of unknown type.  It is
    syntactically valid.  A parser must not fail when receiving it.

    A proxy receiving this request would process it just as it would any
    other INVITE.  An endpoint receiving this request would reject it
    with a 415 Unsupported Media Type error.
    '''
    log = logging.getLogger('invct')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('INVITE')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: Modify the content type
    head['Content-Type'] = 'application/%s' % genRandStr(10)
    # Tweak 2: Modify the body
    body = '<audio>\r\n  <pcmu port="443"/>\r\n</audio>'
    # Tweak 3: Modify the content-length
    head['Content-Length'] = '%s' % len(body)
    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(invct(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
