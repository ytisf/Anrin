import re
import random
import string


class Blacker():

	def __init__(self):
		self._all_ips = []
		self._all_macs = []
		self._all_dnss = []
		self._randomized_macs = []
		self._randomized_ips = []
		self._randomized_dnss = []
		self._ip_a = []
		self._ip_b = []
		self._ip_c = []
		self._ip_d = []

	def parse_line(self, line):

		regex_ip = "(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
		regex_mac = "([a-fA-F0-9]{2}[:-][a-fA-F0-9]{2}[:-][a-fA-F0-9]{2}[:-][a-fA-F0-9]{2}[:-][a-fA-F0-9]{2}[:-][a-fA-F0-9]{2})"
		regex_dns = "([a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,6})"

		# Search for IPs
		match = re.search(regex_ip, line)
		if match:
			self._all_ips.append(match.group())
			line = line.replace(match.group(), "")
			self.parse_line(line)

		else:
			# Search for MACs
			match = re.search(regex_mac, line)
			if match:
				self._all_macs.append(match.group())
				line = line.replace(match.group(), "")
				self.parse_line(line)

			else:
				# Search for Domains
				match = re.search(regex_dns, line)
				if match:
					self._all_dnss.append(match.group())
					line = line.replace(match.group(), "")
					self.parse_line(line)

	def blacken_ip(self, ip):
		'''
		This function will take an IP address, check if it has been randomized before,
		if not, it will split to subnets and try to keep the logic sane.
		:param ip: This current IP to process.
		:return: To a global array
		'''
		found = 0
		new_ip = []
		previousIP = ip
		# Split IP:
		ip = str(ip)
		ip = ip.split('.')

		# Check all IP.
		for curr_ip in self._randomized_ips:
			if previousIP == curr_ip[0]:
				return 0

		# Check first segment
		for a in self._ip_a:
			#print self._ip_a
			if a[0] == ip[0]:
				ip[0] = a[1]
				new_ip.append(ip[0])
				found = 1

		if found == 0:
			new_a = random.randrange(1, 253, 1)
			new_ip.append(new_a)
			self._ip_a.append([ip[0], new_a])
		found = 0


		# Check 2nd segment
		for a in self._ip_b:
			if a[0] == ip[1]:
				ip[1] = a[1]
				new_ip.append(ip[1])
				found = 1

		if found == 0:
			new_a = random.randrange(1, 253, 1)
			new_ip.append(new_a)
			self._ip_b.append([ip[1], new_a])
		found = 0

		# Check 3rd segment
		for a in self._ip_c:
			if a[0] == ip[2]:
				ip[2] = a[1]
				new_ip.append(ip[2])
				found = 1

		if found == 0:
			new_a = random.randrange(1, 253, 1)
			new_ip.append(new_a)
			self._ip_c.append([ip[2], new_a])
		found = 0

		# Check 4th segment
		for a in self._ip_d:
			if a[0] == ip[3]:
				ip[3] = a[1]
				new_ip.append(ip[3])
				found = 1

		if found == 0:
			new_a = random.randrange(1, 253, 1)
			new_ip.append(new_a)
			self._ip_d.append([ip[3], new_a])

		new_ip = str(new_ip[0]) + "." + str(new_ip[1]) + "." + str(new_ip[2]) + "." + str(new_ip[3])
		self._randomized_ips.append([previousIP, new_ip])

	def blacken_mac(self, mac):
		'''
		This function will go over a MAC address given.
		It will then check if the mac have been seen before and if so it will exit.
		If the MAC address was not seen it will create a random MAC and store it
		in the self._randomized_macs var for later use.
		:param mac: The Mac address to change
		:return:
		'''
		found = 0
		new_mac = ""

		# search if mac alread has translattion
		for item in self._randomized_macs:
			if mac == item[0]:
				found = 1

		# if not replace with new random mac
		if found == 0:
			macs = [ 'z', 'x', 'y', 'w', 'h', 'g', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
			for a in range(1, 6, 1):
				string = ""
				b = random.sample(macs, 2)
				for char in b:
					string += char
				new_mac += string + ":"

			a = random.sample(macs, 2)
			string = ""
			for char in a:
				string += char
			new_mac += string

			# store mac in parent store
			self._randomized_macs.append([mac, new_mac])

	def blacken_domain(self, domain):
		'''
		This function will "encrypt" the domain names. It does not maintaine logic.
		:param domain: The Domain name to hide
		:return: global array
		'''
		found = 0

		# Search if DNS is in domain list
		for item in self._randomized_dnss:
			if domain == item[0]:
				found = 1

		if found == 0:
			def getServer():
				ServerName = ''
				loop = random.randint(5, 5)
				for a in range(loop):
					ServerName += getLetter()
				ServerName += '.'
				loop = random.randint(4, 6)
				for a in range(loop):
					ServerName += getLetter()
				ServerName += '.'
				loop = random.randint(2, 3)
				for a in range(loop):
					ServerName += getLetter()

				return ServerName

			def getLetter():
				letter = 59
				while True:
					if (letter in range(58, 65)) or (letter in range(91, 97)) or (letter > 122):
						letter = random.randint(48, 122)
					else:
						break
				return chr(letter)

			new_domain = getServer()
			self._randomized_dnss.append([domain, new_domain])

	def rec_replace(self, original_data):
		'''
		:param original_data: A line to parse
		:return:
		'''

		# Replace all MACS
		for mac in self._randomized_macs:
			if original_data.find(mac[0]) != -1:
				original_data = original_data.replace(mac[0], mac[1])
				continue

		# Replace All IPs
		for ip in self._randomized_ips:
			if original_data.find(ip[0]) != -1:
				original_data = original_data.replace(ip[0], ip[1])
				continue

		# Replace All DNSs
		for dns in self._randomized_dnss:
			if original_data.find(dns[0]) != -1:
				original_data = original_data.replace(dns[0], dns[1])
				continue

		return original_data

