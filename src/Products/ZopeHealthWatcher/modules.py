from datetime import datetime
import os
import sys

MEM_INFO = '/proc/meminfo'


def _read_file(path):
    if not os.path.exists(path):
        return ''
    with open(path) as f:
        return f.read().strip()


def time():
    return ['Time', datetime.now().isoformat()]


def threads():
    return ['Number of Worker Threads', str(len(sys._current_frames()) - 1)]


def sysload():
    return ['Sysload', os.getloadavg()]


def meminfo():
    return ['Meminfo', _read_file(MEM_INFO)]

MODULES = [time, threads, sysload, meminfo]
