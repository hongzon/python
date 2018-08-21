#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

sender = '3431319639@qq.com'
receivers = ['1374625832@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# 创建一个带附件的实例
message = MIMEMultipart()
message['From'] = Header("zhz", 'utf-8')
message['To'] = Header("zhz", 'utf-8')
subject = '附件'
message['Subject'] = Header(subject, 'utf-8')

# 邮件正文内容
# message.attach(MIMEText('附件', 'plain', 'utf-8'))
# message.attach(MIMEText('<html><body><h1>Hello</h1>' +
#     '<p><img src="cid:0"></p>' +
#     '</body></html>', 'html', 'utf-8'))
# 构造附件1，传送当前目录下的 test.txt 文件
# att1 = MIMEText(open('test.xlsx', 'rb').read(), 'base64', 'utf-8')
# att1["Content-Type"] = 'application/octet-stream'
# # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
# att1["Content-Disposition"] = 'attachment; filename="test.xlsx"'
# message.attach(att1)
#图片发送 貌似不能用
with open('1.jpg', 'rb') as f:
    # 设置附件的MIME和文件名，这里是jpg类型:
    mime = MIMEImage(f.read())
    # 加上必要的头信息:
    mime.add_header('Content-Disposition', 'attachment', filename='1.jpg')
    mime.add_header('Content-ID', '<0>')
    message.attach(mime)

# with open('1.jpg', 'rb') as f:
#     # 设置附件的MIME和文件名，这里是jpg类型:
#     mime = MIMEBase('image', 'jpg', filename='1.jpg')
#     # 加上必要的头信息:
#     mime.add_header('Content-Disposition', 'attachment', filename='1.jpg')
#     mime.add_header('Content-ID', '<0>')
#     mime.add_header('X-Attachment-Id', '0')
#     # 把附件的内容读进来:
#     mime.set_payload(f.read())
#     # 用Base64编码:
#     encoders.encode_base64(mime)
#     # 添加到MIMEMultipart:
#     message.attach(mime)

# 构造附件2，传送当前目录下的 runoob.txt 文件
# att2 = MIMEText(open('runoob.txt', 'rb').read(), 'base64', 'utf-8')
# att2["Content-Type"] = 'application/octet-stream'
# att2["Content-Disposition"] = 'attachment; filename="runoob.txt"'
# message.attach(att2)

try:
    smtpObj = smtplib.SMTP('smtp.qq.com')
    smtpObj.starttls()
    smtpObj.login(sender, 'cyrwmqrnsivadadf')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print
    "Error: 无法发送邮件"