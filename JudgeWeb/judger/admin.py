'''
Created on 2012-9-1

@author: TheBeet
'''
from django.contrib import admin
from JudgeWeb.judger.models import Judger

class JudgerAdmin(admin.ModelAdmin):
    search_fields = ('judger_name', )
    list_display = ('id', 'ip', 'port', 'judger_name', 'defunct', )
    list_editable = ('defunct', )

admin.site.register(Judger, JudgerAdmin)