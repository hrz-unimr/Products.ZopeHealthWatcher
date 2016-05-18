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

In addition, your front-end servers can efficiently check the status (health checking) of 
a Zope server without blocking the Zope application threads.

`ZopeHealthWatcher` is based on `DeadlockDebugger` code,
see http://plone.org/products/deadlockdebugger.

Installation
============

If you run `zc.buildout`, add the ``Products.ZopeHealthWatcher`` product into
your buildout file. 

For example ::

    [buildout]

    parts =
        zhw

    [zhw]
    recipe = zc.recipe.egg

    eggs = Products.ZopeHealthWatcher
    scripts = zHealthWatcher

You can also install it using `pip` or `easy_install`.

Configuration
=============

Once the package is installed, create the config file ``zopehealthwatcher.ini`` module located in
directory of the zope instance and add following lines, so
the tool is activated::

    [ZopeHealthWatcher]
    SECRET=secret

Usage
=====

There are three ways to query the tool: with the `zHealthWatcher` script, through the browser or http based health check clients.

zHealthWatcher
-------------------

`zHealthWatcher` takes the root URL of the Zope server to run::

    $ zHealthWatcher http://localhost:8080
    OK - 0/4 thread(s) are working (ready)

It will return the number of idling and busy threads.

In case your server is on high load (e.g. 4 busy threads), the tool will
return some relevant infos like the time, the sysload (only linux),
the memory information (only linux) and for each busy thread, the current
stack of execution, the query, the url and the user agent::

    $ zHealthWatcher http://localhost:8080
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

    WARNING - 4/5 thread(s) are working (high load)

If the server is down or unreachable, the script will return a failure::

    $ zHealthWatcher http://localhost:8080
    FAILURE - [Errno socket error] (61, 'Connection refused')

`zHealthWatcher` is also returning the right exit codes, so it can
be used by third party programs like Nagios:

- OK = 0
- WARNING = 1
- FAILURE = 2
- CRITICAL = 3

web access
----------

An HTML version is accessible through the web, using the url
`http://host:port/manage_zhw?secret`. This url has to be changed depending
on the values entered in `zopehealthwatcher.ini`.

Beware that this URL is not password protected.

    .. image:: http://bitbucket.org/tarek/zopewatcher/raw/ca8cb8e237eb/ZHW.png

health checking
---------------

In general, before performing traffic by a front-end server (e.g. load balancer)
forwarding to back-end Zope servers, it is recommended to tell the front-end server to check
the health of the Zope threads hosted by each Zope server of a farm. The
not password protected url `http://host:port/manage_zhw` can simply used 
without blocking a Zope thread for health checks by common known
web front-end servers like nginx, varnish or haproxy. The availability of a
Zope thread is encoded in the http response of the url::

    If the server has idle Zope threads, it will return
    $ curl -I http://localhost:8080/manage_zhw
    HTTP/1.0 200 OK
    ...

    If the server is busy (all Zope threads are busy), it will return
    $ curl -I http://localhost:8080/manage_zhw
    HTTP/1.0 404 Not Found
    ...

    If the server has zombie Zope threads or rather is in an undefined state, it will return
    $ curl -I http://localhost:8080/manage_zhw
    HTTP/1.0 500 Internal Server Error
    ...

