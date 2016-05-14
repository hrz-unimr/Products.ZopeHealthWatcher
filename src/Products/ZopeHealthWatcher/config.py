import logging
from ConfigParser import SafeConfigParser
from ConfigParser import NoSectionError

log = logging.getLogger('Procucts.ZopeHealthWatcher')

class ZopeHealthWatcherConfig(object):

    def __init__(self, secret=None):
        parser = SafeConfigParser()
        filename = 'zopehealthwatcher.ini'
        ini = parser.read(['etc/%s' % filename, filename])
        if not ini:
            raise ImportError
        self.SECRET = parser.get('ZopeHealthWatcher', 'SECRET')
        self.DUMP_URL = '/manage_zhw'
        self.SDUMP_URL = self.DUMP_URL + '?' + self.SECRET


try:
    zhw_config = ZopeHealthWatcherConfig()
except (ImportError, NoSectionError):
    msg = ('Not activated, you must set a SECRET in a '
           'config file `zopehealthwatcher.ini` in the current '
           'directory or, if you are running zope, in the config '
           'dir of your zope instance.'
           """

The file should look like this:

[ZopeHealthWatcher]
SECRET = <SECRET>

""")
    raise ImportError(msg)
