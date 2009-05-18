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
import thread
import threadframe
import traceback
from datetime import datetime
from cStringIO import StringIO
try:
    from zLOG import LOG, DEBUG
except ImportError:
    DEBUG = 1
    import logging
    def _log(title, level, msg):
        if level == DEBUG:
            logging.debug('%s %s' % (title, msg))
        else:
            logging.info('%s %s' % (title, msg))
    LOG = _log

import custom
from modules import MODULES

def dump_modules():
    return [mod() for mod in MODULES]

def dump_threads():
    """Dump running threads

    Returns a string with the tracebacks.
    """
    res = ['Dumping threads']
    frames = threadframe.dict()
    this_thread_id = thread.get_ident()

    for thread_id, frame in frames.iteritems():
        if thread_id == this_thread_id:
            continue
        # Find request in frame
        reqinfo = ''
        f = frame
        while f is not None:
            co = f.f_code
            #if (co.co_name == 'publish' and
            #    co.co_filename.endswith('/ZPublisher/Publish.py')):
            request = f.f_locals.get('request')
            if request is not None:
                method = request.get('REQUEST_METHOD', '')
                path = request.get('PATH_INFO', '')
                url = request.get('URL', '')
                agent = request.get('HTTP_USER_AGENT', '')
                query_string = request.get('QUERY_STRING')

                query = 'QUERY: %s %s' % (method, path_info)
                if query_string is not None:
                    query += '?%s' % query_string

                requinfo.append(query)

                # Add actual URL and user agent
                reqinfo.append('URL: %s' % URL)
                reqinfo.append('HTTP_USER_AGENT: %s' % AGENT)
                reqinfo = '\n'.join(reqinfo)
                break
            f = f.f_back

        output = StringIO()
        traceback.print_stack(frame, file=output)
        res.append("Thread %s%s:\n%s" %
            (thread_id, reqinfo, output.getvalue()))

    res.append("End of dump")
    return res

dump_url = custom.DUMP_URL
if custom.SECRET:
    dump_url += '?' + custom.SECRET

def match(self, request):
    uri = request.uri

    # added hook
    if uri == dump_url:
        dump = dump_modules()
        dump += dump_threads()
        request.channel.push('HTTP/1.0 200 OK\nContent-Type: text/plain\n\n')
        request.channel.push('\n'.join(dump))
        request.channel.close_when_done()
        LOG('DeadlockDebugger', DEBUG, '\n'.join(dump))
        return 0
    # end hook

    if self.uri_regex.match(uri):
        return 1
    else:
        return 0

try:
    from ZServer.HTTPServer import zhttp_handler
    zhttp_handler.match = match
except ImportError:
    pass  # not in a zope environment

