"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))`
"""
import datetime

import captcha
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, HttpRequest, JsonResponse  # 导入 JsonResponse 对象
from django.template.loader import get_template

# view 函数,根据 request 请求，返回响应的结果
def index(request: HttpRequest):
    mydict = {
        'title': '测试标题',
        'content': '这是测试内容',
        'a': 100,
        'b': 0,
        'c': list(range(10, 20)),
        'd': dict(zip('abcde', 'ABCDE')),
        's': 'abcde',
        'date': datetime.datetime.now()
    }
    context = {'content': 'www.ada.com', 'mydict': mydict}
    print('=' * 30)

    # 加载模板并填充数据的方法二
    from django.shortcuts import HttpResponse, render
    return render(request, 'index.html', context, status=201)   # 从全局配置中，找到加载模板的路径，再从路径中找到index.html


# 不同url path 和不同函数之间的对应关系，不管什么函数执行后，最终都应该返回结果（准备返回给客户端的中间内容，可能还会被包装）
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('index/', index),
    path('users/', include('users.urls')),  # 对 /users 的访问在 users.urls.py 中设置
    path('posts/', include('post.urls')),
    path('captcha/', include('captcha.urls'))   # 图片验证码 路由
]
