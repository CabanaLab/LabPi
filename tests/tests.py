"""Unit tests for LabPi"""

import unittest, re, datetime, sys

sys.path.append("..")
import empty.validate, empty.send_notification, empty.check_if_empty

class input(unittest.TestCase):
    def validate_incoming_string(self):
        """Incoming strings should pass validation"""
        test_data = ( ('UL9999', True),
                      ('12345', True),
                      ('maliciousdata', False)
                      )

        for exp_in, exp_out in self.test_data:
            result = empty.validate(exp_in)
            self.assertEqual(result, exp_out)

# unittest.mock
# class notification(unittest.TestCase):
#     def 
