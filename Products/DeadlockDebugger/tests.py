from nose.tools import *

from Products.ZopeHealthWatcher.check_zope import get_result, FAILURE

def test_watcher():

    res = get_result('http://unexisting')
    assert_equals(res[0], FAILURE[0])

