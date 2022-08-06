from django import forms
from users.models import User
from hashlib import sha1, md5
import bcrypt
import random
import os

class SignUpForm(forms.Form):
    first_name=forms.CharField()
    last_name=forms.CharField()
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    password1=forms.CharField(widget=forms.PasswordInput)
    
    def clean_email(self):
        email=self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise forms.ValidationError('email exist')
        except User.DoesNotExist:
            return email
    
    def clean_password1(self):
        password=self.cleaned_data.get('password')
        password1=self.cleaned_data.get('password1')
        if password==password1:
            return password
        else:
            raise forms.ValidationError('wrong password')
    
    
    def save(self):
        first_name=self.cleaned_data.get('first_name')
        last_name=self.cleaned_data.get('last_name')
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        salt=md5(os.urandom(128)).hexdigest()
        encode_salt=salt.encode('utf-8')
        print(salt)
        t1=password
        t1=sha1(t1.encode('utf-8')).hexdigest()
        print(t1)
        for i in range(30):
            t1=sha1(encode_salt+t1.encode('utf-8')).hexdigest()
        print(t1)
        decode_pass=t1
        print(decode_pass)
        user=User.objects.create(username=email, email=email)
        print(user)
        user.password=decode_pass
        user.first_name=first_name
        user.last_name=last_name
        user.salt=salt
        user.save()
        

        
class LoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)
    
    
    def clean(self):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        try:
            user=User.objects.get(username=email)
            salt=user.salt.encode('utf-8')
            encode_pass=user.password.encode('utf-8')
            t1=password
            t1=sha1(t1.encode('utf-8')).hexdigest()
            for i in range(30):
                t1=sha1(salt+t1.encode('utf-8')).hexdigest()
            print(t1)
            print(password.encode('utf-8'))
            print(user.password.encode('utf-8'))
            if encode_pass==t1.encode('utf-8'):
                return self.cleaned_data
            else:
                raise forms.ValidationError('password is not correct')
        except User.DoesNotExist:
            raise forms.ValidationError('user does not exist')
        