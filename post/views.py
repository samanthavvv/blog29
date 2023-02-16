import datetime
import math
from functools import wraps

import simplejson
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.db.transaction import atomic
from django.views.decorators.csrf import csrf_protect, csrf_exempt, ensure_csrf_cookie

from messages import Messages
from post.models import Post, Content


# 认证装饰器
def user_login_required(exclude_method=None):
    def _user_login_required(viewfunc):
        # 参照 django.contrib.auth.decorators.login_required
        @wraps(viewfunc)
        def wrapper(request, *args, **kwargs):
            nonlocal exclude_method
            print('user_login_required ~~~~~~~~~~~是否认证 = ', request.user.is_authenticated, request.session.items())

            # 如果请求方法类型在白名单之中，则不用认证
            if exclude_method is None:  # 如果白名单中无值
                exclude_method = []

            if request.method.lower() in exclude_method:
                return viewfunc(request, *args, **kwargs)
            else:
                if request.user.is_authenticated:
                    print('认证通过')
                    return viewfunc(request, *args, **kwargs)
            print('认证不通过')
            return JsonResponse(Messages.NOT_LOGIN, status=401)

        return wrapper

    if callable(exclude_method):  # 如果直接装饰了普通的视图函数
        fn = exclude_method
        exclude_method = None
        return _user_login_required(fn)
    return _user_login_required


# Create your views here.
# 详情页
@user_login_required('get')
def getpost(request: HttpRequest, id: int):
    try:
        print(id)
        post = Post.objects.get(pk=id)

        return JsonResponse({'post': {
            'id': post.pk,
            'title': post.title,
            'postdate': post.postdate,  # UTC 字符串
            'author_id': post.author_id,
            'content': post.content.content
        }})
    except Exception as e:
        print(e)
        return JsonResponse(Messages.NOT_FOUND)


# 处理GET 请求中的参数：1. 获取参数，若无，则设置默认值；2. 处理超界问题：这是通用的处理参数，参数的边界问题各不相同，应该让参数自己处理.参考排序方法sort
def validata(d: dict, name: str, default, type_func, validate_fn):
    try:
        value = type_func(d.get(name, default))
        value = validate_fn(value, default)
    except:  # 若有其它异常，比如分页值为一个字母
        value = default
    return value


# 博客列表页：分页
# @method_decorator(user_login_required, name='post')
class PostView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        try:
            page = validata(request.GET, 'page', 1, int,
                            lambda value, default: value if value > 0 else default)
            size = validata(request.GET, 'size', 20, int,
                            lambda value, default: value if value > 0 and value < 101 else default)
            print(page, size)
            start = size * (page - 1)

            # 数据库根据分页返回数据
            mgr = Post.objects
            total = mgr.count()  # 全部博客数

            posts = mgr.order_by('-pk')[start:start + size]  # 查询一般根据从最新发布的文章往前查。最新文章id最大

            return JsonResponse({
                'posts': [
                    {'id': post.id, 'title': post.title}
                    for post in posts
                ],
                'pagination': {
                    'page': page,
                    'size': size,
                    'total': total,
                    'pages': math.ceil(total / size)
                }
            })

        except Exception as e:
            print('??????????????????', e)
            return JsonResponse(Messages.BAD_REQUEST)

    # @user_login_required    # user_login_required(post) 等价于 post=wrapper
    # @method_decorator([user_login_required, csrf_protect])  # 先进行user_login_required 认证，再进行 csrf_protect 认证
    @method_decorator([user_login_required, csrf_protect])
    def post(self, request: HttpRequest, *args, **kwargs):
        try:
            post = Post()
            content = Content()
            payload = simplejson.loads(request.body)
            print(payload)

            # 增、改. post表: id?, title, postdate, author
            if payload.get('id'):  # 改：若数据库中没有对应id记录 ，则也为新增
                uid = Post.objects.filter(id=payload['id'])
                if uid:
                    post.id = payload['id']
                else:
                    return JsonResponse(Messages.BAD_REQUEST, status=409)  # 修改时，若在数据库中未找到对应记录，则不予修改
            post.title = payload['title']
            post.postdate = datetime.datetime.now(  # 数据库存入的是utc 时间，但是django 查询回来时，是设置好的增加了8小时的中国时间
                datetime.timezone(datetime.timedelta(hours=8))
            )
            post.author = request.user  # 作者不能直接填充用户名，需要填充author_id，且必须登录后才有author_id

            content.content = payload['content']  # content 表增加记录：post(post表提交后才有), content

            with atomic():
                post.save()  # save 持久化 做了2个操作，1 是若持久化成功，则直接commit；2 是若失败，则rollback
                content.post = post
                # content.post_id = post.id
                content.save()

            return JsonResponse({'post': {
                'id': post.id
            }}, status=201)
        except Exception as e:
            print('****************', e)
            return JsonResponse(Messages.BAD_REQUEST)  # 当发布失败是，需提醒用户，但提醒信息不宜过多，防止恶意猜测l


# 处理前端请求 csrftoken cookie 的视图
@user_login_required
@ensure_csrf_cookie  # 保证请求在到达处理视图前，先返回一个csrftoken cookie
def getToken(request: HttpRequest):
    print('csrf token')
    return HttpResponse()
