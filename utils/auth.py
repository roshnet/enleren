
def authorise(uname='', pswd='', creds_dict=dict()):
	'''
	Returns 1 if `uname` maps to `pswd` in `creds_dict` ;
	Returns 0, if `uname` exists but `pswd` does not correspond to it;
	Returns the string 'nouser', if `uname` does not exist in `creds_dict` as a key.
	'''
	try:
		if uname in creds_dict.keys():
			if pswd == creds_dict[uname]:
				return 1
			return 0
		return 'nouser'
	except KeyError:
		return "Sorry, something broke :( . We'll soon fix it."