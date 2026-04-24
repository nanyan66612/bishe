from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, TeacherCode
import re


def index(request):
    return render(request, 'login.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # 禁止管理员在学生/教师端登录
        try:
            user = User.objects.get(username=username)
            if user.is_superuser:
                messages.error(request, "管理员请使用右上角【管理员登录】入口！")
                return redirect('index')
        except User.DoesNotExist:
            pass

        # 正常学生/教师登录
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile = UserProfile.objects.get(user=user)
            if profile.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, "用户名或密码错误")
    return redirect('index')


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")
        teacher_code = request.POST.get("teacher_code", "")

        # 用户名校验：10位数字
        if not re.fullmatch(r"\d{10}", username):
            messages.error(request, "用户名必须是10位数字")
            return redirect('register')

        # 密码校验：15位，含大小写、数字、特殊符号
        if len(password) > 14 or not (
                re.search(r"[A-Z]", password) and
                re.search(r"[a-z]", password) and
                re.search(r"[0-9]", password) and
                re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
        ):
            messages.error(request, "密码必须15位以下，包含大小写、数字和特殊符号")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "两次密码不一致")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "用户名已存在")
            return redirect('register')

        # 教师码校验
        if role == "teacher":
            code_obj = TeacherCode.objects.filter(code=teacher_code, is_used=False).first()
            if not code_obj:
                messages.error(request, "教师码无效或已被使用")
                return redirect('register')
            code_obj.is_used = True
            code_obj.save()

        # 写入数据库
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, role=role)
        messages.success(request, "注册成功，请登录")
        return redirect('register')

    return render(request, 'register.html')


def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 安全认证：只允许超级管理员登录后台
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('/admin/')

        messages.error(request, "管理员账号或密码错误")
    return render(request, 'admin/login.html')


@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')


@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')


def user_logout(request):
    logout(request)
    return redirect('index')