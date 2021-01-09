# -*- coding: utf-8 -*-
# @Time       :   2021-01-06 18:09
# @Author     :   XrazYang
# @File       :   urls.py
# @Project    :   Enlifes


from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('qrcode/', views.qrcodeview, name="qrcodeview"),
    path('moredetails/', views.get_more_diary_info, name='moredetails'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('details/', views.DiaryDetails.as_view(), name="details"),
    path('create/', views.CreateDiary.as_view(), name="create_diary")
]
