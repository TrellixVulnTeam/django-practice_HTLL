from django import forms
import re  # 引入正则表达式
from operation.models import UserAsk


# 这里的表单用模型表单来做，即由模型直接生成表单
class UserAskForm(forms.ModelForm):  # 注意这里继承的是ModelForm模型表单

    class Meta:
        model = UserAsk  # 表示针对UserAsk模型
        fields = ['name', 'mobile', 'course_name']  # 挑选想要的字段

    def clean_mobile(self):  # 这里用到自定义验证方式，验证函数必须定义成这个，表单会自动进行验证
        """
        验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data['mobile']  # 去除表单中的mobile字段，cleaned_data是字典类型的
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")  # 这里需要添加一个将手机好吗非法传递到前端的方式




























































