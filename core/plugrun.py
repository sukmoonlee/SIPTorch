#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#     SIP Torch     #
#-:-:-:-:-:-:-::-:-:#

# Author: 0xInfection
# This module requires SIPTorch
# https://github.com/0xInfection/SIPTorch

import os
import sys
import json
import socket
import logging
import pluginbase
from libs import config
from core.logger import logresp
from core.colors import color, G, GR
from core.requester import connector
from core.utils import checkBadResponse


def runPlugin(msg: str, minfo: dict):
    '''
    Perform the request and print results
    '''
    log = logging.getLogger('plugrun')
    if not msg:
        log.critical('Nothing received as request body')
        return
    if not config.TCP:
        sock = connector.sockinit()
    else:
        sock = connector.tcp_sockinit()
    print(GR, 'Running test: %s%s%s' % (color.ORANGE, minfo['test'], color.END))
    log.debug("Sending the request")
    try:
        log.debug('\n%sRequest:%s %s' % (color.RED, color.END, msg.strip()))
        if not config.TCP:
            connector.sendreq(sock, msg)
            data, *_ = connector.handler(sock)
        else:
            if not config.TLS:
                connector.tcp_sendreq(sock, msg)
                data, *_ = connector.tcp_handler(sock)
            else:
                ssock = connector.tcp_tls_sendreq(sock, msg)
                data, *_ = connector.tcp_tls_handler(sock, ssock)
        log.debug('\n%sResponse:%s %s' % (color.RED, color.END, data.strip()))
        if config.LOG_FILE:
            log.debug('Logging data to file')
            logdata = '''
### Test: %s
- Category: %s
- ID: `%s`
- Request:
```
%s
```
- Response:
```
%s
```''' % (minfo['test'], minfo['category'], minfo['id'], msg.strip(), data.strip())
            logresp(logdata)
        # We wait for more data
        if checkBadResponse(data):
            if not config.TCP:
                data, *_ = connector.handler(sock)
            else:
                if not config.TLS:
                    data, *_ = connector.tcp_handler(sock)
                else:
                    data, *_ = connector.tcp_tls_handler(sock, ssock)
            log.debug('\n%sResponse:%s %s' % (color.RED, color.END, data.strip()))
            if config.LOG_FILE:
                log.debug('Logging data to file')
                logdata = '''- Response Received Later:
```
%s
```
                ''' % data.strip()
                logresp(logdata)
        sock.close()  # Terminate the socket
        return True
    except socket.error as err:
        log.critical('Something\'s not right here: %s' % err.__str__())
        return


def buildcache(pluginlist):
    '''
    Builds a cache of modules present
    '''
    testtypes = [
        'Application Layer Semantics',
        'Backward Compatability Tests',
        'Invalid Messages',
        'Syntactical Parser Tests',
        'Transaction Layer Semantics',
        'Catfish - Protocol'
    ]
    memmap = dict()
    for test in testtypes:
        appender = list()
        for plug in pluginlist.list_plugins():
            loader = pluginlist.load_plugin(plug)
            if loader.module_info['category'] == test:
                appender.append(loader.module_info['test'])
        try:
            appender.sort(key=lambda x: int(x.split(")", 1)[0].split(".")[-1]))
        except ValueError:
            pass
        memmap[test] = appender
    with open('libs/modules.json', 'w+') as wf:
        json.dump(memmap, wf, indent=4)


def runAll(options=None):
    '''
    Runs all the plugins at once
    '''
    log = logging.getLogger('runAll')
    log.debug('Loading all modules')
    plugin = pluginbase.PluginBase(package='modules')
    pluginsource = plugin.make_plugin_source(
        searchpath=['./modules/application', 
                    './modules/backcomp', 
                    './modules/invalid',
                    './modules/parser',
                    './modules/transaction',
                    './modules/catfish'
                ])
    # pluginsource = plugin.make_plugin_source(searchpath=['./modules/application', './modules/backcomp'])
    if options is not None and options.build_cache:
        print('executing')
        buildcache(pluginsource)  # <- Uncomment this line to build cache
        return
    for plug in pluginsource.list_plugins():
        p = pluginsource.load_plugin(plug)
        p.run()
