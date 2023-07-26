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
    'test'      :   'From header name length - 100',
    'id'        :   'from_name_100'
}


def from_name_100():
    '''
    SIP From header name length

    SIP From header name length
    '''
    log = logging.getLogger('from_name_100')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    if 100 <= 50:
        head['From'] = '"%s" <sip:%s@%s>' % (genCatfishString(100), config.DEF_EXT, config.RHOST)
    else:
        head['From'] = '"%s" <sip:%s@%s>' % (genCatfishString(100, allow_printable=True), config.DEF_EXT, config.RHOST)

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(from_name_100(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
