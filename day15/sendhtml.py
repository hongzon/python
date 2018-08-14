#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = '3431319639@qq.com'
receivers = ['1374625832@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

mail_msg = """
<p>在Http请求中，我们每天都在使用Content-type来指定不同格式的请求信息，但是却很少有人去全面了解content-type中允许的值有多少，这里将讲解Content-Type的可用值</p>
<p>MediaType，即是Internet Media Type，互联网媒体类型；也叫做MIME类型，在Http协议消息头中，使用Content-Type来表示具体请求中的媒体类型信息</p>
"""
message = MIMEText(mail_msg, 'html', 'utf-8')
message['From'] = Header("zhz", 'utf-8')
message['To'] = Header("wds", 'utf-8')

subject = 'http'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP('smtp.qq.com')
    smtpObj.starttls()
    smtpObj.login(sender, 'cyrwmqrnsivadadf')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print
    "邮件发送成功"
except smtplib.SMTPException:
    print("Error: 无法发送邮件")