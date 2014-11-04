

import logging
import glob
import re
import os
import sys
from subprocess import call
from subprocess import check_call

success = True

call(["getmail",])

logging.basicConfig(filename='log.txt',level=logging.DEBUG)
newmails = glob.glob("/home/pi/scanMail/new/*.nodepi")
scandir = "/home/pi/nodescan/"
formats = ["jpg", "JPG", "PNG", "png"]

for mail in newmails:
	# get sender
	try:
		with open(mail, 'r') as f:
  			first_line = f.readline()
  			sender = re.search("<([\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4})>", first_line).group(1)
			logging.debug("Successful parse")
			logging.debug(sender)
	except:
		logging.debug("Error in parsing %s\n" % l)
		success = False
		break

	# get image
	try:
		cmd = "munpack -fq -C /home/pi/nodescan " + mail
		os.system(cmd)
		logging.debug("Succesfull outputting image munpack")
	except:
		logging.debug("Error in outputting image munpack")
		success = False
		break


	images = sum(map(lambda x: glob.glob("/home/pi/nodescan/*."+x), formats), [])
	if len(images) > 0:
		try:
			check_call(["python", scandir + "scan.py", "--image", images[0]])
			logging.debug("Successfully used scan.py")
		except:
			logging.debug("Problem with scan.py")
			success = False
			break

		try:
			# send back the ok message with the file attached
			cmd = "mutt -s 'Voila ton scan !' -i /home/pi/nodescan/ok_msg.txt " + sender +  " -a /home/pi/*.pdf < /dev/null"
			os.system(cmd)
			logging.debug("Successfully send the scaned image")
		except:
			logging.debug("Problem sending mail")
			success = False
			break
	else:
		# there is no image to process
		# send back the "no image attached" error message
		cmd = "mutt -s 'Euh, elle est ou ton image ?' -i /home/pi/nodescan/error_empty_msg.txt " + sender +  " < /dev/null"
		os.system(cmd)
		logging.debug("no image in mail")
		success = False
		break

	# try:
	# clean
	os.remove(mail)
	cmd = "rm -f " + map(lambda x: "/home/pi/nodescan/*."+x, formats +["pdf, desc"]).join(" ")
	os.system(cmd)
	os.system("rm -f /home/pi/scanMail/sent/cur/*")
	logging.debug("Successfully cleaned files")
	# except:
	# 	logging.debug("Problem in cleaning files")
	# 	success = False
	# 	break


	if success != True:
		# the image was not correctly processed
		# send back the "file not processed" error message
		cmd = "mutt -s 'Probleme de scan...' -i /home/pi/nodescan/log.txt " + "bxnode.scan@gmail.com" +  " < /dev/null"
		os.system(cmd)
		cmd = "mutt -s 'Erreur de scan' -i /home/pi/nodescan/error_process_msg.txt " + sender +  " < /dev/null"
		os.system(cmd)
		# clean
		try: 
			os.remove(mail)
			os.system("rm -f /home/pi/nodescan/*.JPG.* /home/pi/nodescan/*.jpg.* /home/pi/nodescan/*.desc* /home/pi/*.pdf.*")
			os.system("rm -f /home/pi/scanMail/sent/cur/*")
		except:
			print "error in cleaning"
			logging.debug("Problem in cleaning files with errors")


