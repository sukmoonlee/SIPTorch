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
    'test'      :   'To header name length - 70',
    'id'        :   'to_name_70'
}


def to_name_70():
    '''
    SIP TO header name length

    SIP TO header name length
    '''
    log = logging.getLogger('to_name_70')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    if 70 <= 50:
        head['To'] = '"%s" <sip:%s@%s>' % (genCatfishString(70), config.DEF_EXT, config.RHOST)
    else:
        head['To'] = '"%s" <sip:%s@%s>' % (genCatfishString(70, allow_printable=True), config.DEF_EXT, config.RHOST)

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(to_name_70(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
