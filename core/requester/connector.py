#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import os
from libs import config
import socket, logging, select, time
import ssl
from core.requester.parser import parseResponse


def sockinit():
    '''
    Initiates a socket connection
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(config.TIMEOUT)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return sock


def sendreq(sock, data):
    '''
    Sends the request to the server
    '''
    dst = (config.IP, config.RPORT)
    # Added delay functionality
    if config.DELAY > 0:
        time.sleep(config.DELAY)
    while data:
        # SIP RFC states the default serialized encoding is utf-8
        bytes_sent = sock.sendto(bytes(data[:8192], 'utf-8'), dst)
        data = data[bytes_sent:]


def handler(sock):
    '''
    Listens for incoming messages
    '''
    log = logging.getLogger('handler')
    bindingface = config.BIND_IFACE
    localport = config.LPORT
    # Descriptors to use during async I/O waiting
    rlist = [sock]
    wlist, xlist = list(), list()
    log.debug("Binding to %s:%s" % (bindingface, config.LPORT))
    try:
        sock.bind((bindingface, localport))
    except socket.error:
        pass
    while True:
        data, *_ = select.select(rlist, wlist, xlist, config.TIMEOUT)
        if data:
            buff, src = sock.recvfrom(8192)
            daff, host, port = parseResponse(buff, src)
            log.debug("Data received from: %s:%s" % (str(host), str(port)))
            return (daff, host, port)
        else:
            try:
                buff, src = sock.recvfrom(8192)
                daff, host, port = parseResponse(buff, src)
                log.debug("Data received from: %s:%s" % (str(host), str(port)))
                return (daff, host, port)
            except socket.timeout:
                message = 'Generic timeout occured - no reply received.\n'
                message += 'It is highly probable that the server might have '
                message += 'encountered an issue which handling this request.\n'
                message += 'Investigate your server logs.'
                log.error('Timeout occured when waiting for message')
                return (message, '', '')
            except socket.error as err:
                log.error("Target errored out: %s" % (err.__str__()))
                return ('Error Enountered: %s' % err.__str__(), '', '')


def proxy_handler(sock, data):
    '''
    Listens for incoming messages
    '''
    log = logging.getLogger('proxy_handler')
    bindingface = config.BIND_IFACE
    localport = config.LPORT
    # Descriptors to use during async I/O waiting
    rlist = [sock]
    wlist, xlist = list(), list()
    log.debug("Binding to %s:%s" % (bindingface, localport))
    try:
        sock.bind((bindingface, localport))
    except socket.error as error:
        log.error("socket binding error : (%d) %s" % (error.errno, os.strerror(error.errno)))

    s = sockinit()
    sendreq(s, data)

    while True:
        data, *_ = select.select(rlist, wlist, xlist, config.TIMEOUT)
        if data:
            buff, src = sock.recvfrom(8192)
            daff, host, port = parseResponse(buff, src)
            log.debug("Data received from: %s:%s" % (str(host), str(port)))
            s.close()  # Terminate the socket
            return (daff, host, port)
        else:
            try:
                buff, src = sock.recvfrom(8192)
                daff, host, port = parseResponse(buff, src)
                log.debug("Data received from: %s:%s" % (str(host), str(port)))
                s.close()  # Terminate the socket
                return (daff, host, port)
            except socket.timeout:
                message = 'Generic timeout occured - no reply received.\n'
                message += 'It is highly probable that the server might have '
                message += 'encountered an issue which handling this request.\n'
                message += 'Investigate your server logs.'
                log.error('Timeout occured when waiting for message')
                s.close()  # Terminate the socket
                return (message, '', '')
            except socket.error as err:
                log.error("Target errored out: %s" % (err.__str__()))
                s.close()  # Terminate the socket
                return ('Error Enountered: %s' % err.__str__(), '', '')


def tcp_sockinit():
    '''
    Initiates a TCP socket connection
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(config.TIMEOUT)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock


