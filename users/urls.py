from django.urls import path
from .views import reg, userlogin, userindex, userlogout,get_captcha

# 要去掉前缀 /users ,已在全局路由配置中设置
urlpatterns = [
    path('', reg),  # 注册路由。 POST /users/  --》reg
    path('login/', userlogin),  # 登录路由。 POST /users/login  --》login
    path('index/', userindex),
    path('logout/', userlogout),
    path('getcaptcha/', get_captcha) # 验证码路由。 GET /users/getcaptcha --> get_captcha
]
