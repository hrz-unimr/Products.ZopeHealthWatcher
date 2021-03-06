#!/usr/bin/python
""" Zope Health Controller - inspired from :

- DeadlockDebugger : http://plone.org/products/deadlockdebugger

- MonitoringExchange :
  http://www.monitoringexchange.org/cgi-bin/page.cgi?g=Detailed%2F1354.html;d=1

"""
import sys
import json
import logging

from urllib import FancyURLopener
from Products.ZopeHealthWatcher.config import zhw_config

OK = (0, 'OK - %s')
WARNING = (1, 'WARNING - %s')
FAILURE = (2, 'FAILURE - %s')
CRITICAL = (3, 'CRITICAL - %s')


class ZHCOpener(FancyURLopener):
    version = 'ZopeHealthController'


def _read_url(url):
    result = ZHCOpener().open(url).read()
    return result


def _(status, msg):
    return status[0], status[1] % msg


def get_result(url):
    try:
        jdata = _read_url(url)
        info = json.loads(jdata)
    except Exception, e:
        return {}, _(FAILURE, str(e))

    stats = info['stats']

    total_threads = stats['total_threads']
    busy_count = stats['busy_count']
    zombie_count = stats['zombie_count']

    if total_threads:

        if busy_count < total_threads and busy_count >= 4:
            state = _(WARNING, '%s/%s thread(s) are working (high load)' %
                      (busy_count, total_threads))
        elif busy_count == total_threads:
            state = _(CRITICAL, '%s/%s thread(s) are working (busy)' %
                      (busy_count, total_threads))
        elif busy_count < total_threads:
            state = _(OK, '%s/%s thread(s) are working (ready)' %
                      (busy_count, total_threads))

    elif zombie_count > 0:
        state = _(CRITICAL, '%s/%s thread(s) died unexpectedly' %
                  (zombie_count, zombie_count + total_threads))
    else:
        # if Number of total_threads == 0, then the Zope instance
        # hadn't handled any request
        state = _(OK, 'zope is listening')

    return info, state


def main():
    url = sys.argv[1] + zhw_config.DUMP_URL
    logging.debug('Call URL: "%s"' % url)
    if zhw_config.SECRET:
        url = sys.argv[1] + zhw_config.SDUMP_URL
    info, state = get_result(url)

    # only if state != 0
    if state[0] != FAILURE[0]:
        if True or state[0] != OK[0]:
            modules = info['modules']
            threads = info['threads']

            if len(modules) > 0:
                print('Information:')
            for name, value in modules:
                print('%s %s' % (name, value))
            if len(threads) > 0:
                print('')
                print('Threads:')
                for thid, reqinfo, output in threads:
                    print ('Thread %s is %s' % (thid, output and 'busy'
                                                or 'sleeping'))
                    if reqinfo:
                        print('\n'.join(reqinfo))

    print('Status:')
    print(state[1])
    sys.exit(state[0])

if __name__ == "__main__":
    main()
