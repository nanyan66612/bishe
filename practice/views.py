from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from questions.models import Question
from .models import Submit, WrongQuestion
from judge.judger import run_c_code

@login_required
def practice_list(request):
    qs = Question.objects.all()
    return render(request,'practice_list.html',{'qs':qs})

@login_required
def practice_detail(request,qid):
    q = get_object_or_404(Question,id=qid)
    if request.method == 'POST':
        code = request.POST.get('code')
        res = run_c_code(code, q.test_input, q.test_output)
        Submit.objects.create(user=request.user,question=q,code=code,result=res)
        if res != 'AC':
            WrongQuestion.objects.get_or_create(user=request.user,question=q)
        return render(request,'result.html',{'result':res,'q':q})
    return render(request,'editor.html',{'q':q})

@login_required
def wrong_list(request):
    wrongs = WrongQuestion.objects.filter(user=request.user)
    return render(request,'wrong_list.html',{'wrongs':wrongs})