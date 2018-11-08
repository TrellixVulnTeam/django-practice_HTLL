from django.conf.urls import url, include
from .views import UserInfoView, UploadImageView, UpdatePwdView
urlpatterns = [
    url(r'^info', UserInfoView.as_view(), name="user_info"),  # 课程列表
    url(r'^image/upload', UploadImageView.as_view(), name="image_upload"),  # 用户头像上传
    url(r'^pwd/update', UpdatePwdView.as_view(), name="pwd_update"),  # 个人中心密码修改






]
