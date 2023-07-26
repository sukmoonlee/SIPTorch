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
    'test'      :   'Call-ID header name length - 3',
    'id'        :   'callid_name_3'
}


def callid_name_3():
    '''
    SIP Call-ID header name length

    SIP Call-ID header name length
    '''
    log = logging.getLogger('callid_name_3')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    if 3 <= 50:
        head['Call-ID'] = '"%s" <sip:%s@%s>' % (genCatfishString(3), config.DEF_EXT, config.RHOST)
    else:
        head['Call-ID'] = '"%s" <sip:%s@%s>' % (genCatfishString(3, allow_printable=True), config.DEF_EXT, config.RHOST)

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(callid_name_3(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
