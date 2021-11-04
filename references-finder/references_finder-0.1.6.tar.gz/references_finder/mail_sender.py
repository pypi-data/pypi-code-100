import smtplib
import os
from configparser import ConfigParser
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import sys

class Mail_sender():
  def __init__(self, host, from_addr, password):
    self._host = host
    self._from_addr = from_addr
    self._password = password


  def send_mail(self, subject, body_text, *emails,cc_emails=None, bcc_emails=None, file_to_attach=None, enc="utf-8", w_config="smtp"):
    """
    send a mail
    
    """
    assert (self._host and self._from_addr or w_config) is not None, "haven't got host or from_addr"
    
    
    if self._host is None:
        self._host, self._from_addr, self._password = self._host_manager(w_config)
    
    login_data = [self._from_addr, self._password]
        
    # create the message
    msg = MIMEMultipart()
    msg["From"] = self._from_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    if body_text:
        msg.attach( MIMEText(body_text) )
    msg["To"] = ', '.join(emails)
    #msg["cc"] = ', '.join(cc_emails)
    
    header = 'Content-Disposition', 'attachment; filename="%s"' % file_to_attach.split("/")[-1]
    
    attachment = MIMEBase('application', "octet-stream")
    
    if file_to_attach is not None:
        try:
            with open(file_to_attach, "rb") as fh:
                data = fh.read()

            attachment.set_payload( data )
            encoders.encode_base64(attachment)
            attachment.add_header(*header)
            msg.attach(attachment)
        except IOError:
            msg = "Error opening attachment file %s" % file_to_attach
            print(msg)
            sys.exit(1)
    self._sending(emails, msg.as_string())
    
  def _sending(self, emails, msg_str):
    server = smtplib.SMTP(self._host, 587)
    server.starttls()
    if self._password is not None:
        server.login(*[self._from_addr, self._password])
    server.sendmail(self._from_addr, emails, msg_str)
    if emails[0] != "vl.sergiiy@gmail.com":
      print("Письмо отправлено. ")
    server.quit()
    
  def _host_manager(self, config):
    base_path = os.path.dirname(os.path.abspath("mail_sender.ipynb"))
    config_path = os.path.join(base_path, "email.ini")
    
    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        print("Config not found! Exiting!")
        sys.exit(1)
    
    host = cfg.get(config, "server")
    from_addr = cfg.get(config, "from_addr")
    password = cfg.get(config, "password")
    return host, from_addr, password
