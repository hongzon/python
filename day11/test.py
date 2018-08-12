from io import StringIO
str = '34jdfh'
def str1(str):
	return str[::-1]
def str2(str):
	if len(str) <= 1:
		return str
	return  str2(str[1:]) + str[0:1]
def str3(str):
	return ''.join([str[index] for index in range(len(str)-1, -1, -1)])
def str4(str):
	rstr = StringIO()
	for index in range(len(str)-1, -1, -1):
		rstr.write(str[index])
	return rstr.getvalue()


print(str1(str))
print(str2(str))
print(str3(str))
print(str4(str))
print()
