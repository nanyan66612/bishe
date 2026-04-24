from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from practice.models import Submit
import pandas as pd

def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'

def dashboard(request):
    s = Submit.objects.all()
    data = pd.DataFrame(list(s.values('result')))
    total = len(data)
    ac = len(data[data['result']=='AC']) if total else 0
    return render(request,'dashboard.html',{'total':total,'ac':ac})