=================
ZopeHealthWatcher
=================

ZopeHealthWatcher allows you to monitor the threads of a Zope application,
wether it's a Zeo client, wether it's a plain Zope server.

For each thread running on your server, you will know if it's active or
idling. When it's active, you will get an execution stack.

It's also useful to debug in case of a locked thread : you'll know
where the problem is located.

You can monitor it through your browser or through a console script.

`ZopeHealthWatcher` is based on `DeadlockDebugger` code,
see http://plone.org/products/deadlockdebugger.

Installation
============

If you run `zc.buildout`, add the ``ZopeHealthWatcher`` product into
your buildout file. For instance in a Plone buildout ::

    [buildout]
    ...
    eggs =
        ZopeHealthWatcher
    ...

You can also install it using `pip` or `easy_install`.

Configuration
=============

Once the package is installed, open the ``custom.py`` module located in
`ZopeHealthWatcher` and change ``ACTIVATED`` and ``SECRET`` values, so
the tool is activated::

    ACTIVATED = True
    SECRET = 'MySuperPass'

Usage
=====

There are two ways to query the tool: with the `zope_watcher` script or
through the browser.

zope_watcher
------------

`zope_watcher` takes the root URL of the Zope server to run::

    $ zope_watcher http://localhost:8080
    Idle: 4 Busy: 1
    OK - Everything looks fine

It will return the number of idling and busy threads.

In case your server is on high load (e.g. 4 busy threads), the tool will
return some relevant infos like the time, the sysload (only linux),
the memory information (only linux) and for each busy thread, the current
stack of execution, the query, the url and the user agent::

    $ zope_watcher http://localhost:8080
    Information:
            Time 2009-05-18T18:23:34.415319
            Sysload
            Meminfo

    Dump:
    Thread -1339518976
    QUERY: GET /test?
    URL: http://localhost:8080/test
    HTTP_USER_AGENT: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.10) Gecko/2009042315 Firefox/3.0.10
    File "/Volumes/MacDev/bitbucket.org/zopewatcher/parts/zope2/lib/python/ZServer/PubCore/ZServerPublisher.py", line 25, in __init__
        response=b)
        ...
        roles = getRoles(container, name, value, _noroles)

    Thread -1340051456
    QUERY: GET /test?
    URL: http://localhost:8080/test
    HTTP_USER_AGENT: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.10) Gecko/2009042315 Firefox/3.0.10
    File "/Volumes/MacDev/bitbucket.org/zopewatcher/parts/zope2/lib/python/ZServer/PubCore/ZServerPublisher.py", line 25, in __init__
        response=b)
        ...
        roles = getRoles(container, name, value, _noroles)

    Thread -1341648896
    not busy

    Thread -1341116416
    QUERY: GET /test?
    URL: http://localhost:8080/test
    HTTP_USER_AGENT: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.10) Gecko/2009042315 Firefox/3.0.10
    File "/Volumes/MacDev/bitbucket.org/zopewatcher/parts/zope2/lib/python/ZServer/PubCore/ZServerPublisher.py", line 25, in __init__
        response=b)
        ...
        roles = getRoles(container, name, value, _noroles)

    Thread -1340583936
    QUERY: GET /test?
    URL: http://localhost:8080/test
    HTTP_USER_AGENT: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.10) Gecko/2009042315 Firefox/3.0.10
    File "/Volumes/MacDev/bitbucket.org/zopewatcher/parts/zope2/lib/python/ZServer/PubCore/ZServerPublisher.py", line 25, in __init__
        response=b)
        ...
        roles = getRoles(container, name, value, _noroles)

    Idle: 1 Busy: 4
    WARNING - Warning, high load

If the server is down or unreachable, the script will return a failure::

    $ bin/zope_watcher http://localhost:8080
    Idle: 0 Busy: 0
    FAILURE - [Errno socket error] (61, 'Connection refused')

`zope_watcher` is also returning the right exit codes, so it can
be used by third party programs like Nagios:

- OK = 0
- WARNING = 1
- FAILURE = 2
- CRITICAL =3

web access
----------

An HTML version is accessible through the web, using the url
`http://host:port/manage_zhw?secret`. This url has to be changed depending
on the values entered in `custom.py`.

Beware that this URL is not password protected.

