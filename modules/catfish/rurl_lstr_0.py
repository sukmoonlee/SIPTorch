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
    'test'      :   'Request URL Left String length - 0',
    'id'        :   'rurl_lstr_0'
}


def rurl_lstr_0():
    '''
    Request URL Left String length

    Request URL Left String length
    '''
    log = logging.getLogger('rurl_lstr_0')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    if 0 <= 50:
        mline = mline.replace(mline.split(" ")[1], r"sip:%s@%s" % (genCatfishString(0), config.RHOST))
    else:
        mline = mline.replace(mline.split(" ")[1], r"sip:%s@%s" % (genCatfishString(0, allow_printable=True), config.RHOST))

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(rurl_lstr_0(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
