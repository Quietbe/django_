from django.urls import path
from course import views

urlpatterns = [

    path('index/', views.index),

]