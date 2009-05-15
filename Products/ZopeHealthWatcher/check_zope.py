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

OK = (0, 'OK - %s')
WARNING = (1, 'WARNING - %s')
FAILURE = (2, 'FAILURE - %s')

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
    threads = data.split('\n\n')

    # reading the headers
    time = threads[0].split()[1]
    sysload = threads[1].split()[1]
    meminfo = threads[2].split()[1]

    # now reading the rest of the dump
    idle = 0
    busy = []
    for line in threads[3:]:
        line = line.strip()
        if line in ('', 'End of dump'):
            continue
        sublines = line.split('\n')
        elems = lines[0].split()
        id = elems[1]
        if len(elems) > 2:
            req_url = '%s %s' % (elems[2], elems[3])
            req_url = req_url[1:-2]
            busy.append((id, requrl, '\n'.join(lines)))
        else:
            idle += 1
    return time, sysload, meminfo, idle, busy

def main():
    url = sys.argv[1]
    state, msg = get_result(url)
    print(msg)
    sys.exit(state)

def get_result(url):
    try:
        time, sysload, meminfo, idle, busy = query_zope(url)
    except Exception, e:
        return _(FAILURE, str(e))

    if idle == 0:
        state = _(CRITICAL, 'No more Zeo client available')
    elif len(busy) > (4*idle):
        state = _(WARNING, 'Warning, high load')
    else:
        state = _(OK, 'Everything looks fine')

    return state

if __name__ == "__main__":
    main()


