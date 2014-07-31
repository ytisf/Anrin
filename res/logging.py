import sys


class Wall_e():
	def __init__(self):
		pass

	def log_error(self, code, data):
		'''
		:param code: Type of error as int
		:param data: Error Message
		:return: Nothing
		'''

		# 0 = info, 1=warning, 2=error, 3=critical

		if code == 0:
			print ("[+]\t%s" % data)

		elif code == 1:
			print("[-] %s" % data)

		elif code == 2:
			print("[!] %s" % data)

		elif code == 3:
			sys.exit("[X] " + data)

		# If you're here you are batshit crazy...
		else:
			print("Go learn your error handler!!!!")
			sys.exit(1)

		return 0
