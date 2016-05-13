# (C) Copyright 2005 Nuxeo SARL <http://nuxeo.com>
# Author: Florent Guillaume <fg@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
"""Debug running threads

ZServer hook to dump a traceback of the running python threads.
"""
import os
import sys
import thread
import traceback
import logging
import json

from cStringIO import StringIO
from mako.template import Template

import ZServer.PubCore

from Products.ZopeHealthWatcher.config import zhw_config
from Products.ZopeHealthWatcher.modules import MODULES

log = logging.getLogger('Products.ZopeHealthWatcher')
lock = thread.allocate_lock()
_thread_info = {}


def zthread_stats():

    # Idea adopted from
    # https://github.com/RedTurtle/munin.zope/\
    #    blob/master/src/munin/zope/browser.py
    if ZServer.PubCore._handle is not None:
        handler_lists = ZServer.PubCore._handle.im_self._lists
    else:
        handler_lists = ((), (), ())
        # Check the ZRendevous __init__ for the definitions below
    busy_count, request_queue_count, free_count = [
        len(l) for l in handler_lists
        ]

    frames = sys._current_frames()
    this_thread_id = thread.get_ident()

    lock.acquire()
    try:
        for thread_id in frames.iterkeys():
            if this_thread_id == thread_id:
                continue
            _thread_info[thread_id] = 1
    finally:
        lock.release()

    total_threads = len(frames) - 1
    zombie_count = len(_thread_info) - total_threads

    res = {'total_threads': total_threads,
           'zombie_count': zombie_count,
           'busy_count': busy_count,
           'request_queue_count': request_queue_count,
           'free_count': free_count
           }

    return res


def dump_modules():
    return [mod() for mod in MODULES]


def dump_threads():
    """Dump running threads

    Returns a string with the tracebacks.
    """
    res = []
    frames = sys._current_frames()
    log.debug('Number of Threads: %s' % str(len(frames) - 1))
    # if Number of Threads == 0, then the Zope instance
    # hadn't handled any request
    this_thread_id = thread.get_ident()

    for thread_id, frame in frames.iteritems():
        if thread_id == this_thread_id:
            continue
        # Find request in frame
        reqinfo = ['']
        f = frame
        while f is not None:
            co = f.f_code
            if co.co_filename.endswith('Publish.py'):
                request = f.f_locals.get('request')
                if request is not None:
                    method = request.get('REQUEST_METHOD', '')
                    path = request.get('PATH_INFO', '')
                    url = request.get('URL', '')
                    agent = request.get('HTTP_USER_AGENT', '')
                    query_string = request.get('QUERY_STRING')

                    query = 'QUERY: %s %s' % (method, path)
                    if query_string is not None:
                        query += '?%s' % query_string

                    reqinfo.append(query)
                    reqinfo.append('URL: %s' % url)
                    reqinfo.append('HTTP_USER_AGENT: %s' % agent)
                    break
            f = f.f_back

        output = StringIO()
        traceback.print_stack(frame, file=output)
        output = output.getvalue()

        lines = [line.strip() for line in output.split('\n')
                 if line.strip() != '']
        zeo_marker = os.path.join('ZEO', 'zrpc', 'connection')
        acquire_marker = 'l.acquire()'
        if len(lines) > 1 and (zeo_marker in lines[-2] or
                               acquire_marker in lines[-1]):
            output = None

        res.append((thread_id, reqinfo, output))
    return res


def match(self, request):
    uri = request.uri

    # added hook
    if uri.startswith(zhw_config.DUMP_URL):
        page = ''
        stats = zthread_stats()
        total_threads = stats['total_threads']
        busy_count = stats['busy_count']
        zombie_count = stats['zombie_count']

        if total_threads:
            if busy_count < total_threads:
                msg = 'OK - %s/%s thread(s) are working (ready)' %\
                    (busy_count, total_threads)
                error_code = '200 OK'
            elif busy_count == total_threads:
                msg = 'CRITICAL - %s/%s thread(s) are working (busy)' %\
                    (busy_count, total_threads)
                error_code = '404 Not Found'
        elif zombie_count > 0:
            msg = 'CRITICAL - %s/%s thread(s) died unexpectedly\n' %\
                (zombie_count, zombie_count + total_threads)
            error_code = '500 Internal Server Error'
        else:
            msg = 'OK - zope is listening'
            error_code = '200 OK'

        # default content_type
        content_type = 'text/plain'

        # verbose output if authenticated
        if uri.endswith(zhw_config.SDUMP_URL):
            user_agent = request.get_header('User-Agent')
            if user_agent == 'ZopeHealthController':
                info = {'modules': dump_modules(),
                        'threads': dump_threads(),
                        'stats': stats
                        }
                page = json.dumps(info)
                content_type = 'application/json'
            else:
                # html version
                curdir = os.path.dirname(__file__)
                template = os.path.join(curdir, 'template.html')
                template = Template(open(template).read())
                page = str(template.render(modules=dump_modules(),
                                           threads=dump_threads(),
                                           msg=msg))
                content_type = 'text/html'

            log.debug(page)

        request.channel.push('HTTP/1.0 %s\n' % (error_code,))
        request.channel.push('Content-Type: %s\n\n' % content_type)
        if page:
            request.channel.push(page)
        request.channel.close_when_done()
        return 0

    # end hook

    if self.uri_regex.match(uri):
        return 1
    else:
        return 0
