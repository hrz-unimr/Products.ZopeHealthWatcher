import logging
from ConfigParser import SafeConfigParser
from ConfigParser import NoSectionError

log = logging.getLogger('Procucts.ZopeHealthWatcher')


class ZopeHealthWatcherConfig(object):

    def __init__(self, secret=None):
        parser = SafeConfigParser()
        parser.read('zopehealthwatcher.ini')

        self.SECRET = parser.get('ZopeHealthWatcher', 'SECRET')
        self.DUMP_URL = '/manage_zhw'
        self.SDUMP_URL = self.DUMP_URL + '?' + self.SECRET


zhw_config = None
try:
    zhw_config = ZopeHealthWatcherConfig()
except NoSectionError:
    log.error('Not activated, you must set a SECRET in a '
              'config file `zopehealthwatcher.ini` in the base '
              'directory of your zope instance.'
              """

The file should look like this:

[ZopeHealthWatcher]
SECRET = <SECRET>

""")
