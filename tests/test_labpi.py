"""Unit tests for LabPi"""

import unittest
from unittest import mock
import re
import datetime
import sys
import configparser
from contextlib import contextmanager


from labpi import empty


class InputTests(unittest.TestCase):
    def test_barcode_validation(self):
        """Incoming strings should pass validation"""
        test_data = ( ('UL9999', True),
                      ('12345', True),
                      ('maliciousdata', False)
                      )
        for exp_in, exp_out in test_data:
            result = empty.validate(exp_in)
            self.assertEqual(result, exp_out)


class ConfigTest(unittest.TestCase):
    """Tests to determine if the configuration is loaded."""
    def test_load_config(self):
        config = empty.load_config()
        # with open('example.conf', 'w') as configfile:
        #     config.write(configfile)
        self.assertIsInstance(config, configparser.ConfigParser)
        self.assertEqual(len(config.sections()), 1)
        # Check default configuration
        self.assertEqual(config['server']['username'], '')
        self.assertEqual(config['server']['password'], '')
        self.assertEqual(config['server']['base_url'], 'http://example.com/container/{id}')


class InputLoopTest(unittest.TestCase):
    """Tests for the main input loop."""
    @contextmanager
    def patch_input(self, new_str):
        with mock.patch('builtins.input', lambda *args: new_str):
            yield
    
    def test_valid_input(self):
        mocklcd = mock.MagicMock()
        mockserver = mock.MagicMock()
        mockserver.mark_as_empty.return_value = 200
        with self.patch_input('1568'):
            empty.process_input(lcd=mocklcd, server=mockserver)
        # Check that the right server call was made
        mockserver.mark_as_empty.assert_called_with('1568')
        # Check that the LCD was updated appropriately
        mocklcd.print_message.assert_any_call(
            'Container 1568:\nSending...',
            mocklcd.C_WARNING,
        )
        mocklcd.print_message.assert_any_call(
            'Container 1568:\nMarked as Empty!',
            mocklcd.C_SUCCESS,
        )
        # Check that it works when padded with zeros
        with self.patch_input('001568'):
            empty.process_input(lcd=mocklcd, server=mockserver)
        # Check that the right server call was made
        mockserver.mark_as_empty.assert_called_with('1568')
        # Check that 404 status codes update the LCD
        mockserver.mark_as_empty.return_value = 404
        mocklcd.print_message.reset_mock()
        with self.patch_input('1568'):
            empty.process_input(lcd=mocklcd, server=mockserver)
        mocklcd.print_message.assert_any_call(
            "Container 1568:\nNot Found!",
            mocklcd.C_ERROR)
        # Check that non-404 failure status codes update the LCD
        mockserver.mark_as_empty.return_value = 500
        mocklcd.print_message.reset_mock()
        with self.patch_input('1568'):
            empty.process_input(lcd=mocklcd, server=mockserver)
        mocklcd.print_message.assert_any_call(
            "Container 1568:\nError! (500)",
            mocklcd.C_ERROR)        
    
    def test_nonsense_input(self):
        pass


class MainLoopTests(unittest.TestCase):
    def test_main_loop(self):
        pass
