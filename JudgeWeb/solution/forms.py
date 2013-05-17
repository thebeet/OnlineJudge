'''
Created on 2012-7-26

@author: TheBeet
'''
from django import forms
from django.forms import Form
from models import Solution

class SubmitSolutionForm(Form):
    pid = forms.IntegerField()
    source_code = forms.Field(widget = forms.Textarea())