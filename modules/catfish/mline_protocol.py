#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: smlee@sk.com
# This module requires SIPTorch
# https://github.com/sukmoonlee/SIPTorch

import logging
from core.requester import buildreq
from core.plugrun import runPlugin
from core.requester.parser import parseSIPMessage, concatMethodxHeaders
from mutators.replparam import genCatfishString

module_info = {
    'category'  :   'Catfish - Protocol',
    'test'      :   'SIP Request Line - Protocol',
    'id'        :   'mline_protocol'
}


def mline_protocol():
    '''
    SIP Request line test

    [[ABC,1,1000,100]] sip:sktims.net SIP/2.0
    '''
    log = logging.getLogger('mline_protocol')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    mline = mline.replace(mline.split(" ")[2], genCatfishString(100, printable=True))

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(mline_protocol(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
