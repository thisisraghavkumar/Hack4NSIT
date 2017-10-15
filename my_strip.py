def my_strip(str,pat):
	strn = str.lstrip(pat)
	low = strn.split(",")
	rlow=[]
	for word in low:
		rlow.append(word.lstrip())
	return rlow
