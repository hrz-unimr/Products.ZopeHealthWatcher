from datetime import datetime
import os

LOAD_AVG = '/proc/loadavg'
MEM_INFO = '/proc/meminfo'

def _read_file(path):
    if not os.path.exists(path):
        return ''
    f = open(path)
    try:
        return f.read().strip()
    finally:
        f.close()

def time():
    return 'Time %s' % datetime.now().isoformat()

def sysload():
    return 'Sysload %s' % _read_file(LOAD_AVG)

def meminfo():
    return 'Meminfo %s' % _read_file(MEM_INFO)

MODULES = [time, sysload, meminfo]

