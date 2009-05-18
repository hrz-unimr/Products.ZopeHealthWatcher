#!/usr/bin/python
""" Zope Health Controller - inspired from :

- DeadlockDebugger : http://plone.org/products/deadlockdebugger

- MonitoringExchange :
  http://www.monitoringexchange.org/cgi-bin/page.cgi?g=Detailed%2F1354.html;d=1

"""
import os
import shutil
import sys
import custom
from urllib import FancyURLopener

OK = (0, 'OK - %s')
WARNING = (1, 'WARNING - %s')
FAILURE = (2, 'FAILURE - %s')
CRITICAL = (3, 'CRITICAL - %s')

class ZHCOpener(FancyURLopener):
    version = 'ZopeHealthController'

def _read_url(url):
    return ZHCOpener().open(url).read()

def _(status, msg):
    return status[0], status[1] % msg

def query_zope(url):
    """Queries a Zope server"""
    data = _read_url(url)

    lines = data.split('\n')
    # reading the modules
    modules = []
    for index, line in enumerate(lines):
        line = line.strip()
        if line == '':
            continue
        if line == '***':
            break
        line = line.split()
        name = line[0]
        data = ' '.join(line[1:])
        modules.append((name, data))

    # now reading the rest of the dump
    idle = 0
    busy = 0
    index += 1
    dump = index
    while index < len(lines):
        if lines[index].startswith('Thread'):
            if index +1 < len(lines) and lines[index+1] == 'not busy':
                idle +=1
                index += 2
            else:
                busy += 1
                # jump to the next Thread
                index += 1
                while (index < len(lines) and
                       not lines[index].startswith('Thread')):
                    index += 1
        else:
            index += 1

    return modules, lines[dump:], idle, busy

def main():
    url = sys.argv[1]
    url = '%s%s?%s' % (url, custom.DUMP_URL, custom.SECRET)
    modules, dump, idle, busy, state = get_result(url)

    # only if state != 0
    if state[0] != 0:
        if len(modules) > 0:
            print('Information:')
        for name, value in modules:
            print('\t%s %s' % (name, value))
        if len(dump) > 0:
            print('')
            print('Dump:')
            print('\n'.join(dump))
            print('')

    print('Idle: %s\tBusy: %s' % (idle, busy))
    print(state[1])
    sys.exit(state[0])

def get_result(url):
    try:
        modules, dump, idle, busy = query_zope(url)
    except Exception, e:
        return [], '', 0, 0, _(FAILURE, str(e))
    if idle == 0:
        state = _(CRITICAL, 'No more Zeo client available')
    elif busy >= 4:
        state = _(WARNING, 'Warning, high load')
    else:
        state = _(OK, 'Everything looks fine')

    return modules, dump, idle, busy, state

if __name__ == "__main__":
    main()


