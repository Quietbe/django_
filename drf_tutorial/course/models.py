from django.db import models

# Create your models here.
"""
1.定义模型类
2.模型迁移
   2.1 先生成迁移文件（不会在数据库中生成表，只会创建一个 数据表和模型的对应关系）
        python manage.py makemigrations
   2.2 再迁移（会在数据库中生成表)
        python manage.py migrate
"""

class BookInfo(models.Model):

    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class PeopleInfo(models.Model):

    name = models.CharField(max_length=10)
    #性别
    ggender = models.BooleanField()
    #外键  on_delete
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE)