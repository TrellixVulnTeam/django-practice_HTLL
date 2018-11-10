from django.conf.urls import url, include
from .views import UserInfoView, UploadImageView, UpdatePwdView, MyCoursesView, MyFavoriteOrgsView, \
    MyFavoriteTeachersView, MyFavoriteCoursesView, MyMessageView
urlpatterns = [
    url(r'^info', UserInfoView.as_view(), name="user_info"),  # 课程列表
    url(r'^image/upload', UploadImageView.as_view(), name="image_upload"),  # 用户头像上传
    url(r'^pwd/update', UpdatePwdView.as_view(), name="pwd_update"),  # 个人中心密码修改

    url(r'^my/courses', MyCoursesView.as_view(), name="my_courses"),  # 用户收藏课程
    url(r'^my_fav/orgs', MyFavoriteOrgsView.as_view(), name="my_fav_orgs"),  # 用户收藏的机构
    url(r'^my_fav/teachers', MyFavoriteTeachersView.as_view(), name="my_fav_teachers"),  # 用户收藏讲师
    url(r'^my_fav/courses', MyFavoriteCoursesView.as_view(), name="my_fav_courses"),  # 用户收藏课程
    url(r'^my/message', MyMessageView.as_view(), name="my_message"),  # 用户消息



]
