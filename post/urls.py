from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import user_login_required, getpost, PostView,getToken


urlpatterns = [
    # path('', PostView.as_view())

    # 映射并调用视图函数时，传递的参数：(request, * args, **kwargs)
    # PostView.as_view() --> view
    # view() --> handler(request, *args, **kwargs) --> post(request, *args, **kwargs)
    # user_login_required(PostView.as_view()) --> user_login_required(view) --> wrapper
    # path('', user_login_required(['get'])(PostView.as_view()))
    # path('', user_login_required(['get'])(PostView.as_view())),   # 直接使用 method_decorator 装饰类视图
    path('', PostView.as_view()),
    path('<int:id>/', getpost),
    path('gettoken/', getToken)

]