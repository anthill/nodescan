
import os
import re
import json
import smtplib, imaplib
from email import parser
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from subprocess import check_call


login = json.loads(open("login.json","r").read())

# get unseen mails
mail = imaplib.IMAP4_SSL("imap." + login["host"], 993)
mail.login(login["user"], login["password"])
mail.select('INBOX')
result, data = mail.search(None, "ALL")
uids = data[0].split()
newmails = [mail.fetch(uids[i], "(RFC822)")[1][0][1] for i in range(len(uids))]

for mail in newmails:
    # parse mail and content
    msg = parser.Parser().parsestr(mail)
    sender = re.search("<([\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4})>", msg["From"]).group(1)
    subject = msg["Subject"].lower()

    # prepare answer
    msg = MIMEMultipart()
    msg['Subject'] = 'Your Scan'
    msg['From'] = login["user"]
    msg['To'] = sender
    text = MIMEText(login["message"])
    msg.attach(text)

    # parse subject for arguments
    args = subject.split(" ")
    if "bw" in args:
        bw = "true"
    else:
        bw = "false"
    if "a4" in args:
        a4 = "true"
    else:
        a4 = "false"

    # process images and add them to answer
    for part in msg.walk():
        atype, format = attachment.get_content_type().split("/")
        if atype == "image":
            open('attachment.' + format, 'wb').write(part.get_payload(decode=True))
            check_call(["python", os.path.abspath("scan.py"), "-i", 'attachment.' + format, "-b", bw, "-a", a4])
            img_data = open(os.path.abspath("out.pdf"), 'rb').read()
            image = MIMEImage(img_data, name=os.path.basename("out.pdf"), _subtype="pdf")
            msg.attach(image)

    # send mail
    s = smtplib.SMTP("smtp." + login["host"], login["port"])
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(login["user"], login["password"])
    s.sendmail(login["user"], sender, msg.as_string())
    s.quit()

    # mark as read
    for e_id in uids:
        mail.store(e_id, '+FLAGS', '\Seen')






