from django.conf.urls import url, include
from .views import CoursesListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView\
    , VideoPlayView
urlpatterns = [
    url(r'^list$', CoursesListView.as_view(), name="courses_list"),  # 课程列表
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name="course_detail"),  # 课程详情
    url(r'^info/(?P<course_id>\d+)$', CourseInfoView.as_view(), name="course_video"),
    url(r'^comment/(?P<course_id>\d+)$', CommentsView.as_view(), name="course_comment"),


    # 用户添加评论(js访问)
    url(r'^add_comment/$', AddCommentsView.as_view(), name="add_comments"),

    url(r'^video/(?P<video_id>\d+)$', VideoPlayView.as_view(), name="video_play"),
]














