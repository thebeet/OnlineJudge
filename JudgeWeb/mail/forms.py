'''
Created on 2012-9-7

@author: Macro
'''
from django import forms
from django.forms import Form
from models import Mail

class SubmitMailForm(Form):
    mail_id = forms.IntegerField()
    title = forms.CharField(max_length = 256)
    content = forms.TextInput()
    
    class Meta:
        models = Mail
        fields = {'title', 'content'}