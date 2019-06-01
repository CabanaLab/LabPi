"""Unit tests for LabPi"""

import unittest
import re
import datetime
import sys
import configparser


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


class MainLoopTests(unittest.TestCase):
    def test_main_loop(self):
        pass
