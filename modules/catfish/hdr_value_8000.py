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
    'test'      :   'SIP Header Value length - 8000',
    'id'        :   'hdr_value_8000'
}


def hdr_value_8000():
    '''
    SIP Header Value Length

    use SIP User-Agent Header
    '''
    log = logging.getLogger('hdr_value_8000')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    if "8000" == "0":
        head['User-Agent'] = ''
    else:
        head['User-Agent'] = '%s' % genCatfishString(8000, printable=True)

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(hdr_value_8000(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
