from nose.tools import *

from Products.ZopeHealthWatcher.check_zope import get_result, FAILURE

def test_watcher():
    res = get_result('http://unexisting')
    assert_equals(res[0], FAILURE[0])


DUMP = """\
Time 2009-05-18T11:42:43.399882
Sysload
Meminfo
Thread -1341648896:
  File "/Library/Frameworks/Python.framework/Versions/2.4//lib/python2.4/threading.py", line 442, in __bootstrap
    self.run()
  File "/Library/Frameworks/Python.framework/Versions/2.4//lib/python2.4/threading.py", line 422, in run
    self.__target(*self.__args, **self.__kwargs)
  File "/Volumes/MacDev/bitbucket.org/zopewatcher/parts/zope2/lib/python/ZEO/zrpc/connection.py", line 59, in client_loop
    r, w, e = select.select(r, w, e, client_timeout)

End of dump
"""

import urllib2

def setup_server():
    class Request:
        def __init__(self, *args):
            pass
        def close(self):
            pass
        def read(self):
            return DUMP

    def _open(url):
        return Request(url)
    urllib2.old = urllib2.urlopen
    urllib2.urlopen = _open

def teardown_server():
    urllib2.urlopen = urllib2.old
    del urllib2.old


@with_setup(setup_server, teardown_server)
def test_caller():
    res = get_result('http://localhost:8080/manage_debug_threads?secret76')
    assert_equals(res, (0, 'OK - Everything looks fine'))

