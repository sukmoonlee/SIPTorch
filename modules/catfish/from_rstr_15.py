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
    'test'      :   'From header right string length - 15',
    'id'        :   'from_rstr_15'
}


def from_rstr_15():
    '''
    SIP From header right string length

    SIP From header right string length
    '''
    log = logging.getLogger('from_rstr_15')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    if 15 <= 50:
        head['From'] = '"siptorch" <sip:%s@%s>' % (config.DEF_EXT, genCatfishString(15))
    else:
        head['From'] = '"siptorch" <sip:%s@%s>' % (config.DEF_EXT, genCatfishString(15, allow_printable=True))

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(from_rstr_15(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
