from django.shortcuts import render
import json  # 用于修改密码格式错误时返回前端信息
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q  # Q用于并操作
from django.views.generic.base import View  # 用于基于类的函数
from django.contrib.auth.hashers import make_password  # 用于生成密码

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm
from operation.models import UserCourse, UserFavorite
from organization.models import CourseOrg, Teacher
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse
# Create your views here.


# 这里自定义一个登录验证逻辑，是对系统逻辑ModelBackend的authenticate方法的改写
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
            else:
                return None
        except Exception as e:
            return None


# 这个是基于类的登录验证视图
class LoginView(View):  # 继承View类，这个类中定义了get,post等方法，我们继承后改写就行了
    def get(self, request):  # 在这种基于类的视图中无需像下面直接定义函数而做成的方法中判断请求方式是get还是post，在基于类的方法中他会根据请求方式自动调用对应的方法
        return render(request, "login.html")  # 注意：从首页点击登录选项时，就是以get方式访问user_login，所以get访问方式也存在

    def post(self, request):
        login_form = LoginForm(request.POST)  # Form实例化需要字典参数，request.POST为一个提交表单的字典，他会自动与LoginForm表单里的字段对应
        if login_form.is_valid():  # 若form校验通过

            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            user = authenticate(username=user_name, password=pass_word)  # 这里必须要命名参数

            if user is not None:
                if UserProfile.objects.get(username=user_name).is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, 'login.html', {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {'msg': "用户名或密码错误", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})  # form校验不通过


# 这个是基于函数的登录方法，需要判断请求方式，可行，不推荐
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#
#         user = authenticate(username=user_name, password=pass_word)  # 这里必须要命名参数
#
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html")
#         else:
#             return render(request, "login.html", {'msg': "用户名或密码错误"})
#
#     else:
#         return render(request, "login.html")  # 注意：从首页点击登录选项时，就是以get方式访问user_login，所以get访问方式也存在


# 用户注册（基于类的视图）
class RegisterView(View):  # 依然继承View类，改写里面的方法
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {"msg": "用户已存在", "register_form": register_form})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # send_register_email('username', 'register')
            send_register_email(user_name, 'register')
            return render(request, "login.html")
        else:
            return render(request, "register.html", {'register_form': register_form})


# 用户激活链接视图
class ActiveUserView(View):
    def get(self, request, active_code):  # 这里的active_code是url中带进来的
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'login.html')
        else:
            return render(request, 'active_fail.html')


class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email('username', 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forgetpwd_form': forgetpwd_form})


# 用户重置密码链接视图
class ResetView(View):
    def get(self, request, reset_code):  # 这里的reset_code是url中带进来的
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {"email": email})
        else:
            return render(request, 'active_fail.html')

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email","")
            if pwd1 == pwd2:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd2)
                user.save()
                return render(request, "login.html")
            else:
                return render(request, "password_reset.html", {"msg": "密码不一致", "email": email})
        else:
            return render(request, "password_reset.html", {"msg": "输入错误，请重新输入"})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        user = request.user

        return render(request, 'usercenter-info.html', {

        })


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        upload_image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if upload_image_form.is_valid():
            #image = upload_image_form.cleaned_data['image']  # cleaned_data[]里面是验证通过的字段数据，
                                                              # 前面写了instance就不用取了
            #request.user.image = image
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')  # 指明返回的是json字符串，语法是固定的
                                        # 浏览器自动解析成json数据
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')  # 指明返回的是json字符串，语法是固定的
            # 浏览器自动解析成json数据
            pass


class UpdatePwdView(View):
    """
    个人中心修改密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 == pwd2:
                user = request.user
                user.password = make_password(pwd2)
                user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"密码输入不一致"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class MyCoursesView(LoginRequiredMixin, View):
    """
    用户个人课程
    """
    def get(self, request):
        user = request.user
        user_courses = UserCourse.objects.filter(user=user)

        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses
        }
                      )


class MyFavoriteOrgsView(LoginRequiredMixin, View):
    """
    用户收藏的机构
    """
    def get(self, request):
        user = request.user
        orgs_list = []  # 设定一个数组用于存放收藏的机构
        user_fav_orgs = UserFavorite.objects.filter(user=user, fav_type=2)
        for org in user_fav_orgs:
            org_id = org.fav_id
            fav_org = CourseOrg.objects.get(id=org_id)
            orgs_list.append(fav_org)
        return render(request, 'usercenter-fav-org.html', {
            'user_fav_orgs': orgs_list
        }
                      )


class MyFavoriteTeachersView(LoginRequiredMixin, View):
    """
    用户收藏的讲师
    """
    def get(self, request):
        user = request.user

        teachers_list = []  # 设定一个数组用于存放收藏的机构
        user_fav_teachers = UserFavorite.objects.filter(user=user, fav_type=3)
        for teacher in user_fav_teachers:
            teacher_id = teacher.fav_id
            fav_teacher = Teacher.objects.get(id=teacher_id)
            teachers_list.append(fav_teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'user_fav_teachers': teachers_list
        }
                      )


























































