# -*- coding: utf-8 -*-
# @Time       :   2021-01-07 17:09
# @Author     :   XrazYang
# @File       :   forms.py
# @Project    :   Enlifes

from django.forms import forms, CharField, TextInput, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegisterForm(forms.Form):
    username = CharField(widget=TextInput)
    password = CharField(widget=PasswordInput)
    check_password = CharField(widget=PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        check_password = self.cleaned_data.get("check_password")

        if not username:
            raise forms.ValidationError("用户名不能为空！")

        if not password:
            raise forms.ValidationError("密码不能为空！")

        if password != check_password:
            raise forms.ValidationError("两次输入密码不一致！")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名{}已经存在".format(username))

        User.objects.create_user(username=username, password=password)  # 存入数据库

        return self.cleaned_data


class LoginForm(forms.Form):
    username = CharField(widget=TextInput)
    password = CharField(widget=PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if not username:
            raise forms.ValidationError("用户名不能为空！")

        if not password:
            raise forms.ValidationError("密码不能为空！")

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名不存在！")

        user = authenticate(username=username, password=password)

        if not user:
            raise forms.ValidationError("登录失败！")

        self.cleaned_data["user"] = user

        return self.cleaned_data
