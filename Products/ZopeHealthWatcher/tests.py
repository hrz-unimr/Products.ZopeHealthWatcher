from nose.tools import *

from Products.ZopeHealthWatcher.check_zope import get_result, FAILURE
from Products.ZopeHealthWatcher import check_zope

def test_watcher():
    modules, dump, idle, busy, state = \
             get_result('http://unexisting')
    assert_equals(state[0], FAILURE[0])


DUMP = """\
Time 2009-05-18T11:42:43.399882
Sysload
Meminfo
***
Thread -1341648896
not busy
"""

def setup_server():
    def _open(url):
        return DUMP
    check_zope.old = check_zope._read_url
    check_zope._read_url = _open

def teardown_server():
    check_zope._read_url = check_zope.old
    del check_zope.old

@with_setup(setup_server, teardown_server)
def test_caller():
    modules, dump, idle, busy, state = \
            get_result('http://localhost:8080/manage_debug_threads?secret76')
    assert_equals(state, (0, 'OK - Everything looks fine'))

