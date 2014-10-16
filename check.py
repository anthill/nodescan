

import glob
import re
import os
import sys
from subprocess import call
from subprocess import check_call


call(["getmail",])

newmails = glob.glob("/home/pi/scanMail/new/*.nodepi")
scandir = "/home/pi/nodescan/"

for mail in newmails:
	try:
		# get sender
		with open(mail, 'r') as f:
  			first_line = f.readline()
  			sender = re.search("<([\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4})>", first_line).group(1)
		# get image
		cmd = "munpack -C /home/pi/nodescan " + mail
		os.system(cmd)
		images = glob.glob("/home/pi/nodescan/*.jpg") + glob.glob("/home/pi/nodescan/*.JPG")
		# if image then process
		if len(images) > 0:
			check_call(["python", scandir + "scan.py", "--image", images[0]])
			# send back the ok message with the file attached
			cmd = "mutt -s 'Voila ton scan !' -i /home/pi/nodescan/ok_msg.txt " + sender +  " -a /home/pi/*.pdf < /dev/null"
			os.system(cmd)
						
		else:
			# there is no image to process
			# send back the "no image attached" error message
			cmd = "mutt -s 'Euh, elle est ou ton image ?' -i /home/pi/nodescan/error_empty_msg.txt " + sender +  " < /dev/null"
			os.system(cmd)
		

		# clean
		os.remove(mail)
		os.system("rm -f /home/pi/nodescan/*.JPG /home/pi/nodescan/*.jpg /home/pi/nodescan/*.desc /home/pi/nodescan/*.pdf")
		os.system("rm -f /home/pi/scanMail/sent/cur/*")
		#call(["rm part*"])
		#call(["rm "+mail,])

	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		print "pb with %s" % mail

		# the image was not correctly processed
		# send back the "file not processed" error message
		cmd = "mutt -s 'Elle est moche ta photo' -i /home/pi/nodescan/error_process_msg.txt " + sender +  " < /dev/null"
		os.system(cmd)
		# clean
		os.remove(mail)
		os.system("rm -f /home/pi/nodescan/*.JPG /home/pi/nodescan/*.jpg /home/pi/nodescan/*.desc /home/pi/nodescan/*.pdf")
		os.system("rm -f /home/pi/scanMail/sent/cur/*")
