forbidden = [";", "'"]

def sanitize_search(s):
	new_s = {}
	for key in s:
		tempKey = key.replace("'", "")
		tempKey = tempKey.replace(";", "")
		tempValue = s[key].replace("'", "")
		tempValue = tempValue.replace(";", "")
		new_s[tempKey] = tempValue
	return new_s

def sanitize_input(s, forbidden):
	if any(word in s for word in forbidden):
		#need to figure out best way to continue if SQL is found
		print("No SQL Please")
