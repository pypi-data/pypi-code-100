# import smtplib
# from email.header import Header
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText


# def sendMail(host, password, fromMail, toMailList, subject, content='', attachmentList=None):
#     '''发送邮件 attachmentList格式为[(name, bytes), ...]'''

#     message = MIMEMultipart()
#     message['From'] = fromMail
#     message['To'] = ','.join(toMailList)
#     message['Subject'] = Header(subject, 'utf-8')
#     message.attach(MIMEText(content, 'plain', 'utf-8'))

#     if attachmentList:
#         for item in attachmentList:
#             att = MIMEText(item[1], 'base64', 'utf-8')
#             att['Content-Type'] = 'application/octet-stream'
#             # att['Content-Disposition'] = 'attachment; filename="file.txt"'
#             att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', item[0]))
#             message.attach(att)

#     smtpObj = smtplib.SMTP_SSL()
#     smtpObj.connect(host)
#     smtpObj.login(fromMail, password)
#     smtpObj.sendmail(fromMail, toMailList, message.as_string())
