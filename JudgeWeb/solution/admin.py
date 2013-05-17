'''
Created on 2012-9-1

@author: TheBeet
'''
from django.contrib import admin
from JudgeWeb.solution.models import Solution

class SolutionAdmin(admin.ModelAdmin):
    search_fields = ['id', 'problem', 'user', 'result', 'contest']
    list_display = ['id', 'problem', 'user', 'result', 'contest']

admin.site.register(Solution, SolutionAdmin)