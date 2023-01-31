from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.models import User  # django 内置的数据库用户模型
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import login_required  # @login_required 装饰view 函数，要求在view 函数前先检查是否登录
from django.contrib.sessions.backends.db import SessionStore

import simplejson

from messages import Messages

# Create your views here.

# 自定义session 认证装饰器
from functools import wraps


def user_login_required(viewfunc):
    # 参照 django.contrib.auth.decorators.login_required
    @wraps(viewfunc)
    def wrapper(request, *args, **kwargs):
        print('user_login_required ~~~~~~~~~~~是否认证 = ', request.user.is_authenticated, request.session.items())
        if request.user.is_authenticated:
            # 获取session 信息
            session: SessionStore = request.session
            print(type(session))
            print(session.items(), sep='\n\n')
            # 设置session 信息
            session["userinfo"] = {
                "username":request.user.username,
                "userid": request.user.id
            }

            return viewfunc(request, *args, *kwargs)
        return HttpResponse("认证不通过", status=401)
    return wrapper


# 注册视图函数
@require_POST
def reg(req: HttpRequest):
    print('~' * 30)
    print(req.path)
    print(req.content_type)  # application/json
    print(req.body)  # 此时为文本形式
    print(simplejson.loads(req.body))  # 转换为python 字典后打印
    print('=' * 30)
    try:
        payload = simplejson.loads(req.body)
        username = payload["name"]  # 用索引查回来
        # 判断用户名是否已存在？浏览器端有没有提醒过用户，永远不要相信客户端：使用模板和数据库用户对比
        count = User.objects.filter(username=username).count()
        if count > 0:  # 用户已存在
            return JsonResponse(Messages.USER_EXITS)

        # 数据存储
        email = payload["email"]
        password = payload["password"]
        # 使用 django 内建模型自带的创建用户的方法：create_user
        user = User.objects.create_user(username, email, password)  # 新增用户存储到数据库,内部调用了 user_save
        print(type(user), user)  # 一旦创建成功，登录成功看到的应该是 User 的实例

        return JsonResponse({"result": "success"}, status=201)  # 成功则返回201
    except Exception as e:  # 有任何异常，都需要返回
        print('eee', e)
        return JsonResponse(Messages.INVALID_USERNAME_PASSWORD, status=200)


# 登录且认证后的跳转首页的视图函数
# @login_required   # django 提供的session 认证方法
@user_login_required  # 用户自定义的session 认证方法
def userindex(request: HttpRequest):
    if request.user.is_authenticated:
        s = 200
        print('userindex~~~~~~~~~~~', *request.session.items(), sep='\n\n')
    else:
        s = 400
    print('^^' * 30)
    return JsonResponse({"page": "index"}, status=s)


# 登录视图函数
@require_POST
def userlogin(request: HttpRequest):
    # 获取用户信息
    try:
        payload = simplejson.loads(request.body)
        # print(type(payload), payload)  # dict
        username = payload["name"]  # 获取到用户登录信息后，如何处理？
        password = payload['password']
        user = authenticate(request, username=username,
                            password=password)  # 比较用户信息,若在数据库存在唯一用户且值一一对应，则返回 User 类对象；否则返回为 none
        # print(type(user), user)
        # print('响应set-cookie 前', type(request.user),
        #       request.user)  # <class 'django.utils.functional.SimpleLazyObject'> AnonymousUser
        # print('响应set-cookie 前', request.session.items())  # dict_items([])
        # print('$' * 30)
        if user:  # 用户匹配成功，则？
            # cookie 和 session，首先，服务器端必须对认证成功的用户浏览器发一个身份id，response 中增加set-cookie，至少应该有session-id。
            # 同时，session-id 也必须保存在服务器端
            login(request, user)  # 各种后台jsp，php，都习惯通过 request.session 取seddion 值。将user属性捆绑到 request 对象
            # print('响应set-cookie 后', type(request.user), request.user)  # <class 'django.contrib.auth.models.User'> user1
            # print('响应set-cookie 后',
            #       request.session.items())  # # dict_items([('_auth_user_id', '2'), ('_auth_user_backend', 'django.contrib.auth.backends.ModelBackend'), ('_auth_user_hash', 'd98872fce7748ce4ab9...')])
            # print('*' * 30)
            return JsonResponse({"result": "success"}, status=201)  # 用户认证成功又当如何？
        return JsonResponse(Messages.INVALID_USERNAME_PASSWORD, status=200)
    except Exception as e:
        print('******************', e)
        return JsonResponse(Messages.BAD_REQUEST, status=200)


# 登出视图函数
@user_login_required
def userlogout(request: HttpRequest):
    # print('~'*30)
    # print('logout 登出视图函数')
    # print('登出前~~~~~~~sessionid=', request.session.items())
    logout(request)
    # print('登出后~~~~~~~sessionid=', request.session.items())

