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
    'test'      :   'CSeq header number length - 18',
    'id'        :   'cseq_num_18'
}


def cseq_num_18():
    '''
    SIP CSeq header number length

    SIP CSeq header number length
    '''
    log = logging.getLogger('cseq_num_18')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('OPTIONS')
    mline, head, body = parseSIPMessage(msg)

    head['CSeq'] = '%s INVITE' % genCatfishNumber(18)

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(cseq_num_18(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
