from django.views.generic import View
from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout
from .models import Diary
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import qrcode
import json


def index(request):
    return render(request, "index.html")


def qrcodeview(request):
    data = "http://111.229.178.124"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save("./static/qrcode.png")
    return render(request, "qrcode.html", {"data": "通过二维码访问接口"})


@login_required(login_url='/login')
def get_more_diary_info(request):
    diary_content = {}
    if request.method == "GET":
        content = Diary.objects.all().filter(title=request.GET.get('title'))
        diary_content['title'] = content[0].title
        diary_content['time'] = content[0].create_time.strftime("%Y-%m-%d %H:%M:%S")
        diary_content['detail'] = content[0].detail

    data = json.dumps(diary_content)
    return HttpResponse(data, content_type="application/json")


class DiaryDetails(View):
    html_path = "details.html"

    @method_decorator(login_required, name="login")
    def get(self, request):
        username = request.user
        diary_titles = []

        details = Diary.objects.all().order_by('-create_time')[0:5]
        for diary in details:
            if diary.cdisry == username:
                diary_titles.append(diary.title)

        new_diary_title = '还没有东西的哦'
        new_diary_time = '还没有东西的哦'
        new_diary_detail = "还没有东西的哦"
        if len(diary_titles) > 0:
            new_diary_title = details[0].title
            new_diary_time = details[0].create_time
            new_diary_detail = details[0].detail

        return render(request, self.html_path,
                      {"username": username, "diary_list": diary_titles, "new_diary_title": new_diary_title,
                       "new_diary_time": new_diary_time, "new_diary_detail": new_diary_detail})


class CreateDiary(View):
    html_path = "create_diary.html"

    @method_decorator(login_required, name="login")
    def get(self, request):
        return render(request, self.html_path, {'username': request.user})

    def post(self, request):
        title = request.POST.get('title')
        detail = request.POST.get("detail")
        if not title or not detail:
            return render(request, self.html_path, {"username": request.user, "error": "标题或者内容不能为空！"})
        Diary.objects.create(title=title, detail=detail, cdisry=request.user)
        return redirect(reverse('details'))


class RegisterView(View):
    html_path = "register.html"

    def get(self, request):
        return render(request, self.html_path, {})

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, self.html_path, {"error": form.non_field_errors})

        return redirect(reverse("login"))


class LoginView(View):
    html_path = "login.html"

    def get(self, request):

        # 验证是否登录
        if request.user.is_authenticated:
            return redirect(reverse("login"))

        data = {}
        next_return = request.GET.get("next", "")
        data["next"] = next_return
        return render(request, self.html_path, data)

    def post(self, request):
        form = LoginForm(request.POST)

        if not form.is_valid():
            return render(request, self.html_path, {"error": form.non_field_errors()})

        user = form.cleaned_data.get("user")
        if user:
            login(request=request, user=user)

        next_return = request.POST.get("next_return")
        if next_return:
            return redirect(next_return)

        return redirect(reverse("details"))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("index"))
