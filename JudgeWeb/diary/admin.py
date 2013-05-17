'''
Created on 2012-9-1

@author: TheBeet
'''
from django.contrib import admin
from JudgeWeb.diary.models import Diary

class DiaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'create_time']

admin.site.register(Diary, DiaryAdmin)