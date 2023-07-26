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
    'test'      :   'CSeq header left string length - 90',
    'id'        :   'cseq_lstr_90'
}


def cseq_lstr_90():
    '''
    SIP CSeq header left string length

    SIP CSeq header left string length
    '''
    log = logging.getLogger('cseq_lstr_90')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)

    if 90 <= 50:
        head['CSeq'] = '%s INVITE' % genCatfishString(90)
    else:
        head['CSeq'] = '%s INVITE' % genCatfishString(90, allow_printable=True)

    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg


def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(cseq_lstr_90(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
