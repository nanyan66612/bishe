from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    teacher_code = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username','email','password1','password2','role']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isdigit() or len(username)!=10:
            raise forms.ValidationError("必须10位数字")
        return username

    def clean_password1(self):
        pwd = self.cleaned_data.get('password1')
        import re
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{15}$', pwd):
            raise forms.ValidationError("15位，大小写+数字+符号")
        return pwd

    def clean(self):
        role = self.cleaned_data.get('role')
        code = self.cleaned_data.get('teacher_code')
        if role == 'teacher' and code != 'ADMIN_TEACHER_2025':
            raise forms.ValidationError("教师码错误")
        return self.cleaned_data