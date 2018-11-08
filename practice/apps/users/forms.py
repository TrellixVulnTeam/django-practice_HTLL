from django import forms
from .models import UserProfile
from captcha.fields import CaptchaField


# 自定义表单验证，在这里先对前端提交的表单进行校验，校验通过再去查询数据库，从而减轻数据库的负担
class LoginForm(forms.Form):
    username = forms.CharField(required=True)  # 注意这里字段的名称必须要和前端页面的input标签中的name的名称一直才能保证正确对应
    password = forms.CharField(required=True)


# 注册表单
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)  # 默认的Email格式要符合
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


# 密码找回表单
class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)  # 默认的Email格式要符合
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


# 修改密码表单
class ModifyPwdForm(forms.Form):

    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class UploadImageForm(forms.ModelForm):
    """
    用户头像表单
    """
    class Meta:
        model = UserProfile # 表示针对UserProfile模型
        fields = ['image']  # 挑选想要的字段，只要求有图片就行
















































