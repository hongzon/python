from django.shortcuts import render,redirect
from .models import Subject,Teacher,User,proto
from django.http import HttpResponse
import json
from django.urls import reverse
from .forms import UserForm
from django.forms.models import model_to_dict
# Create your views here.

def logout(requset):
    if 'user' in requset.session:
        del requset.session['user']
    return redirect(reverse('login'))
def login(request):
    if request.method.lower() == 'get':
        return render(request, 'demo/login.html')
    else:
        username = request.POST['username'];
        try:
            user = User.objects.get(username__exact=username)
            password =  request.POST['password']
            hasher = proto.copy()
            hasher.update(password.encode('utf-8'))
            if hasher.hexdigest() == user.password:
                request.session['user'] = model_to_dict(user)
                return redirect(reverse('sub'))
        except User.DoesNotExist:
            pass
        return render(request, 'demo/login.html', {'hint': '用户名或密码错误'})
def show_subjects(request):
    if 'user' in request.session and request.session['user']:
        ctx = {'subject_list':Subject.objects.all()}
        return render(request, 'demo/subject.html', ctx)
    else:
        return render(request, 'demo/login.html', {'hint': '用户名或密码错误'})
def show_teachers(request, no):
    if 'user' in request.session and request.session['user']:
        teachers = Teacher.objects.select_related('subject').filter(subject__no =  no)
        ctx = {'teachers_list':teachers}

    #print(teachers.query)
        return render(request,'demo/teacher.html',ctx)
    else:
        return render(request, 'demo/login.html', {'hint': '用户名或密码错误'})
def register(request):
    form = UserForm()
    if request.method.lower() == 'get':
        return render(request, 'demo/register.html', {'f': form})
    else:
        ctx = {}
        try:
            form = UserForm(request.POST)
            print(form.errors)
            ctx['f'] = form
            if form.is_valid():
                form.save(commit=True)
                ctx['hint'] = '注册成功请登录!'
                return render(request, 'demo/login.html', ctx)
        except:
            ctx['hint'] = '注册失败, 请重新尝试!'
    return render(request, 'demo/register.html', ctx)
def make_comment(request, no):
    ctx = {'code': 200}
    if 'user' in request.session and request.session['user']:
        user = request.session['user']
        print(user)
        if user['counter'] > 0:
            try:
                teacher = Teacher.objects.get(pk=no)
                if request.path.startswith('/good'):
                    teacher.good_count += 1
                    ctx['result'] = f'好评({teacher.gcount})'
                else:
                    teacher.bad_count += 1
                    ctx['result'] = f'差评({teacher.bcount})'
                teacher.save()
                user['counter'] -= 1
                User.objects.filter(username__exact=user['username'])\
                    .update(counter=user['counter'])
                request.session['user'] = user
            except Teacher.DoesNotExist:
                ctx['code'] = 404
        else:
            ctx['code'] = 403
            ctx['result'] = '票数不足'
    else:
        ctx['code'] = 302
        ctx['result'] = '请先登录'
    return HttpResponse(json.dumps(ctx),
                        content_type='application/json; charset=utf-8')
def check_username(request):
    ctx = {}
    if 'username' in request.GET:
        username = request.GET['username']
        print(username)
        if not username:
            ctx['valid'] = False
        else:
            try:
                User.objects.get(username__exact=username)
                ctx['valid'] = False
            except User.DoesNotExist:
                ctx['valid'] = True
    return HttpResponse(json.dumps(ctx),
                        content_type='application/json; charset=utf-8')
