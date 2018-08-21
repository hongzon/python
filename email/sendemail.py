from smtplib import SMTP
from email.header import Header
from email.mime.text import MIMEText

def main():
    # 请自行修改下面的邮件发送者和接收者
    sender = '3431319639@qq.com'
    receivers = ['1374625832@qq.com']
    message = MIMEText('背诵兰亭集序.背诵兰亭集序。背诵兰亭集序', 'plain', 'utf-8')
    message['From'] = Header('zhz', 'utf-8')
    message['To'] = Header('zhz', 'utf-8')
    message['Subject'] = Header('语文作业', 'utf-8')
    smtper = SMTP('smtp.qq.com',25)
    smtper.set_debuglevel(1)
    smtper.starttls()
    # 请自行修改下面的登录口令
    smtper.login(sender, 'cyrwmqrnsivadadf')
    smtper.sendmail(sender, receivers, message.as_string())
    smtper.quit()
    print('邮件发送完成!')


if __name__ == '__main__':
	main()