"""practice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
from django.views.generic import TemplateView  # 表示处理静态文件,引入TemplateView类
import xadmin
from django.views.static import serve  # 引入处理静态文件的函数
from practice.settings import MEDIA_ROOT  # 引入MEDIA根目录

# from users.views import user_login  # 引入基于函数的登录验证
from users.views import IndexView, LoginView, RegisterView, ActiveUserView, ForgetPwdView, \
    ResetView, LogoutView  # 引入基于类的登录验证
from organization.views import OrgView
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name="index"),  # 这里用TemplateView类中的as_view方法
    # url('^user_login/$', user_login, name="user_login")  # 基于函数的登录验证
    url('^user_login/', LoginView.as_view(), name="user_login"),  # 注意调用基于类的方法时要加上括号
    url('^user_logout/', LogoutView.as_view(), name="user_logout"),

    url('^register/', RegisterView.as_view(), name="user_register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),  # 注意url中的active_code是参数，
                                                                                         # 需要传到视图函数中,复习正则表达式
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(P<reset_code>.*)/$', ResetView.as_view(), name="reset_pwd"),

    # 用户组
    url(r'^users/', include('users.urls', namespace='users')),

    # 机构组
    url(r'^org/', include('organization.urls', namespace='org')),

    # 课程组
    url(r'^courses/', include('courses.urls', namespace='courses')),

    # 配置上传文件的访问处理，因为有的图片是放在media中，不是static中，所以要重新配置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),





]
