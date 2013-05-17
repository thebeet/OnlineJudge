'''
Created on 2012-10-11

@author: linsy
'''

from django import forms
from django.forms import Form

class RegisterForm(Form):
    username = forms.CharField()
    nickname = forms.CharField()
    password = forms.PasswordInput()
    email = forms.EmailField()
    school = forms.CharField()
    stu_no = forms.CharField()
    realname = forms.CharField()
    birthday = forms.CharField()
    address = forms.CharField()
    phone = forms.CharField()