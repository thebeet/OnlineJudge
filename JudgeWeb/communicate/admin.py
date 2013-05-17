'''
Created on 2012-9-1

@author: TheBeet
'''
from django.contrib import admin
from JudgeWeb.communicate.models import Communicate

class CommunicateAdmin(admin.ModelAdmin):
    list_display = ['id', 'create_time']

admin.site.register(Communicate, CommunicateAdmin)