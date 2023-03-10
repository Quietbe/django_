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

"""
书籍表：
    id,name,pub_data,readcount,commentcount,is_delete
    名字，发布日期，阅读量，点评论量，是否删除
"""
class BookInfo(models.Model):

    name = models.CharField(max_length=20, unique=True, verbose_name='名字')#长度， 唯一， 后台名字
    #发布日期
    pub_data = models.DateField(null=True)  #允许为空
    #阅读量
    readcount = models.IntegerField(default=0)
    #评论量
    commentcount = models.IntegerField(default=0)
    #是否删除
    is_delete = models.BooleanField(default=False)

    #修改默认表名
    class Meta:
        db_table = 'bookinfo'
        #修改后台admin的显示信息的配置
        verbose_name = '书籍表'

    # 后台返回属性
    def __str__(self):
        return self.name

# 人物列表信息模型类
class PeopleInfo(models.Model):

    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    name = models.CharField(max_length=20, verbose_name='姓名')
    # 性别
    ggender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    description = models.CharField(max_length=200, null=True, verbose_name='功法')
    # 外键 on_delete 关联数据关系，是否同时删除，CASCADE同时删除
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='书名')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'peopleinfo'
        verbose_name = '人物信息'

    def __str__(self):

        return self.name
