from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.practice_list, name='practice_list'),
    path('detail/<int:qid>/', views.practice_detail, name='practice_detail'),
    path('wrong/', views.wrong_list, name='wrong_list'),
]