from django.apps import AppConfig


class BookConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "book"
    verbose_name = '后台相关' #settings要注册app为 BookConfig 不然用不了，在admin后台的名字
