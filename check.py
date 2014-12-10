
import os
import re
import json
import smtplib, imaplib
import email
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from scanner import core


login = json.loads(open("/home/pi/nodescan/login.json","r").read())

# get unseen mails
mailer = imaplib.IMAP4_SSL("imap." + login["host"], 993)
mailer.login(login["user"], login["password"])
mailer.select('INBOX')
result, data = mailer.search(None, "(UNSEEN)")
uids = data[0].split()
newmails = [mailer.fetch(uids[i], "(RFC822)")[1][0][1] for i in range(len(uids))]
print "got %s new mails" % str(len(newmails))

for mail in newmails:
    # parse mail and content
    msg = email.message_from_string(mail)
    sender = re.search("<([\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4})>", msg["From"]).group(1)
    try:
        subject = msg["Subject"].lower()
    except:
        subject = "bw a4"

    # prepare answer
    responseMessage = MIMEMultipart()
    responseMessage['Subject'] = 'Your Scan'
    responseMessage['From'] = login["user"]
    responseMessage['To'] = sender
    text = MIMEText(login["message"])
    responseMessage.attach(text)

    # parse subject for arguments
    argsubject = subject.split()
    args = {"out": "./", "name": "out", "format": "pdf", "koriginal": "false", "dpi": 80 }
    if "bw" in argsubject:
        args["bw"] = "true"
    else:
        args["bw"] = "false"
    if "a4" in argsubject:
        args["a4"] = "true"
    else:
        args["a4"] = "false"

    print "parsed args"

    # process images and add them to answer
    for part in msg.walk():
        atype, fformat = part.get_content_type().split("/")
        if atype == "image" and (fformat in ["jpeg", "png", "jpg"]):
            open('attachment.' + fformat, 'wb').write(part.get_payload(decode=True))
            args["image"] = 'attachment.' + fformat
            core.processImage(args)
            img_data = open(os.path.abspath("out.pdf"), 'rb').read()
            image = MIMEImage(img_data, name=os.path.basename("out.pdf"), _subtype="pdf")
            responseMessage.attach(image)

    print "processImage"

    # send mail
    s = smtplib.SMTP("smtp." + login["host"], login["port"])
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(login["user"], login["password"])
    s.sendmail(login["user"], sender, responseMessage.as_string())
    s.quit()

    print "send"

    # mark as read
    for e_id in uids:
        mailer.store(e_id, '+FLAGS', '\Seen')

    print "taged as seen"





