#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import logging, random
from core.requester import buildreq
from core.plugrun import runPlugin
from core.requester.parser import parseSIPMessage, concatMethodxHeaders
from mutators.replparam import genRandStr

module_info = {
    'category'  :   'Application Layer Semantics',
    'test'      :   '(3.3.4) Unknown Request URI with Unknown Scheme in Header Fields',
    'id'        :   'unkscm2'
}

def unkscm2():
    '''
    Unknown Request URI with Unknown Scheme in Header Fields

    This message contains registered schemes in the To, From, and Contact
    header fields of a request.  The message is syntactically valid.
    Parsers must not fail when receiving this message.

    Proxies should treat this message as they would any other request for
    this URI.  A registrar would reject this request with a 400 Bad
    Request response, since the To: header field is required to contain a
    SIP or SIPS URI as an AOR.
    '''
    log = logging.getLogger('unkscm2')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('REGISTER')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: modify the header URI scheme
    head['To'] = '%s:%s' % (genRandStr(4), random.getrandbits(32))
    fromhead = head['From']
    head['From'] = fromhead.replace(fromhead.split(';')[0], '<http://example.com>')
    head['Contact'] = '<name:siptorch_flames>'
    # Forming the request message back up
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(unkscm2(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
