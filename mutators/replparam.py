#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import random
import string
import logging

hard = 'someval=value'


def genRandStr(length, allow_digits=False):
    '''
    Generates a random string depending on choice
    '''
    if not allow_digits:
        result = "".join(random.choice(
            string.ascii_lowercase) for i in range(length))
    else:
        result = "".join(random.choice(
            string.ascii_lowercase + string.digits) for i in range(length))
    return result


def genCatfishString(length, allow_printable=False):
    '''
    Generates a random string depending on choice for catfish
    '''
    if not allow_printable:
        result = "".join(random.choice(
            string.ascii_letters + string.digits) for i in range(length))
    else:
        result = "".join(random.choice(
            string.printable) for i in range(length))
    return result


def genCatfishNumber(length, allow_first_zero=False):
    '''
    Generates a random number depending on choice for catfish
    '''
    if length <= 0:
        return ""
    if allow_first_zero:
        result = "".join(random.choice(
            string.digits) for i in range(length))
    else:
        result = "".join(random.choice(
            "123456789") for i in range(1))
        if length > 1:
            result += "".join(random.choice(
                string.digits) for i in range(length - 1))
    return result


def getCatfishRandomPhone(prefix="010"):
    '''
    Generates a random phone number for catfish
    '''
    return prefix + genCatfishNumber(8)


def replParam(mg: str, hardcoded=False):
    '''
    Replaces parameters with junk values
    '''
    log = logging.getLogger('replParam')
    if not mg:
        log.error('Nothing available for parsing')
        return
    if ';' not in mg:
        log.error('No parameters found for parsing')
        return
    msg = mg.split(';', 1)[1]
    ins = mg.split(';', 1)[0]
    for x in msg.split(';'):
        if '=' in x:
            if hardcoded:
                msg = msg.replace(x, hard)
            else:
                y = x.split('=')
                if y[0].lower() != 'branch':
                    msg = msg.replace(y[0], genRandStr(len(y[0])))
                    msg = msg.replace(y[1], genRandStr(len(y[1])))
        else:
            msg = msg.replace(x, genRandStr(len(x)))
    # Forming the final string
    final = '%s%s%s' % (ins, ';', msg)
    return final


def rmallParam(msg: str):
    '''
    Removes the parameter specified
    '''
    log = logging.getLogger('rmallParam')
    if not msg:
        log.error('Nothing available for parsing')
        return
    log.debug('Received: %s' % msg)
    if ';' not in msg:
        log.error('No parameters found for parsing')
        return
    return msg.split(';', 1)[0]


def rmspcParam(mg: str, param='branch'):
    '''
    Removes a specified param
    '''
    log = logging.getLogger('rmspcParam')
    if not mg:
        log.error('Nothing available for parsing')
        return
    log.debug('Received: %s' % mg)
    if ';' not in mg:
        log.error('No parameters found for parsing')
        return
    msg = mg.split(';', 1)[1]
    ins = mg.split(';', 1)[0]
    for x in msg.split(';'):
        if '=' in x:
            if x.split('=')[0].lower() == param.lower():
                msg = msg.replace(x, '')
        else:
            msg = msg.replace(x, '')
    # Forming the final string
    if msg != '':
        final = '%s%s%s' % (ins, ';', msg)
    else:
        final = ins
    return final
