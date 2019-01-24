def fermat(n):
	if n == 2:
		return True
	if not n & 1:
		return False
	return pow(2, n-1, n) == 1
