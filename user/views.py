from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import SendEmailForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.core.mail import send_mail


def index(request):
    return render(request, 'index.html')

def send_email(request):
    sent = False
    user = get_user_model()
    user = user.objects.all()
    if request.method == 'POST':
        form = SendEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = cd['subject']
            message = cd['message']
            send_mail(subject, message,'admin@myblog.com', user, )
            sent = True
    else:
        form = SendEmailForm()
    return render(request, 'admin/user/send_email.html', {'user': user, 'form':form, 'sent':sent})