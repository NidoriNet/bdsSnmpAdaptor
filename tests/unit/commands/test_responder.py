# -*- coding: utf-8 -*-
#
# This file is part of bdsSnmpAdaptor software.
#
# Copyright (C) 2017-2019, RtBrick Inc
# License: BSD License 2.0
#
import asyncio
import io
import sys
import unittest
from unittest import mock

from bdssnmpadaptor.commands import responder


class SnmpFrontEndTestCase(unittest.TestCase):

    CONFIG = """
bdsSnmpAdapter:
  loggingLevel: debug
  stateDir: /var/run/bds-snmp-responder
  responder:
    listeningIP: 0.0.0.0  # SNMP command responder listens on this address
    listeningPort: 11161  # SNMP command responder listens on this port
    engineId: 80:00:C3:8A:04:73:79:73:4e:61:6d:65:31:32:33
    versions:  # SNMP versions map, choices=['1', '2c', '3']
      1:  # map of configuration maps
        manager-A:  # SNMP security name
          community: public
      2c:  # map of configuration maps
        manager-B:  # SNMP security name
          community: public
      3:
        usmUsers:  # map of USM users and their configuration
          user1:  # descriptive SNMP security name
            user: testUser1  # USM user name
            authKey: authkey123
            authProtocol: md5  # md5, sha224, sha256, sha384, sha512, none
          user2:  # descriptive SNMP security name
            user: testUser2  # USM user name
            authKey: authkey123
            authProtocol: md5  # md5, sha224, sha256, sha384, sha512, none
            privKey: privkey123
            privProtocol: des  # des, 3des, aes128, aes192, aes192blmt, aes256, aes256blmt, none
"""

    def setUp(self):
        self.my_loop = asyncio.get_event_loop()
        self.addCleanup(self.my_loop.close)

        super(SnmpFrontEndTestCase, self).setUp()

    @mock.patch('bdssnmpadaptor.commands.responder.snmp_config', autospec=True)
    @mock.patch('bdssnmpadaptor.commands.responder.BdsAccess', autospec=True)
    def test___init__(self, mock_access, mock_snmp_config):

        with mock.patch(
                'bdssnmpadaptor.config.open',
                side_effect=[io.StringIO(self.CONFIG),
                             io.StringIO(self.CONFIG),
                             io.StringIO(self.CONFIG)]):
            responder.SnmpFrontEnd({'config': '/file'})

        mock_access.assert_called_once_with(mock.ANY)
        mock_oiddb = mock_access.return_value.getOidDb
        mock_oiddb.assert_called_once_with()

        mock_snmpEngine = mock_snmp_config.getSnmpEngine.return_value

        mock_snmp_config.getSnmpEngine.assert_called_once_with(
            engineId=mock.ANY)
        mock_snmp_config.setSnmpTransport.assert_called_once_with(
            mock_snmpEngine, ('0.0.0.0', 11161))

        mock_setCommunity_calls = [
            mock.call(mock_snmpEngine, 'manager-A', 'public', version='1'),
            mock.call(mock_snmpEngine, 'manager-B', 'public', version='2c')
        ]
        mock_snmp_config.setCommunity.assert_has_calls(
            mock_setCommunity_calls)

        mock_snmp_config.setMibController.assert_called_once_with(
            mock_snmpEngine, mock.ANY)


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
