'''
Created on 2012-9-3

@author: Macro
'''

from django import forms
from django.forms import Form
from models import Discuss

class SubmitDiscussForm(Form):
    id = forms.IntegerField()
    title = forms.CharField(max_length = 255)
    content = forms.CharField()

    class Meta:
        models = Discuss
        fields = {'title', 'content'}