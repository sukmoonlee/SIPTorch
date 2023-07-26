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
    'test'      :   'Via header left string length - 80',
    'id'        :   'via_lstr_80'
}


def via_lstr_80():
    '''
    SIP Via header left string length

    SIP Via header left string length
    '''
    log = logging.getLogger('via_lstr_80')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseSIPMessage(msg)

    if 80 <= 50:
        head['Via'] = '%s %s' % (genCatfishString(80), head['Via'].split(" ", 1)[1])
    else:
        head['Via'] = '%s %s' % (genCatfishString(80, allow_printable=True), head['Via'].split(" ", 1)[1])

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(via_lstr_80(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
