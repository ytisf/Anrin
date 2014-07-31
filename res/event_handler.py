import pyinotify
import res.logging
import res.blacker
import random
import string

class EventHandler(pyinotify.ProcessEvent):

	def process_IN_CREATE(self, event):
		'''
		This function is what loads when a new file is created under the directory.
		:param event: Event of file creation
		:return:Nothing
		'''
		error_handler = res.logging.Wall_e()								# Setting up error handlers
		blacker = res.blacker.Blacker()										# Blacker Handler
		filename = event.pathname
		error_handler.log_error(0, "Starting to analyse %s" % filename)

		# Open file for read
		file = open(filename, 'rb')
		a = file.read()
		a = a.split('\n')
		for line in a:
			blacker.parse_line(line)

		error_handler.log_error(1, "Detected " + str(len(blacker._all_ips)) + " IPs.")
		error_handler.log_error(1, "Detected " + str(len(blacker._all_macs)) + " MAC addresses.")
		error_handler.log_error(1, "Detected " + str(len(blacker._all_dnss)) + " Domain Names.")

		# Blacken the IPs
		for a in blacker._all_ips:
			blacker.blacken_ip(a)
		error_handler.log_error(1, "Blacked %s IP addresses" % len(blacker._randomized_ips))

		# Blacken the MACs
		for a in blacker._all_macs:
			blacker.blacken_mac(a)
		error_handler.log_error(1, "Blacked %s MAC addresses" % len(blacker._randomized_macs))

		# Blacken DNSs:
		for a in blacker._all_dnss:
			blacker.blacken_domain(a)
		error_handler.log_error(1, "Blacked %s DNS addresses" % len(blacker._randomized_dnss))


		""" Build and save censored file """
		# Open Original File
		data = []
		last_read = open(filename, 'rb')
		black_file_data = last_read.readlines()

		for line in black_file_data:
			data.append(blacker.rec_replace(line))

		# Build black list file name (random 6 charachters)
		blacklist_file_name_base = ""
		for i in range(1, 6, 1):
			blacklist_file_name_base += random.choice(string.letters)

		blacklist_file_name = blacklist_file_name_base + ".censored.txt"

		blackfile_handler = open("./blacked/" + blacklist_file_name, 'wb')

		for line in data:
			blackfile_handler.write(line)

		blackfile_handler.close()


		""" Build and save dictionary file """
		dictionary_filename = blacklist_file_name_base + ".dictionary.txt"
		f = open("./blacked/" + dictionary_filename, 'wb')

		f.write("MACs\n")
		f.write("################################################\n")
		for org_mac, new_mac in blacker._randomized_macs:
			f.write(org_mac + ":" + new_mac + "\n")

		f.write("\n\nIPs\n")
		f.write("################################################\n")
		for org_ip, new_ip in blacker._randomized_ips:
			f.write(org_ip + ":" + new_ip + "\n")

		f.write("\n\nDNSs\n")
		f.write("################################################\n")
		for org_dns, new_dns in blacker._randomized_dnss:
			f.write(org_dns + ":" + new_dns + "\n")

		f.close()
		error_handler.log_error(0, "Wrote file to blacked/" + blacklist_file_name)


	def process_IN_DELETE(self, event):
		print "Removing:", event.pathname