from users.models import EmailVerifyRecord
from random import Random  # 引入Random函数
from django.core.mail import send_mail
from practice.settings import EMAIL_FROM  # 引入settings中设定的EMAIL发送方


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    random_str = generate_random_str()
    email_record.code = random_str
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "注册激活链接"
        email_body = "请点击以下链接激活账户：http://127.0.0.1:8000/active/{0}".format(email_record.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return
    elif send_type == "forget":
        email_title = "找回密码链接"
        email_body = "请点击以下链接重置密码：http://127.0.0.1:8000/forget/{0}".format(email_record.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])


def generate_random_str(randomlength=8):
    str = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    random = Random()
    length = len(chars)-1
    for i in range(randomlength):
        str = str+chars[random.randint(0,length)]
    return str


















































