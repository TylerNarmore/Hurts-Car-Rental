forbidden = [";", "'"]

def sanitize_search(s):
	new_s = s.lower()
	new_s = new_s.replace("'", "")
	new_s = new_s.replace(";", "")
	return new_s

def sanitize_input(s, forbidden):
	if any(word in s for word in forbidden):
		#need to figure out best way to continue if SQL is found
		print("No SQL Please")
