"""
Uses the "bgtunnel" package to establish an SSH tunnel in the background,
using it to forward HTTP connections.

Modeled roughly on the UnixAdapter from docker-py
(https://github.com/dotcloud/docker-py/blob/master/docker/unixconn/unixconn.py)
"""
import httplib
import bgtunnel
import requests.adapters
import urlparse
from requests.packages.urllib3 import connectionpool


class SSHTunnelHTTPConnection(httplib.HTTPConnection):
    def __init__(
            self, host, ssh_user, ssh_host, ssh_port, host_address, host_port):
        self.ssh_user = ssh_user
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.host_address = host_address
        self.host_port = host_port
        self.tunnel = None
        httplib.HTTPConnection.__init__(self, host)

    def connect(self):
        self.tunnel = bgtunnel.open(
            ssh_user=self.ssh_user,
            ssh_address=self.ssh_host, ssh_port=self.ssh_port,
            host_address=self.host_address, host_port=self.host_port,
            silent=True
        )
        self._set_hostport(self.host, self.tunnel.bind_port)
        return httplib.HTTPConnection.connect(self)

    def close(self):
        self.tunnel.close()


class SSHTunnelHTTPConnectionPool(connectionpool.HTTPConnectionPool):
    def __init__(self, ssh_user, ssh_host, ssh_port, host_address, host_port):
        self.ssh_user = ssh_user
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.host_address = host_address
        self.host_port = host_port
        connectionpool.HTTPConnectionPool.__init__(self, 'localhost')

    def _new_conn(self):
        return SSHTunnelHTTPConnection(
            self.host, self.ssh_user, self.ssh_host, self.ssh_port,
            self.host_address, self.host_port)


class SSHTunnelHTTPAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, ssh_user, ssh_host, ssh_port=22):
        super(SSHTunnelHTTPAdapter, self).__init__()
        self.ssh_user = ssh_user
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port

    def get_connection(self, url, proxies=None):
        components = urlparse.urlparse(url)
        if ':' in components.netloc:
            remote_host, remote_port = components.netloc.split(':')
            remote_port = int(remote_port)
        else:
            remote_host = components.netloc
            remote_port = 80
        return SSHTunnelHTTPConnectionPool(
            self.ssh_user, self.ssh_host, self.ssh_port,
            remote_host, remote_port)


def main():
    import argparse
    import requests

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', help="remote SSH username")
    parser.add_argument('-H', '--host', required=True, help="remote SSH host")
    parser.add_argument('url', help="URL (as seen from the remote host)")
    args = parser.parse_args()

    ssh_adapter = SSHTunnelHTTPAdapter(ssh_user=args.user, ssh_host=args.host)
    session = requests.Session()
    session.mount('http://', ssh_adapter)
    r = session.get(args.url)
    print(r)
    print(r.text)


if __name__ == '__main__':
    main()
