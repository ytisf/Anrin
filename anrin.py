#!/usr/bin/python
# coding=utf-8
'''
Anrin will try to black out IP addresses, MAC addresses and domain names from files.
It will do so while keeping the logs flow to allow others to analyze them without
revealing sensitive information.
'''

import sys
import res.event_handler

try:
	import pyinotify
except ImportError, e:
	print ("Error: The module pyinotify is not installed.")
	print ("       Use 'sudo pipt install pyinotify' to install it.")
	print ("       Anrin cannot operate without it. Exiting now.")
	sys.exit(1)

__authors__ = ["Yuval tisf Nativ", "Omree Benari"]

# Setting up globals:
folder_to_watch = './watch'
filename = ""

def banner():
	print ""
	print "  )¯¯,¯\ ° |\¯¯¯\)¯¯\   |\¯¯¯,¯)°  |¯¯¯| |\¯¯¯\)¯¯\   "
	print " /__/'\__\ |/__/\____\° \|__|\__)' |___| |/__/\____\°"
	print "|__ |/\|__| |__|/\|___|  |__|\|__| |___| |__|/\|____| "
	print "'                    '                         ‘            '         "
	print "\t\tby " + __authors__[0] + " & " + __authors__[1]
	print "\t\tA Log Censor Tool"
	print ""
	print "\t Now watching the folder 'watch'"
	print "\t Files which will be put there will be "
	print "\t blackend (hence the name) and saved to 'blacked'."
	print "\t Notice that a dictionary file is also created and"
	print "\t it is possible to decrypt the data with it!"
	print ""


def main():

	banner()

	# Setting up pyinotify handlers
	wm = pyinotify.WatchManager()
	mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE

	# Actually starting to monitor file changes
	handler = res.event_handler.EventHandler()
	notifier = pyinotify.Notifier(wm, handler)
	wdd = wm.add_watch(folder_to_watch, mask, rec=True)

	notifier.loop()


if __name__ == "__main__":
	main()