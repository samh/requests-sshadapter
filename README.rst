requests-sshadapter
===================
Currently a very basic module that provides an adapter for `requests
<http://pypi.python.org/pypi/requests>`_ that creates an SSH tunnel
(using the `bgtunnel <https://pypi.python.org/pypi/bgtunnel>`_ module),
using it to connect to an HTTP server.

How to use
----------
On a ``requests.Session`` object (or a subclass), call the ``mount``
method to register the adapter::

    ssh_adapter = SSHTunnelHTTPAdapter(ssh_user='samh', ssh_host='foo.bar')
    session = requests.Session()
    session.mount('http://', ssh_adapter)

When making a request, provide the URL as if you were connecting from the
remote server::

    r = session.get('http://localhost')

