

import glob
import re
import os
import sys
from subprocess import call
from subprocess import check_call


call(["getmail",])

newmails = glob.glob("/home/pi/scanMail/new/*.nodepi")
scandir = "~/nodescan/"

for mail in newmails:
	try:
		# get sender
		with open(mail, 'r') as f:
  			first_line = f.readline()
  			sender = re.search("<([\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4})>", first_line).group(1)
		# get image
		os.system("cd ")
		cmd = "munpack -C ~/nodescan " + mail
		os.system(cmd)
		images = glob.glob("~/nodescan/*.jpg") + glob.glob("~/nodescan/*.JPG")
		# if image then process
		if len(images) > 0:
			returncode = check_call(["python", scandir + "scan.py", "--image", images[0]])
			if returncode == 0:
				# send back the ok message with the file attached
				cmd = "mutt -s 'Voila ton scan !' -i ~/nodescan/ok_msg.txt " + sender +  " -a *.pdf < /dev/null"
				os.system(cmd)
			else:
				# the image was not correctly processed
				# send back the "file not processed" error message
				cmd = "mutt -s 'Elle est moche ta photo' -i ~/nodescan/error_process_msg.txt " + sender +  " < /dev/null"
				os.system(cmd)			
		else:
			# there is no image to process
			# send back the "no image attached" error message
			cmd = "mutt -s 'Euh, elle est ou ton image ?' -i ~/nodescan/error_empty_msg.txt " + sender +  " < /dev/null"
			os.system(cmd)
		

		# clean
		os.remove(mail)
		os.system("rm -f ~/nodescan/*.JPG ~/nodescan/*.jpg ~/nodescan/*.desc ~/nodescan/*.pdf")
		os.system("rm -f ~/scanMail/sent/cur/*")
		#call(["rm part*"])
		#call(["rm "+mail,])

	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		print "pb with %s" % mail
