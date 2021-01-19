# -*- coding: utf-8 -*-
from collective.clamav.interfaces import IAVScanner
from collective.clamav.scanner import ScanError
from collective.clamav.testing import AV_INTEGRATION_TESTING
from collective.clamav.testing import EICAR
from zope.component import getUtility

import unittest


class TestScanner(unittest.TestCase):
    """Integration test for clamav. This testcase communicates with
    clamd, so you need it installed. Provide the -a2 flag to testrunner
    to include it.
    """

    layer = AV_INTEGRATION_TESTING

    level = 2  # Only run on level 2...

    def setUp(self):
        self.scanner = getUtility(IAVScanner)

    def test_net_ping(self):
        """ Test ping with a network connection on localhost 3310
        """

        self.assertEqual(self.scanner.ping(type='net'), True)

        # Test timeout
        self.assertRaises(
            ScanError,
            self.scanner.ping,
            {'type': 'net', 'timeout': 1.0e-16})

    def test_unix_socket_ping(self):
        """ Test ping with a socket connection on /tmp/clamd.socket
        which is default on macports clamd. If you use linux just change
        the socketpath
        """

        self.assertEqual(
            self.scanner.ping(type='socket', socketpath='/tmp/clamd.socket'),
            True)

        # Test timeout
        self.assertRaises(
            ScanError,
            self.scanner.ping,
            {'type': 'socket',
             'socketpath': '/tmp/clamd.socket',
             'timeout': 1.0e-16})

    def test_net_scanBuffer(self):
        """ Try a virus through the net.
        """

        self.assertEqual(
            self.scanner.scanBuffer(EICAR, type='net'),
            'Win.Test.EICAR_HDB-1')

        # And a normal file...
        self.assertEqual(
            self.scanner.scanBuffer('Not a virus', type='net'),
            None)

        # Test timeout
        self.assertRaises(
            ScanError,
            self.scanner.scanBuffer,
            ('Not a virus', ),
            {'type': 'net', 'timeout': 1.0e-16})

    def test_unix_socket_scanBuffer(self):
        """ Try a virus through a unix socket.
        """

        self.assertEqual(
            self.scanner.scanBuffer(
                EICAR, type='socket',
                socketpath='/tmp/clamd.socket'),
            'Win.Test.EICAR_HDB-1')

        # And a normal file...
        self.assertEqual(
            self.scanner.scanBuffer(
                'Not a virus', type='socket',
                socketpath='/tmp/clamd.socket',
            ), None)

        # Test timeout
        self.assertRaises(
            ScanError,
            self.scanner.scanBuffer,
            ('Not a virus', ),
            {'type': 'socket',
             'socketpath': '/tmp/clamd.socket',
             'timeout': 1.0e-16})
