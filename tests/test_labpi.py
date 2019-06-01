"""Unit tests for LabPi"""

import unittest, re, datetime, sys


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

class MainLoopTests(unittest.TestCase):
    def test_main_loop(self):
        pass
