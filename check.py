

import glob
import re
import os
from subprocess import call


call(["getmail",])

newmails = glob.glob("/home/pi/scanMail/new/*.nodepi")

for mail in newmails:
	try:
		# get sender
		with open(mail, 'r') as f:
  			first_line = f.readline()
  			sender = re.search("<([\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4})>", first_line).group(1)
		# get image
		cmd = "munpack " + mail
		os.system(cmd)
		images = glob.glob("*.jpg") + glob.glob("*.JPG") + glob.glob("*.png") + glob.glob("*.PNG")
		# if image then process
		if len(images) > 0:
			cmd = "python scan.py --image " + images[0]
			os.system(cmd)
			# send back
			cmd = "mutt -s 'Your scanned image' -i message_ok.txt " + sender +  " -a *.pdf < /dev/null"
			os.system(cmd)
		else:
			# send back an error mail
			cmd = "mutt -s 'No image to scan' -i message_error.txt " + sender +  " < /dev/null"
			os.system(cmd)
		

		# clean
		call(["mv ~/scanMail/new/*.nodepi ~/scanMail/cur/"])
		call(["rm -f *.jpg *.JPG *.png *.PNG *.desc *.pdf",])
		#call(["rm part*"])
		#call(["rm "+mail,])

	except:
		print "pb with %s" % mail
