from .forms import LoginForm
from .models import User

from django.contrib import messages, auth
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect
from django.views.generic import FormView


def register_view(request):

    if request.method == 'POST':

        try:
            user_id = request.POST['user_id']
            user = User.objects.get(user_id=user_id)

        except Exception as e:
            User.objects.create_user(
                user_id = request.POST['user_id'],
                password= request.POST['password1'],
                email = request.POST.get('user_email'),
                hp = request.POST.get('hp'),
                business_name = request.POST.get('BusinessName'),
                business_add = '',
                business_regnum = request.POST.get('BusinessNumber'),
                region = '0',
            )
            return redirect('/')
        else:
            context = {'error' : '유저 아이디가 이미 존재합니다.'}
            return render(request, 'users/register.html', context)

    else:
        return render(request, 'users/register.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def ChageInfo(request):

    if request.method == 'POST':

        hp = request.POST['hp']
        email = request.POST['email']
        business_name = request.POST['business_name']
        business_add = request.POST['business_add']
        business_regnum = request.POST['business_regnum']

        user = request.user
        update_field = []

        user.hp = hp
        update_field.append('hp')
        user.email = email
        update_field.append('email')
        user.business_name = business_name
        update_field.append('business_name')
        user.business_add = business_add
        update_field.append('business_add')
        user.business_regnum = business_regnum
        update_field.append('business_regnum')

        user.save(update_fields=update_field)

        # password 수정 삭제
        # password = request.POST['password']
        # if password != '':
        #     user.set_password(password)
        #     user.save()
        #     update_session_auth_hash(request, request.user)


        return redirect('/changeInfo')

    else:
        if request.user.is_authenticated:
            user_info = User.objects.get(user_id = request.user)
            context = {
                'user_info': user_info
                }
            
            return render(request, 'users/changeinfo.html', context)

        else:
            return redirect('/')


class LoginView(FormView):
    '''
    View for the main page that handles login form requests.
    '''
    template_name = 'users/index.html'
    form_class = LoginForm
    success_url = '/list'

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=user_id, password=password)

        if user:
            self.request.session['user_id'] = user_id
            login(self.request, user)
            return super().form_valid(form)

    def form_invalid(self, form):
        '''
        Handles invalid form submissions by displaying an error message.
        '''
        messages.error(self.request, '아이디 또는 비밀번호를 확인해주세요.')
        return super().form_invalid(form)
