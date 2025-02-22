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
    'category'  :   'Application Layer Semantics',
    'test'      :   '(3.3.12) REGISTER with a Contact Header Parameter',
    'id'        :   'cparam1'
}

def cparam1():
    '''
    REGISTER with a Contact Header Parameter

    This register request contains a contact where the 'unknownparam'
    parameter must be interpreted as a contact-param and not a url-param.

    This REGISTER should succeed.  The response must not include
    "unknownparam" as a url-parameter for this binding.  Likewise,
    "unknownparam" must not appear as a url-parameter in any binding
    during subsequent fetches.
    '''
    log = logging.getLogger('cparam1')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: Add an unknwown param to contact header
    head['Contact'] += ';unknownparam'
    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(cparam1(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
