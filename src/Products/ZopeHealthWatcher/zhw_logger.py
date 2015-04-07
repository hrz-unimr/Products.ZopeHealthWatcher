try:
    from zLOG import LOG
    from zLOG import DEBUG
    from zLOG import INFO
    from zLOG import WARNING
    from zLOG import ERROR
    from zLOG import CRITICAL
except ImportError:
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    import logging
    logger = logging.getLogger()

    def LOG(title, level, msg):
        if level == NOTSET:
            pass
        if level == DEBUG:
            logger.debug('%s %s' % (title, msg))
        if level == INFO:
            logger.info('%s %s' % (title, msg))
        if level == WARNING:
            logger.warning('%s %s' % (title, msg))
        if level == ERROR:
            logger.error('%s %s' % (title, msg))
        if level == CRITICAL:
            logger.critical('%s %s' % (title, msg))
        else:
            pass
