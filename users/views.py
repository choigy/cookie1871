from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from users.forms import SignUpForm, LoginForm
from users.models import User
from django.contrib.auth import authenticate,login, logout
import bcrypt
# Create your views here.


def home(request):
    return render(request, 'base.html')

class LoginView(View):
    def get(self, request):
        if request.COOKIES.get('username'):
            username=request.COOKIES.get('username')
            password=request.COOKIES.get('password')
            user=authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('users:home'))
        else:
            form=LoginForm()
            return render(request, 'users/form.html', {'form':form})
    
    def post(self, request):
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            print(email)
            password=form.cleaned_data.get('password')
            print(password)
            user=User.objects.get(email=email)
            print(user)
            user.verify_email()
            if user:
                login(request, user)
                response=render(request, 'home.html')
                response.set_cookie('username', email)
                response.set_cookie('password', password)
                return response
        return render(request, 'users/form.html', {'form':form})
        
    

class SignupView(View):
    def get(self, request):
        form=SignUpForm(request.GET)
        return render(request, 'users/signup.html', {'form':form})
    
    def post(self, request):
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user=authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
            user.verify_email()
            return redirect(reverse('users:home'))
        return render(request, 'users/signup.html', {'form':form})
    

def confirm_mail(request):
    key=request.GET.get('key')
    try:
        user=User.objects.get(email_key=key)
        user.email_confirmed=True
        user.email_key=""
        user.save()
    except User.DoesNotExist:
        return redirect(reverse('home'))
        
    
    
    
class ProfileView(View):
    def get(self,request,pk):
        user=User.objects.get(pk=pk)
        print(pk)
        print(user)
        return render(request, 'users/profile.html', {'user':user})


class Update(View):
    pass


def log_out(request):
    response=render(request, 'base.html')
    response.delete_cookie('username')
    response.delete_cookie('password')
    logout(request)
    return response