

import glob
import re
import os
import sys
from subprocess import call
from subprocess import check_call

logText = ""
success = True

call(["getmail",])

newmails = glob.glob("/home/pi/scanMail/new/*.nodepi")
scandir = "/home/pi/nodescan/"

for mail in newmails:
	# get sender
	try:
		with open(mail, 'r') as f:
  			first_line = f.readline()
  			sender = re.search("<([\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4})>", first_line).group(1)
			logText += "Successful parse:\n"
			logText += sender + "/n"
	except:
		logText += "Error in parsing %s\n" % mail
		success = False
		break

	# get image
	try:
		cmd = "munpack -C /home/pi/nodescan " + mail
		os.system(cmd)
		logText += "Succesfull outputting image munpack \n"
	except:
		logText += "Error in outputting image munpack \n"
		success = False
		break


	images = glob.glob("/home/pi/nodescan/*.jpg") + glob.glob("/home/pi/nodescan/*.JPG")
	if len(images) > 0:
		try:
			check_call(["python", scandir + "scan.py", "--image", images[0]])
			logText += "Successfully used scan.py \n"
		except:
			logText += "Problem with scan.py \n"
			success = False
			break

		try:
			# send back the ok message with the file attached
			cmd = "mutt -s 'Voila ton scan !' -i /home/pi/nodescan/ok_msg.txt " + sender +  " -a /home/pi/*.pdf < /dev/null"
			os.system(cmd)
			logText += "Successfully send the scaned image \n"
		except:
			logText += "Problem sending mail \n"
			success = False
			break
	else:
		# there is no image to process
		# send back the "no image attached" error message
		cmd = "mutt -s 'Euh, elle est ou ton image ?' -i /home/pi/nodescan/error_empty_msg.txt " + sender +  " < /dev/null"
		os.system(cmd)
		logText += "no image in mail \n"
		success = False
		break

	try:
		# clean
		os.remove(mail)
		os.system("rm -f /home/pi/nodescan/*.JPG /home/pi/nodescan/*.jpg /home/pi/nodescan/*.desc /home/pi/*.pdf")
		os.system("rm -f /home/pi/scanMail/sent/cur/*")
		logText += "Successfully cleaned files \n"
	except:
		logText += "Problem in cleaning files \n"
		success = False
		break


	if success != True:
		# the image was not correctly processed
		# send back the "file not processed" error message
		tmp = open("/home/pi/nodescan/tmp.txt", "w")
		tmp.write(logText)
		tmp.close()
		cmd = "mutt -s 'Probleme de scan...' -i /home/pi/nodescan/tmp.txt " + "bxnode.scan@gmail.com" +  " < /dev/null"
		os.system(cmd)
		cmd = "mutt -s 'Erreur de scan' -i /home/pi/nodescan/error_process_msg.txt " + sender +  " < /dev/null"
		os.system(cmd)
		# clean
		try: 
			os.remove(mail)
			os.system("rm -f /home/pi/nodescan/*.JPG /home/pi/nodescan/*.jpg /home/pi/nodescan/*.desc /home/pi/*.pdf")
			os.system("rm -f /home/pi/scanMail/sent/cur/*")
		except:
			print "error in cleaning"
			logText += "Problem in cleaning files with errors \n"


logs = open("log.txt", "a")
logs.write(logText)
logs.close()
