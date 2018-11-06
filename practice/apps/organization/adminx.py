import xadmin

from .models import City, CourseOrg, Teacher


class CityAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['name', 'desc']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


xadmin.site.register(City, CityAdmin)


class CourseOrgAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['name', 'desc']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


xadmin.site.register(CourseOrg, CourseOrgAdmin)


class TeacherAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'fav_nums']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'fav_nums', 'add_time']


xadmin.site.register(Teacher, TeacherAdmin)

