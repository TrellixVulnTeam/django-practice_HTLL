from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):  # 普通的class
    @method_decorator(login_required(login_url='/user_login/'))  # 'user_login'
    def dispatch(self, request, *args, **kwargs):  # 这个必须这样写
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
