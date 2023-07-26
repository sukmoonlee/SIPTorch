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
from mutators.replparam import genCatfishNumber

module_info = {
    'category'  :   'Catfish - Protocol',
    'test'      :   'Request URL number length - 11',
    'id'        :   'rurl_num_11'
}


def rurl_num_11():
    '''
    SIP Request URL number length

    SIP Request URL number length
    '''
    log = logging.getLogger('rurl_num_11')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    mline = mline.replace(mline.split(" ")[1], r"sip:%s" % genCatfishNumber(11))

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(rurl_num_11(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
