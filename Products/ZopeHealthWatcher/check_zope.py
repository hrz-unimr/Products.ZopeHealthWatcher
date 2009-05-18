#!/usr/bin/python
""" Zope Health Controller - inspired from :

- DeadlockDebugger : http://plone.org/products/deadlockdebugger

- MonitoringExchange :
  http://www.monitoringexchange.org/cgi-bin/page.cgi?g=Detailed%2F1354.html;d=1

"""
import os
import shutil
import sys
import urllib2
import custom

OK = (0, 'OK - %s')
WARNING = (1, 'WARNING - %s')
FAILURE = (2, 'FAILURE - %s')
CRITICAL = (3, 'CRITICAL - %s')

def _(status, msg):
    return status[0], status[1] % msg

def _read_url(url):
    url = urllib2.urlopen(url)
    try:
        return url.read()
    finally:
        url.close()

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
    busy = []
    for line in lines[index+1:]:
        line = line.strip()
        if line in ('', 'End of dump'):
            continue
        sublines = line.split('\n')
        elems = sublines[0].split()
        if len(elems) > 2:
            id = elems[0]
            req_url = '%s %s' % (elems[1], elems[2])
            req_url = req_url[1:-2]
            busy.append((id, req_url, '\n'.join(sublines)))
        else:
            idle += 1
    return modules, idle, busy

def main():
    url = sys.argv[1]
    url = '%s%s?%s' % (url, custom.DUMP_URL, custom.SECRET)
    modules, state = get_result(url)
    if len(modules) > 0:
        print('Information:')
    for name, value in modules:
        print('\t%s %s' % (name, value))
    print('')
    print(state[1])
    sys.exit(state[0])

def get_result(url):
    try:
        modules, idle, busy = query_zope(url)
    except Exception, e:
        return [], _(FAILURE, str(e))

    if idle == 0:
        state = _(CRITICAL, 'No more Zeo client available')
    elif len(busy) > (4*idle):
        state = _(WARNING, 'Warning, high load')
    else:
        state = _(OK, 'Everything looks fine')

    return modules, state

if __name__ == "__main__":
    main()


