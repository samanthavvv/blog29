import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from post.models import Post, Content
ret = Post.objects.filter(id=1)
print(ret)