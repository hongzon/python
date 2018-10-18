from django.shortcuts import render,redirect
from django.urls import reverse
def showMessage(request, msg ,url = '', time = 2, ):
    if url == '':
        url = request.META['HTTP_REFERER']
    return render(request, 'message.html', {'second': time, 'url': url,'msg':msg})