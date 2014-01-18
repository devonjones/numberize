from numberizer import *

class TestNumberizer:
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testComma(self):
		assert numberizer._sanitize("1,123") == "1123"
		assert numberizer._sanitize("1123") == "1123"
		assert numberizer._sanitize("1,123.45") == "1123.45"

	def testNan(self):
		assert numberizer._sanitize("1234.56") == "1234.56"
		try:
			fail = False
			numberizer._sanitize("1a3123.34")
		except ValueError, ve:
			fail = True
		assert fail == True

	def testDecimal(self):
		assert numberizer._decimal("1.1") == "1/10"
		assert numberizer._decimal("1.02") == "02/100"
		assert numberizer._decimal("1.204") == "204/1000"
		assert numberizer._decimal("1.0153") == "0153/10000"
		assert numberizer._decimal("1") == None

	def testHundreds(self):
		assert numberizer._hundreds("1") == "one"
		assert numberizer._hundreds("011") == "eleven"
		try:
			fail = False
			assert numberizer._hundreds("1234") == None
		except ValueError, ve:
			fail = True
		assert fail == True
		assert numberizer._hundreds("123") == "one hundred twenty-three"
		assert numberizer._hundreds("234") == "two hundred thirty-four"
		assert numberizer._hundreds("345") == "three hundred fourty-five"
		assert numberizer._hundreds("456") == "four hundred fifty-six"
		assert numberizer._hundreds("567") == "five hundred sixty-seven"
		assert numberizer._hundreds("678") == "six hundred seventy-eight"
		assert numberizer._hundreds("789") == "seven hundred eighty-nine"
		assert numberizer._hundreds("890") == "eight hundred ninety"
		assert numberizer._hundreds("901") == "nine hundred one"

	def testTens(self):
		assert numberizer._tens("112") == "twelve"
		assert numberizer._tens("12") == "twelve"
		assert numberizer._tens("37") == "thirty-seven"
		assert numberizer._tens("7") == "seven"
		assert numberizer._tens("90") == "ninety"
		assert numberizer._tens("93") == "ninety-three"
		assert numberizer._tens("03") == "three"
		assert numberizer._tens("103") == "three"

	def testNumberToText(self):
		try:
			fail = False
			assert number_to_text("") == None
		except ValueError, ve:
			fail = True
		assert fail == True
		assert number_to_text("3.09") == "Three and 09/100 dollars"
		assert number_to_text("30.1") == "Thirty and 1/10 dollars"
		assert number_to_text("853") == "Eight hundred fifty-three dollars"
		assert number_to_text("1234.56") == "One thousand two hundred thirty-four and 56/100 dollars"
		assert number_to_text("10234.56") == "Ten thousand two hundred thirty-four and 56/100 dollars"
		assert number_to_text("987234.56") == "Nine hundred eighty-seven thousand two hundred thirty-four and 56/100 dollars"
		assert number_to_text("1234567890") == "One billion two hundred thirty-four million five hundred sixty-seven thousand eight hundred ninety dollars"
