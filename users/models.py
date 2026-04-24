from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', '学生'),
        ('teacher', '教师'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class TeacherCode(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="教师注册码")
    is_used = models.BooleanField(default=False, verbose_name="是否已使用")

    class Meta:
        verbose_name = "教师注册码"
        verbose_name_plural = "教师注册码"

    def __str__(self):
        return self.code