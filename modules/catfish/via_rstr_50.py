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
    'test'      :   'Via header right string length - 50',
    'id'        :   'via_rstr_50'
}


def via_rstr_50():
    '''
    SIP Via header right string length

    SIP Via header right string length
    '''
    log = logging.getLogger('via_rstr_50')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseSIPMessage(msg)

    if 50 <= 50:
        head['Via'] = '%s %s' % (head['Via'].split(" ", 1)[0], genCatfishString(50))
    else:
        head['Via'] = '%s %s' % (head['Via'].split(" ", 1)[0], genCatfishString(50, allow_printable=True))

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(via_rstr_50(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])