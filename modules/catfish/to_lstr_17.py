#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: smlee@sk.com
# This module requires SIPTorch
# https://github.com/sukmoonlee/SIPTorch

import logging
from libs import config
from core.requester import buildreq
from core.plugrun import runPlugin
from core.requester.parser import parseSIPMessage, concatMethodxHeaders
from mutators.replparam import genCatfishString

module_info = {
    'category'  :   'Catfish - Protocol',
    'test'      :   'To header left string length - 17',
    'id'        :   'to_lstr_17'
}


def to_lstr_17():
    '''
    SIP TO header left string length

    SIP TO header left string length
    '''
    log = logging.getLogger('to_lstr_17')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    if 17 <= 50:
        head['To'] = '"%s" <sip:%s@%s>' % (config.DEF_EXT, genCatfishString(17), config.RHOST)
    else:
        head['To'] = '"%s" <sip:%s@%s>' % (config.DEF_EXT, genCatfishString(17, allow_printable=True), config.RHOST)

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(to_lstr_17(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
