import xadmin

from .models import UserAsk, CourseComment, UserFavorite, UserMessage, UserCourse


class UserAskAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name', 'add_time']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)


class CourseCommentAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['user', 'course', 'comment', 'add_time']
    search_fields = ['user', 'course', 'comment', 'add_time']
    list_filter = ['user', 'course', 'comment', 'add_time']


xadmin.site.register(CourseComment, CourseCommentAdmin)


class UserFavoriteAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type', 'add_time']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


xadmin.site.register(UserFavorite, UserFavoriteAdmin)


class UserMessageAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read', 'add_time']
    list_filter = ['user', 'message', 'has_read', 'add_time']


xadmin.site.register(UserMessage, UserMessageAdmin)


class UserCourseAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']


xadmin.site.register(UserCourse, UserCourseAdmin)