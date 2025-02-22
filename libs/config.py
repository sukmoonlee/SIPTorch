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

# Test URL to be tested, pass a domain here, if you have only IP
# pass same thing to both RHOST and IP fields
RHOST = ''
# Pass the IP here
IP = ''

# Target port to use
RPORT = 5060

# Local port to use
LPORT = 5060

############################
# Parts of the SIP message #
############################

# Whether to use a hardcoded string as Call-ID
STATIC_CID = False
# If you're using a static call id put it here
CALL_ID = None

# WARNING: Changing from/to headers might break some tests
# Strictly stick to the format -> "name" ext@(site|IP).tld
# From address to use
FROM_ADDR = ''
# Embed a static from tag here if you want it to be static
FROM_TAG = None

# To address to use
TO_ADDR = ''

# Source host to use
SRC_HOST = None

# Default Cseq value to use
CSEQ = 1

# User-agent to use
USER_AGENT = 'siptorch/0.1'

# Contact header to use
CONTACT = None

# Accept value to use
ACCEPT = 'application/sdp'

# Branch ID to use (embed a hardcoded static branch tag)
BRANCH = None

# Content type for the body you provided
CONTENT_TYPE = None

# Extra headers to add to the default header set for some specific tests
EXT_HEADERS = {
    r'UnknownHeaderWithUnusualValue'    :   r';;,,;;,;',
    r'NewFangledHeader'                 :   r'''   newfangled value\r\ncontinued newfangled value''',
}

# Identity header to be used for specific tests only (sample data)
IDENTITY = r'eyJhbGciOiJFUzI1NiIsInR5cCI6InBhc3Nwb3J0IiwieDV1I'
IDENTITY += r'joiaHR0cHM6Ly9jZXJ0LmV4YW1wbGUub3JnL3Bhc3Nwb3J0LmNlciJ9.eyJ'
IDENTITY += r'kZXN0Ijp7InVyaSI6WyJzaXA6YWxpY2VAZXhhbXBsZS5jb20iXX0sImlhdC'
IDENTITY += r'I6IjE0NDMyMDgzNDUiLCJvcmlnIjp7InRuIjoiMTIxNTU1NTEyMTIifX0.r'
IDENTITY += r'q3pjT1hoRwakEGjHCnWSwUnshd0-zJ6F1VOgFWSjHBr8Qjpjlk-cpFYpFYs'
IDENTITY += r'ojNCpTzO3QfPOlckGaS6hEck7w;info=<https://0xInfection.xyz/random.cert>'

# Invite body to use
# maintain the x.x.x.x and y.y.y.y because they will be replaced dynamically
# for some tests, x.x.x.x => IPv4 for caller, y.y.y.y => IPv4 of callee
INVITE_BODY =  'v=0\r\n'
INVITE_BODY += 'o=mhandley 29739 7272939 IN IP4 x.x.x.x\r\n'
INVITE_BODY += 's=-\r\n'
INVITE_BODY += 'c=IN IP4 y.y.y.y\r\n'
INVITE_BODY += 't=0 0\r\n'
INVITE_BODY += 'm=audio 49217 RTP/AVP 0 12\r\n'
INVITE_BODY += 'm=video 3227 RTP/AVP 31\r\n'
INVITE_BODY += 'a=rtpmap:31 LPC'

# TO be implemented later
IP6_SUPPORT = False

# Request method to test. If this var is set to "all" then all existing
# tests will be done, otherwise specify your method explicitly
# METHOD = "INVITE"
# METHOD = 'all'

# Default extension to test against
DEF_EXT = "2000"

# Default header set
DEF_HSET = {
    'Allow'         : 'INVITE, ACK, CANCEL, BYE, NOTIFY, REFER, MESSAGE, OPTIONS, INFO, SUBSCRIBE',
    'Max-Forwards'  : '70',
    'Accept'        : ACCEPT,
    'Call-ID'       : CALL_ID
}

# Timeout to use
TIMEOUT = 5

# Delay between requests
DELAY = 0

# Binding interface to use
BIND_IFACE = '0.0.0.0'

# Log to file bool
LOG_FILE = True

# Default output directory to use
OUTPUT_DIR = './siptorch-output/'

# Spoof User-Agents
SPOOF_UA = False

# SIP Proxy Mode
PROXY = False

# TCP TLS/SIP Mode
TCP = False
TLS = False

# Debug level
DEBUG_LEVEL = 30
