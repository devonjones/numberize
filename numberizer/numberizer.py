import math

WORDS = {
	0: "zero",
	1: "one",
	2: "two",
	3: "three",
	4: "four",
	5: "five",
	6: "six",
	7: "seven",
	8: "eight",
	9: "nine",
	10: "ten",
	11: "eleven",
	12: "twelve",
	13: "thirteen",
	14: "fourteen",
	15: "fifteen",
	16: "sixteen",
	17: "seventeen",
	18: "eighteen",
	19: "nineteen",
	20: "twenty",
	30: "thirty",
	40: "fourty",
	50: "fifty",
	60: "sixty",
	70: "seventy",
	80: "eighty",
	90: "ninety"
}

MAGNITUDE = {
	1: "thousand",
	2: "million",
	3: "billion",
	4: "trillion",
	5: "quadrillion"
}

def _sanitize(num):
	"""
	clears commas, checks for zero length strings and checks to ensure
	the nember can be converted to a float.

	Raises an exception if any of these conditions fail.
	"""
	if num.find(",") > -1:
		num = num.replace(",", "")
	if len(num) == 0:
		raise ValueError("Number string empty")
	float(num)
	return num

def _hundreds(num):
	"""
	Converts three digit numbers to the corresponding words

	Raises an exception if called with a number of more then 3 digits
	"""
	retarr = []
	if len(num) > 3:
		raise ValueError(
			"_hundreds called with a number greater then 999: %s" % num)
	if len(num) == 3:
		val = int(num[0])
		if val > 0:
			retarr.append("%s hundred" % WORDS[val])
	retarr.append(_tens(num))
	if len(retarr) > 0:
		return " ".join([s for s in retarr if s])

def _tens(num):
	"""
	Converts the last 2 digit of a number string into the corresponding words
	representing that string.
	"""
	if len(num) > 2:
		val = int(num[-2:])
	else:
		val = int(num)
	if val > 0:
		if val in WORDS:
			return WORDS[val]
		else:
			return "%s-%s" % (WORDS[val-val%10], WORDS[val%10])

def _decimal(num):
	"""
	Converts the part of the number after the decimal place to n/10 fractions

	Since Dollars can be tracked in values below a penny, and regularly are by
	financial institutions, I decided to allow arbitrary precision on this.
	"""
	if num.find(".") > -1:
		decimal = num.split(".")[1]
		return "%s/%s" % (decimal, int(math.pow(10, len(decimal))))

def number_to_text(num):
	"""
	Converts a number represented by a string to the text version of that
	number, in dollars.
	"""
	num = _sanitize(num)
	numarr = []
	dec = _decimal(num)
	if dec:
		numarr.append(dec)
		numarr.append("and")
		num = num.split(".")[0]
	remainder = True
	magnitude = 0
	while remainder:
		if magnitude > 5:
			raise ValueError("number_to_text can only handle numbers under 1 Quintillion")
		if magnitude > 0:
			numarr.append(MAGNITUDE[magnitude])
		if len(num) <= 3:
			numarr.append(_hundreds(num))
			remainder = False
		else:
			numarr.append(_hundreds(num[-3:]))
			num = num[:-3]
			magnitude += 1
	numarr.reverse()
	numarr.append("dollars")
	return " ".join(numarr).capitalize()
