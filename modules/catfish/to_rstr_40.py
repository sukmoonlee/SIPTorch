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
    'test'      :   'To header right string length - 40',
    'id'        :   'to_rstr_40'
}


def to_rstr_40():
    '''
    SIP TO header right string length

    SIP TO header right string length
    '''
    log = logging.getLogger('to_rstr_40')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    if 40 <= 50:
        head['To'] = '"%s" <sip:%s@%s>' % (config.DEF_EXT, config.DEF_EXT, genCatfishString(40))
    else:
        head['To'] = '"%s" <sip:%s@%s>' % (config.DEF_EXT, config.DEF_EXT, genCatfishString(40, allow_printable=True))

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(to_rstr_40(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
