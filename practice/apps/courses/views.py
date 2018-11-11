from django.shortcuts import render
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import View  # 用于基于类的函数
from .models import Course, CourseResource, Video, Teacher
from operation.models import UserFavorite, CourseComment, UserCourse
from django.http import HttpResponse
from django.db.models import Q  # Q用于并操作
from utils.mixin_utils import LoginRequiredMixin  # 引入登录验证的类
# Create your views here.


class CoursesListView(View):
    def get(self, request):
        all_courses = Course.objects.all()
        hot_courses = all_courses.order_by('-fav_nums')[:3]

        # 主页全局搜索中的课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords))  # 注意这里是双下划线


        latest = all_courses.order_by("-add_time")
        sort = request.GET.get("sort", "")
        if sort == "hot":
            all_courses = all_courses.order_by("-fav_nums")

        elif sort == "students":
            all_courses = all_courses.order_by("-students")
        else:
            pass
        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_courses, 3, request=request)  # 第一个是待分页对象，第二个是每页显示数量，

        courses = p.page(page)  # 生成分页数据
        return render(request, 'course-list.html', {'all_courses': courses,
                                                    'sort': sort,
                                                    'hot_courses': hot_courses
                                                    }
                      )


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()
        has_fav = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):  # 查询此课程是否被收藏
                has_fav = True
        tag = course.tag
        if tag:
            related_course = Course.objects.filter(tag=tag)[:2]
        else:
            related_course = []  # 注意这里就算没有也要传个空的数组到前端，因为前端要进行循环，不能传个字符串回去
        return render(request, 'course-detail.html', {'course': course,
                                                      'related_course': related_course,
                                                      'has_fav': has_fav

                                                      }
                      )


# 这是基于类的视图函数，不能直接用装饰器修饰
class CourseInfoView(LoginRequiredMixin, View):  # 继承LoginRequireMixin来验证登陆，注意继承顺序不能变
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()
        # 查询用户是否已经关联该课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:  # 若没有关联，就将其关联，表示用户学习了该课程
            user_course = UserCourse(user=request.user, course=course)

            user_course.save()
        # 取出所有user的id
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 注意是双下划线
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该课程的所有用户学过其他的课程,注意他的查询方式，使用UserCourse作为连接Course和User的桥梁
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {'course': course,
                                                     'course_resource': all_resources,
                                                     'related_courses': related_courses}
                      )


class CommentsView(LoginRequiredMixin, View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        all_comment = CourseComment.objects.all()
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-comment.html', {'course': course,
                                                       'course_resource': all_resources,
                                                       'all_comment': all_comment}
                      )


class AddCommentsView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated():  # 就算没有登陆，request.user也有，但是是一个匿名的类
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comment = request.POST.get('comments', '')
        if int(course_id) > 0:
            course = Course.objects.get(id=int(course_id))
            course_comment = CourseComment()
            course_comment.course = course
            course_comment.user = request.user
            course_comment.comment = comment
            course_comment.save()
            # all_comments = CourseComment.objects.all()
            # return render(request, 'course-comment.html', {'course': course,
            #                                                'all_comments': all_comments})
            return HttpResponse('{"status":"success", "msg":"发表成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"发表失败"}', content_type='application/json')


class VideoPlayView(View):
    """
    视频播放页面
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        course = video.lesson.course
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:  # 若没有关联，就将其关联，表示用户学习了该课程
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 取出所有user的id
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 注意是双下划线
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该课程的所有用户学过其他的课程,注意他的查询方式，使用UserCourse作为连接Course和User的桥梁
        related_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {'course': course,
                                                    'course_resource': all_resources,
                                                    'related_courses': related_courses,
                                                    'video': video}
                      )













