from collective.clamav.interfaces import IAVScanner
from io import BytesIO
from zope.interface import implementer

import clamd


class ScanError(Exception):
    """Generic exception for AV checks."""

    def __init__(self, message):
        super().__init__(message)


def _make_clamd(type, **kwargs):
    timeout = kwargs.get("timeout", 10.0)
    if type == "socket":
        socketpath = kwargs.get("socketpath", "/var/run/clamd")
        return clamd.ClamdUnixSocket(path=socketpath, timeout=timeout)
    elif type == "net":
        host = kwargs.get("host", "localhost")
        port = kwargs.get("port", 3310)
        return clamd.ClamdNetworkSocket(host=host, port=port, timeout=timeout)
    else:
        raise ScanError("Invalid call")


@implementer(IAVScanner)
class ClamavScanner:
    """ """

    def ping(self, type, **kwargs):
        if not _make_clamd(type, **kwargs).ping() == "PONG":
            raise ScanError("Could not ping clamd server")
        return True

    def scanBuffer(self, buffer, type, **kwargs):
        """Scans a buffer for viruses"""

        timeout = kwargs.get("timeout", 120.0)
        kwargs_copy = dict(kwargs)
        kwargs_copy.update(timeout=timeout)
        cd = _make_clamd(type, **kwargs_copy)
        status = cd.instream(BytesIO(buffer))

        if status["stream"][0] == "FOUND":
            return status["stream"][1]
        if status["stream"][0] == "ERROR":
            raise ScanError(status["stream"][1])
