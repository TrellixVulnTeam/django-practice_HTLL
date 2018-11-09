from django.conf.urls import url, include
from .views import UserInfoView, UploadImageView, UpdatePwdView, MyCoursesView, MyFavoriteOrgsView, \
    MyFavoriteTeachersView
urlpatterns = [
    url(r'^info', UserInfoView.as_view(), name="user_info"),  # 课程列表
    url(r'^image/upload', UploadImageView.as_view(), name="image_upload"),  # 用户头像上传
    url(r'^pwd/update', UpdatePwdView.as_view(), name="pwd_update"),  # 个人中心密码修改

    url(r'^my/courses', MyCoursesView.as_view(), name="my_courses"),  # 用户收藏课程
    url(r'^my_fav/orgs', MyFavoriteOrgsView.as_view(), name="my_fav_orgs"),  # 用户收藏的机构
    url(r'^my/teachers', MyFavoriteTeachersView.as_view(), name="my_teachers"),  # 用户收藏讲师




]
