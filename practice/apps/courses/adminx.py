import xadmin

from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']


xadmin.site.register(Course, CourseAdmin)


class LessonAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name', 'add_time']
    list_filter = ['course__name', 'name', 'add_time']  # 按照课程名筛选


xadmin.site.register(Lesson, LessonAdmin)


class CourseResourceAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['name', 'course', 'add_time', 'download']
    search_fields = ['name', 'course', 'add_time', 'download']
    list_filter = ['name', 'course', 'add_time', 'download']


xadmin.site.register(CourseResource, CourseResourceAdmin)


class VideoAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name', 'add_time']
    list_filter = ['lesson', 'name', 'add_time']


xadmin.site.register(Video, VideoAdmin)


