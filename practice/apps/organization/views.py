from django.shortcuts import render
from django.views.generic.base import View  # 用于基于类的函数
from django.shortcuts import render_to_response
from .forms import UserAskForm
from django.http import HttpResponse  # 用于指明返回的数据类型

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from courses.models import Course, Lesson
from users.models import UserProfile
from operation.models import UserFavorite
from django.db.models import Q  # Q用于并操作
from .models import CourseOrg, City, Teacher
# Create your views here.


class OrgView(View):
    def get(self, request):
        all_cities = City.objects.all()
        all_orgs = CourseOrg.objects.all()
        all_orgs_1 = all_orgs

        # 主页全局搜索中的机构搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))
                                            # 注意这里是双下划线

        # 对机构进行点击量排名
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 对机构进行学生数和课程数量排名
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")

        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")
        else:
            pass

        # 筛选城市
        city_id = request.GET.get('city', "")

        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))  # 机构与城市是多对一，每个机构的城市字段存储城市的id根据city_id来筛选机构
        category = request.GET.get('cate', "")
        if category:
            all_orgs = all_orgs.filter(category=category)
        orgs_count = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs, 5, request=request)  # 第一个是待分页对象，第二个是每页显示数量，

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "all_cities": all_cities, "allorgs": all_orgs_1, "all_orgs": orgs, "orgs_count": orgs_count,
            "city_id": city_id,  # 将city_id传到前端进行比对从而实现显著标识
            "category": category,  # 前端传来的机构类别再传回去
            "hot_orgs": hot_orgs,  # 排名回传
            "sort": sort  # 排序方式回传
        })


# 处理前端用户填写的咨询表单，这里用到异步操作，结果不是跳转到某个页面，而是用HttpResponse返回json字符串
class AddUserAskView(View):
    def get(self, request):
        pass

    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask = user_ask_form.save(commit=True)  # 模型表单直接保存成一组数据到数据库
            return HttpResponse('{"status":"success"}', content_type='application/json')  # 指明返回的是json字符串，语法是固定的
                                                                                          # 浏览器自动解析成json数据
        else:
            return HttpResponse('{"status":"fail", "msg":"添加错误"}', content_type='application/json')  #
            # 注意HttpResponse的参数单双引号不能错


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        has_fav = False

        course_org = CourseOrg.objects.get(id=org_id)
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):  # 查询此机构是否被收藏
                has_fav = True

        all_courses = course_org.course_set.all()[:3]  # 这里用到反向的检索，由机构检索该机构的所有课程，取前3个
        # all_courses = Course.objects.filter(course_org=course_org)  # 这个是正向检索，正常思维
        all_teachers = course_org.teacher_set.all()[:]  # 同理检索机构的教师，取前3个
        current_page = 'home'  # current_page用于检测当前页面来修改标签属性从而改变外观
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses, 'all_teachers': all_teachers, 'course_org': course_org,
            'current_page': current_page, 'has_fav': has_fav
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=org_id)
        has_fav = False

        course_org = CourseOrg.objects.get(id=org_id)
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):  # 查询此机构是否被收藏
                has_fav = True
        all_courses = course_org.course_set.all()  # 这里用到反向的检索，由机构检索该机构的所有课程，取前3个
        current_page = 'org_detail'
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses, 'course_org': course_org, 'current_page': current_page,
            'has_fav': has_fav
        })


class OrgDescView(View):
    """
    机构详情
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=org_id)
        has_fav = False

        course_org = CourseOrg.objects.get(id=org_id)
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):  # 查询此机构是否被收藏
                has_fav = True
        desc = course_org.desc
        current_page = 'org_desc'

        return render(request, 'org-detail-desc.html', {'desc': desc, 'current_page': current_page,
                                                        'course_org': course_org, 'has_fav': has_fav})


class OrgTeacherView(View):
    """
    机构详情
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=org_id)
        has_fav = False


        course_org = CourseOrg.objects.get(id=org_id)
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):  # 查询此机构是否被收藏
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        current_page = 'org_detail_teacher'

        return render(request, 'org-detail-teachers.html', {'all_teachers': all_teachers, 'current_page': current_page,
                                                            'course_org': course_org,
                                                            'has_fav': has_fav})


class AddFavView(View):
    """
    用户收藏,取消收藏功能
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', '0')
        fav_type = request.POST.get('fav_type', '0')

        # 判断用户登录状态
        if not request.user.is_authenticated():  # 就算没有登陆，request.user也有，但是是一个匿名的类
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')  # 告诉Ajax，
                                                                                        # Ajax会根据status来进行处理
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 记录已经存在，则取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏已删除"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_type = int(fav_type)
                user_fav.fav_id = int(fav_id)
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"收藏成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏错误"}', content_type='application/json')


class TeachersListView(View):
    """
    课程讲师列表
    """

    def get(self, request):
        teachers = Teacher.objects.all()

        # 主页全局搜索中的机构搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            teachers = teachers.filter(Q(name__icontains=search_keywords))
            # 注意这里是双下划线

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            teachers = Teacher.objects.all().order_by('-fav_nums')

        hot_teachers = Teacher.objects.all().order_by('-fav_nums')
        # 对教师分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(teachers, 1, request=request)  # 第一个是待分页对象，第二个是每页显示数量，

        all_teachers = p.page(page)
        return render(request, 'teachers-list.html', {'teachers': teachers,
                                                      'all_teachers': all_teachers,
                                                      'sort': sort,
                                                      'hot_teachers': hot_teachers


                                                      }
                      )


class TeacherDetailView(View):
    """
    教师详情
    """

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        org = CourseOrg.objects.get(id=teacher.org.id)
        hot_teachers = Teacher.objects.all().order_by('-fav_nums')
        courses = Course.objects.filter(teacher=teacher)
        has_teacher_faved = False
        has_org_faved = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):  # 查询此机构是否被收藏
                has_org_faved = True

            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):  # 查询此教师是否被收藏
                has_teacher_faved = True

        return render(request, 'teacher-detail.html', {'teacher': teacher,
                                                       'courses': courses,
                                                       'hot_teachers': hot_teachers,
                                                       'has_org_faved': has_org_faved,
                                                       'has_teacher_faved': has_teacher_faved
                                                       }
                      )


















