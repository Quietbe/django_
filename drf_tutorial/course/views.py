from django.shortcuts import render, HttpResponse
# from django.http import HttpRequest, HttpResponse

# Create your views here.
"""
视图
1.就是python函数
2.函数的第一个参数就是请求  和请求相关的 它是 HttpRequest的实例对象
3.必须放回一个相应   
"""

def index(request):

    return HttpResponse('index')
