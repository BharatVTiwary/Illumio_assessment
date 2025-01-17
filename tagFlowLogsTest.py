import unittest
import unittest.mock
from unittest.mock import mock_open
import StringIO

from tagFlowLogs import (
    initializeProtocolLookup, getLookup, matchFlogLog, writeTagCount, writePortProtocolCount,
    PROTOCOL_LOOKUP, PROTOCOL_FILE_PATH
)

class TagFlowLogsTest(unittest.TestCase):
    def setUp(self):
        PROTOCOL_LOOKUP.clear()
        PROTOCOL_FILE_PATH="testpath"
        
    @unittest.mock.patch('builtins.open', new_callable=mock_open, read_data='Decimal,Keyword\n8080,http\n8043,https')
    def test_initializeProtocolLookup_success(self, mockFIle):
        initializeProtocolLookup()
        self.assertEqual(PROTOCOL_LOOKUP, {'8080': 'http', '8043': 'https'})

    @unittest.mock.patch('builtins.open', new_callable=mock_open, read_data='dstport,protocol,tag\n25,tcp,sv_P1')
    def test_getLookup_success(self, mockFIle):
        actual = getLookup('lookupFile.txt')
        self.assertEqual(actual, {('25', 'tcp'): 'sv_P1'})

    @unittest.mock.patch('builtins.open', new_callable=mock_open, read_data='25 6')
    def test_matchFlogLog_customeIndexes_success(self, mockFIle):
        PROTOCOL_LOOKUP.update({'6': 'tcp', '8043': 'https'})
        lookupDict = {('25', 'tcp'): 'sv_P1'}
        tagActual, portProtocolActual = matchFlogLog('inFile.txt', lookupDict, 0, 1)
        self.assertEqual(tagActual, {'sv_P1': 1})
        self.assertEqual(portProtocolActual, {('25', 'tcp'): 1})

    @unittest.mock.patch('builtins.open', new_callable=mock_open, read_data='v2 0 0 0 0 0 25 6 0 0 0 0 0 0')
    def test_matchFlogLog_defaultIndexes_success(self, mockFIle):
        PROTOCOL_LOOKUP.update({'6': 'tcp', '8043': 'https'})
        lookupDict = {('25', 'tcp'): 'sv_P1'}
        tagActual, portProtocolActual = matchFlogLog('inFile.txt', lookupDict)
        self.assertEqual(tagActual, {'sv_P1': 1})        
        self.assertEqual(portProtocolActual, {('25', 'tcp'): 1})

    @unittest.mock.patch('builtins.open', new_callable=mock_open, read_data='v2 0 0 0 0 0 25 6 0 0 0 0 0 0')
    def test_matchFlogLog_defaultIndexes_success(self, mockFIle):
        PROTOCOL_LOOKUP.update({'6': 'tcp', '8043': 'https'})
        lookupDict = {('25', 'tcp'): 'sv_P1'}
        tagActual, portProtocolActual = matchFlogLog('inFile.txt', lookupDict)
        self.assertEqual(tagActual, {'sv_P1': 1})        
        self.assertEqual(portProtocolActual, {('25', 'tcp'): 1})

if __name__ == '__main__':
    unittest.main()