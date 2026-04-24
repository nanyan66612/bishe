from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.question_manage, name='question_manage'),
    path('add/', views.question_add, name='question_add'),
]