def tcp_sendreq(sock, data):
    '''
    Sends the request to the server
    '''
    sock.connect((config.IP, config.RPORT))
    # localport = sock.getsockname()[1]

    # Added delay functionality
    if config.DELAY > 0:
        time.sleep(config.DELAY)
    while data:
        # SIP RFC states the default serialized encoding is utf-8
        bytes_sent = sock.send(bytes(data[:8192], 'utf-8'))
        data = data[bytes_sent:]


def tcp_handler(sock):
    '''
    Listens for incoming messages
    '''
    log = logging.getLogger('tcp_handler')
    # Descriptors to use during async I/O waiting
    rlist = [sock]
    wlist, xlist = list(), list()
    while True:
        data, *_ = select.select(rlist, wlist, xlist, config.TIMEOUT)
        if data:
            try:
                buff = sock.recv(8192)
                src = (config.IP, config.RPORT)
                daff, host, port = parseResponse(buff, src)
                log.debug("Data received from: %s:%s" % (str(host), str(port)))
                return (daff, host, port)
            except socket.timeout:
                log.error('Timeout occured when waiting for message')
                return ('Timeout occured when waiting for message', '', '')
            except socket.error as err:
                log.error("Target errored out: %s" % (err.__str__()))
                return ('Error Enountered: %s' % err.__str__(), '', '')
        else:
            try:
                buff = sock.recv(8192)
                src = (config.IP, config.RPORT)
                daff, host, port = parseResponse(buff, src)
                log.debug("Data received from: %s:%s" % (str(host), str(port)))
                return (daff, host, port)
            except socket.timeout:
                message = 'Generic timeout occured - no reply received.\n'
                message += 'It is highly probable that the server might have '
                message += 'encountered an issue which handling this request.\n'
                message += 'Investigate your server logs.'
                log.error('Timeout occured when waiting for message')
                return (message, '', '')
            except socket.error as err:
                log.error("Target errored out: %s" % (err.__str__()))
                return ('Error Enountered: %s' % err.__str__(), '', '')


def tcp_tls_sendreq(sock, data):
    '''
    Sends the request to the server
    '''
    context = ssl.create_default_context()
    sock = socket.create_connection((config.IP, config.RPORT))
    # ssock = context.wrap_socket(sock, server_hostname=config.RHOST)
    context.check_hostname = False
    ssock = context.wrap_socket(sock)
    ssock.settimeout(config.TIMEOUT)

    # Added delay functionality
    if config.DELAY > 0:
        time.sleep(config.DELAY)
    while data:
        # SIP RFC states the default serialized encoding is utf-8
        bytes_sent = ssock.send(bytes(data[:8192], 'utf-8'))
        data = data[bytes_sent:]

    return ssock


def tcp_tls_handler(sock, ssock):
    '''
    Listens for incoming messages
    '''
    log = logging.getLogger('tcp_tls_handler')
    # Descriptors to use during async I/O waiting
    rlist = [sock]
    wlist, xlist = list(), list()
    while True:
        data, *_ = select.select(rlist, wlist, xlist, config.TIMEOUT)
        if data:
            try:
                buff = ssock.recv(8192)
                src = (config.IP, config.RPORT)
                daff, host, port = parseResponse(buff, src)
                log.debug("Data received from: %s:%s" % (str(host), str(port)))
                return (daff, host, port)
            except socket.timeout:
                log.error('Timeout occured when waiting for message')
                return ('Timeout occured when waiting for message', '', '')
            except socket.error as err:
                log.error("Target errored out: %s" % (err.__str__()))
                return ('Error Enountered: %s' % err.__str__(), '', '')
        else:
            try:
                buff = ssock.recv(8192)
                src = (config.IP, config.RPORT)
                daff, host, port = parseResponse(buff, src)
                log.debug("Data received from: %s:%s" % (str(host), str(port)))
                return (daff, host, port)
            except socket.timeout:
                message = 'Generic timeout occured - no reply received.\n'
                message += 'It is highly probable that the server might have '
                message += 'encountered an issue which handling this request.\n'
                message += 'Investigate your server logs.'
                log.error('Timeout occured when waiting for message')
                return (message, '', '')
            except socket.error as err:
                log.error("Target errored out: %s" % (err.__str__()))
                return ('Error Enountered: %s' % err.__str__(), '', '')
