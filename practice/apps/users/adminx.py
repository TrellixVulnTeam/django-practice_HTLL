import xadmin
from xadmin import views
from .models import EmailVerifyRecord, Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "慕学后台管理"
    site_footer = "ykk_practice"
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):  # 注意这里继承python最顶层的类object，不是models.Model
    list_display = ['title', 'url', 'index', 'add_time']
    search_fields = ['title', 'url', 'index', 'add_time']
    list_filter = ['title', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

