import smtplib
from email.mime.text import MIMEText

'''发送文本邮件'''
# MIMEText三个主要参数
# 1. 邮件内容
# 2. MIME子类型，在此案例我们用plain表示text类型
# 3. 邮件编码格式
msg = MIMEText('Hello, I am SmallHong', 'plain', 'utf-8')

# 发送email地址
from_addr = '1490801698@qq.com'
# 此处密码是经过申请设置后的授权码，不是qq邮箱密码
from_pwd = 'tnhvdvtvqeppgidb'

# 收件人信息
# 此处使用qq邮箱，自己发给自己
to_addr = '1490801698@qq.com'

# 输入SMTP服务器地址
# 此处根据不同的邮件服务商有不同的值
# 现在基本任何一家邮件服务商，如果采用第三方收发邮件，都需要开启授权选项
# 腾讯qq邮箱的smtp地址是smtp.qq.com
smtp_srv = 'smtp.qq.com'

try:
    # 两个参数
    # 参数1：服务器地址，必须使用bytes流格式，所以必须对此进行编码
    # 参数2：服务器的接受访问端口
    srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465) # SMTP 协议默认端口25
    # 登录邮箱发送
    srv.login(from_addr, from_pwd)
    # 发送邮件
    # 三个参数：
    # 参数1：发送地址
    # 参数2：接受地址，必须是list形式
    # 参数3：发送内容，必须作为字符串发送
    srv.sendmail(from_addr, [to_addr], msg.as_string())
    # 退出
    srv.quit()
except Exception as e:
    print(e)

'''发送html邮件'''
mail_content = '''
        <!DOCTYPE html>
        <html lang="en>
        <head>
            <meta charset="UTF_8">
            <title>Title</title>
        </head>
        <body>
            <h1>这是一封HTML格式邮件</h1>
        </body>
        </html>
        '''

msg = MIMEText(mail_content, 'html', 'utf-8')

# 构建发送着地址和登录信息
from_addr = '1490801698@qq.com'
from_pwd = 'tnhvdvtvqeppgidb'

# 构建邮件接受者信息
to_addr = '1490801698@qq.com'

smtp_srv = 'smtp.qq.com'

try:
    srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465) # SMTP 协议默认端口25

    srv.login(from_addr, from_pwd)

    srv.sendmail(from_addr, [to_addr], msg.as_string())
    srv.quit()
except Exception as e:
    print(e)


'''发送带附件的邮件'''
from email.mime.multipart import MIMEBase, MIMEMultipart

mail_mul = MIMEMultipart()

# 构建邮件正文
mail_text = MIMEText('Hello, I am SmallHong', 'plain', 'utf-8')
# 把构建好的邮件正文附加入邮件中
mail_mul.attach(mail_text)

# 构建附件
# 构建附件，需要从本地读入附件
# 打开一个本地文件
# 以rb格式打开
with open('02.html', 'rb') as f:
    s = f.read()
    # 设置附件的MIME和文件名
    m = MIMEText(s, 'base64', 'utf-8')
    m['Content-Type'] = 'application/octet-stream'
    # 注意
    # 1. attachment后分号为英文状态
    # 2. filename 后面需要使用引号包裹，注意与外面引号错开
    m['Content_Disposition'] = 'attachment; filename="02.html"'
    # 添加到MIMEMultipart
    mail_mul.attach(m)

# 发送email地址
from_addr = '1490801698@qq.com'
from_pwd = 'tnhvdvtvqeppgidb'

to_addr = '1490801698@qq.com'

smtp_srv = 'smtp.qq.com'

try:
    srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465) # SMTP 协议默认端口25

    srv.login(from_addr, from_pwd)

    srv.sendmail(from_addr, [to_addr], mail_mul.as_string())
    srv.quit()
except Exception as e:
    print(e)


'''发送带有邮件头或抄送的邮件'''
from email.header import Header

msg = MIMEText('Hello world', 'plain', 'utf-8')

# 注意，下面代码故意写错，说明，所谓的发送者的地址，只是从一个Header的第一个参数作为字符串构建的
# 用utf-8编码是因为很可能包含非英文字符
header_from = Header('这是SmallHong发送出去的邮件', 'utf-8')
msg['From'] = header_from

header_to = Header('由BigGrey接受的', 'utf-8')
msg['To'] = header_to

header_sub = Header('这是小红和大灰之间的主题', 'utf-8')
msg['Subject'] = header_sub

from_addr = '1490801698@qq.com'
from_pwd = 'tnhvdvtvqeppgidb'

to_addr = '1490801698@qq.com'

smtp_srv = 'smtp.qq.com'

try:
    srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465) # SMTP 协议默认端口25

    srv.login(from_addr, from_pwd)

    srv.sendmail(from_addr, [to_addr], mail_mul.as_string())
    srv.quit()
except Exception as e:
    print(e)


'''同时发送支持html和text格式的邮件'''

msg = MIMEMultipart('alternative')

html_content = '''
        <!DOCTYPE html>
        <html lang="en>
        <head>
            <meta charset="UTF_8">
            <title>Title</title>
        </head>
        <body>
            <h1>这是一封HTML格式邮件</h1>
        </body>
        </html>
        '''

msg_html = MIMEText(html_content, 'html', 'utf-8')
msg.attach(msg_html)

msg_text = MIMEText('just text content', 'plain', 'utf-8')
msg.attach(msg_text)

from_addr = '1490801698@qq.com'
from_pwd = 'tnhvdvtvqeppgidb'

to_addr = '1490801698@qq.com'

smtp_srv = 'smtp.qq.com'

try:
    srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465) # SMTP 协议默认端口25

    srv.login(from_addr, from_pwd)

    srv.sendmail(from_addr, [to_addr], msg.as_string())
    srv.quit()
except Exception as e:
    print(e)

