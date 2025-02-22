#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import logging, re, random
from libs import config
from core.plugrun import runPlugin
from core.requester import buildreq
from mutators.urlencchar import urlEncodeStrValid
from mutators.urlencchar import urlEncodeStrInvalid
from core.requester.parser import parseSIPMessage, concatMethodxHeaders

module_info = {
    'category'  :   'Syntactical Parser Tests',
    'test'      :   '(3.1.1.3) Valid Use of the % Escaping Mechanism',
    'id'        :   'escvalid'
}

def escvalid():
    '''
    Valid Use of the % Escaping Mechanism

    This INVITE exercises the % HEX HEX escaping mechanism in several
    places. The request is syntactically valid.

    A parser must accept this as a well-formed message.  The application
    using the message must treat the % HEX HEX expansions as equivalent
    to the character being encoded.  The application must not try to
    interpret % as an escape character in those places where % HEX HEX
    ("escaped" in the grammar) is not a valid part of the construction.
    In RFC 3261, "escaped" only occurs in the expansions of SIP-URI,
    SIPS-URI, and Reason-Phrase.
    '''
    log = logging.getLogger('escvalid')
    log.info('Testing module: %s' % module_info['test'])
    msg = buildreq.makeRequest('INVITE')
    mline, head, body = parseSIPMessage(msg)
    # Tweak 1: Modify the user part
    user = re.search(r'(sip:\w+?@[\w\.]+?)\s', mline, re.I).group(1)
    user = urlEncodeStrValid(user)
    # Now replace the grep inside the method
    mline = re.sub(r'sip:\w+@', 'sip:%s@' % user, mline)
    # Tweak 2: Modify the to and from headers
    head['To'] = 'sip:%s@%s' % (
        urlEncodeStrInvalid('user', value=2), config.RHOST)
    head['From'] = '<sip:%s@%s>;tag=%s' % (
        urlEncodeStrValid('I have spaces in user name'), 
        config.RHOST, random.getrandbits(32))
    # Tweak 3: modify the contact header
    head['Contact'] = '<sip:%s@%s;%s;%s=%s%s>' % (
        urlEncodeStrInvalid('caller', value=1),
        config.RHOST, urlEncodeStrInvalid('lr', value=2),
        urlEncodeStrInvalid('name', value=1),
        urlEncodeStrInvalid('value', value=2),
        r'%25%34%31'
    )
    # Forming the message up back again
    mg = concatMethodxHeaders(mline, head, body=body)
    return mg

def run():
    '''
    Run this module by sending the actual request
    '''
    log = logging.getLogger('run')
    if runPlugin(escvalid(), minfo=module_info):
        log.info('Module %s completed' % module_info['test'])
