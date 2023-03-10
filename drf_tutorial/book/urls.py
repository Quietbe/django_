from django.urls import path
from book import views

urlpatterns = [

    path('index/', views.index),

]