from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Question
from .forms import QuestionForm

def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'

def question_manage(request):
    qs = Question.objects.all()
    return render(request,'question_manage.html',{'qs':qs})

def question_add(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_manage')
    else:
        form = QuestionForm()
    return render(request,'question_add.html',{'form':form})