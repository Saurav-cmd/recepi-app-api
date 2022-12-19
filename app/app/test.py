"""
simple test this test doesnt require database

"""

from django.test import SimpleTestCase
from app import calc

class CalculatorTest(SimpleTestCase):
    """Test the calc.py module"""
    def test_add_case(self):
        res = calc.add(5,6)
        self.assertEqual(res,11)

    def test_sub_case(self):
        res = calc.sub(15,10)
        self.assertEqual(res,5)
    