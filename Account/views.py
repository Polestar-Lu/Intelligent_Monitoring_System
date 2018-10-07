from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import django.contrib.staticfiles
from MessageModel.models import WarningMessage


def log_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/account/function_select')
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'Account/log_in.html', {'form': form})
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/account/function_select')
            else:
                print('User not found')
        else:
            # If there were errors, we render the form with these errors
            return render(request, 'Account/log_in.html', {'form': form})


def sign_up(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/account/function_select')
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'Account/sign_up.html', {'form': form})
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#the-save-method
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/account/function_select')
        else:
            # If there were errors, we render the form with these errors
            print(form)
            return render(request, 'Account/sign_up.html', {'form': form})


def change_password(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            login(request, request.user)
            messages.success(request, 'Password successfully changed.')
            return HttpResponseRedirect('/account/login')
    else:
        form = PasswordChangeForm(user=request.user)

    for field in form.fields.values():
        field.help_text = None

    return render(request, 'Account/change_password.html', {
        'form': form
    })


def log_out(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')
    logout(request)
    return render(request, 'Account/log_out.html')


def function_select(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')
    context = {"message": ''}
    context['username'] = request.user.username
    if request.method == "POST":
        if request.POST['action'] == "account":
            if request.user.is_superuser:
                return HttpResponseRedirect('/account/account_list')
            else:
                context["message"] = "您没有进行此项操作的权限！"
                return render(request, 'Account/function_select.html', context)
    return render(request, 'Account/function_select.html', context)


def message_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')
    context = {}
    if request.method == "POST":
        msg = WarningMessage.objects.get(id=request.POST["delete_msg_ID"])
        msg.delete()
    msg_list = WarningMessage.objects.order_by('-create_date_time')
    for msg in msg_list:
        msg.create_date_time = msg.create_date_time.strftime('%Y-%m-%d %H:%M:%S')
    context["msg_list"] = msg_list
    return render(request, 'Account/message_list.html', context)


def account_list(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return HttpResponseRedirect('/account/login')
    context = {}
    if request.method == "POST":
        user = User.objects.get(id=request.POST["delete_user_ID"])
        user.delete()
    account__list = User.objects.order_by('-last_login')
    for account in account__list:
        account.date_joined = account.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        account.last_login = account.last_login.strftime('%Y-%m-%d %H:%M:%S')
        if account.is_superuser:
            account.is_superuser = "是"
        else:
            account.is_superuser = "否"
    context["account_list"] = account__list
    context["my_id"] = request.user.id
    return render(request, 'Account/account_list.html', context)
