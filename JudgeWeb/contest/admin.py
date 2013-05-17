'''
Created on 2012-9-1

@author: TheBeet
'''
from django.contrib import admin
from JudgeWeb.contest.models import Contest

class ContestAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type']

admin.site.register(Contest, ContestAdmin)