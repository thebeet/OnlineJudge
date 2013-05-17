'''
Created on 2012-9-1

@author: TheBeet
'''
from django.contrib import admin
from JudgeWeb.problem.models import Problem

class ProblemAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    list_display = ('id', 'title', 'create_time', 'defunct', )
    list_editable = ('defunct', )

admin.site.register(Problem, ProblemAdmin)