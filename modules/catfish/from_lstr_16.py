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
    'test'      :   'From header left string length - 16',
    'id'        :   'from_lstr_16'
}


def from_lstr_16():
    '''
    SIP From header left string length

    SIP From header left string length
    '''
    log = logging.getLogger('from_lstr_16')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    if 16 <= 50:
        head['From'] = '"siptorch" <sip:%s@%s>' % (genCatfishString(16), config.RHOST)
    else:
        head['From'] = '"siptorch" <sip:%s@%s>' % (genCatfishString(16, allow_printable=True), config.RHOST)

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(from_lstr_16(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
