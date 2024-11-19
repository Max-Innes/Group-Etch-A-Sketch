# You should not modify or submit this file

import unittest
from servo_translator import translate

class TestServoTranslator(unittest.TestCase):
	def setUp(self):
		self._MIN = 1638
		self._MAX = 8192
			
	def test_bounds(self):
		"""Test that the output is within the bounds of the servo"""
		for i in range(-20, 200, 1):
			self.assertLessEqual(translate(i), self._MAX,
						"Output is too large when input is " + str(i) + " degrees")
			self.assertGreaterEqual(translate(i), self._MIN,
						"Output is too small when input is " + str(i) + " degrees")
	
	def test_start(self):
		"""Test that the output is correct when input is 0 degrees"""
		self.assertAlmostEqual(translate(0), self._MIN, delta=1,
						msg="Output is not correct when input is 0 degrees")
	
	def test_middle(self):
		"""Test that the output is correct when input is 90 degrees"""
		self.assertAlmostEqual(translate(90), 4915, delta=1,
						msg="Output is not correct when input is 90 degrees")
		
	def test_end(self):
		"""Test that the output is correct when input is 180 degrees"""
		self.assertAlmostEqual(translate(180), self._MAX, delta=1,
						msg="Output is not correct when input is 180 degrees")

if __name__ == '__main__':
	unittest.main()
