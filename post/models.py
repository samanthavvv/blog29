from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):   # id 主键，title，postdate，author 外键：表post
    class Meta:  # 定义表名
        db_table = "post"

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=128, null=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=False)  # 关联的属性是 author，查询时的字段是 author_id
    postdate = models.DateTimeField(null=False)

    def __repr__(self):
        return "<Post: {}, {}, {}>".format(
            self.title,
            self.author_id,
            self.postdate
        )

    __str__ = __repr__


class Content(models.Model):    # post 外键、主键，content：表content
    class Meta:  # 定义表名
        db_table = "content"

    # 字段映射
    post = models.OneToOneField(Post, on_delete=models.PROTECT, primary_key=True)
    content = models.TextField(max_length=255, default="请编写博客", null=True)

    def __repr__(self):
        return "<content: {}, {}>".format(
            self.pk,
            self.content[:20]
        )

    __str__ = __repr__
