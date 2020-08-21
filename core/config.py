#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

# This file contains all core config variables to be used 
# during the SIP torture tests

# Test URL to be tested
TEST_URL = 'demo.sipvicious.pro'

# Local port to use
LPORT = 5060

# Parts of the SIP message
##########################

# Whether to use a hardcoded string as Call-ID
STATIC_CID = False
# If you're using a static call id put it here
CALL_ID = None

# User-agent to use
USER_AGENT = 'siptorch/0.1'

# Contact header to use
CONTACT = '1234@1.1.1.1'

# Accept value to use
ACCEPT = 'application/sdp'

# Branch ID to use (embed a hardcoded static branch tag)
BRANCH = None

# Extra headers to add to the default header set
EXT_HEADERS = {
    r'UnknownHeaderWithUnusualValue'    :   r';;,,;;,;',
    r'NewFangledHeader'                 :   r'''   newfangled value\r\ncontinued newfangled value''',
}

# Invite body to use
INVITE_BODY = '''v=0\r\no=mhandley 29739 7272939 IN IP4 x.x.x.x\r\ns=-\r\nc=IN IP4 y.y.y.y\r\nt=0 0\r\nm=audio 49217 RTP/AVP 0 12\r\nm=video 3227 RTP/AVP 31\r\na=rtpmap:31 LPC'''

# TO be implemented later
IP6_SUPPORT = False

# Request method to test. If this var is set to "all" then all existing
# tests will be done, otherwise specify your method explicitly
# METHOD = "INVITE" 
METHOD = 'all'

# Default extension to test against
DEF_EXT = "1000"

# Default header set
DEF_HSET = {
    'Allow'         : 'INVITE, ACK, CANCEL, BYE, NOTIFY, REFER, MESSAGE, OPTIONS, INFO, SUBSCRIBE',
    'Max-Forwards'  : '70',
    'User-Agent'    : USER_AGENT,
    'Contact'       : CONTACT,
    'Accept'        : ACCEPT,
    'Call-ID'       : CALL_ID
}

# Timeout to use
TIMEOUT = 7

# Binding interface to use
BIND_IFACE = 'any'