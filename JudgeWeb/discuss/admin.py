'''
Created on 2012-9-1

@author: TheBeet
'''
from django.contrib import admin
from JudgeWeb.discuss.models import Discuss

class DiscussAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    list_display = ('id', 'title', 'problem', 'user', 'defunct')
    list_editable = ('defunct', )

admin.site.register(Discuss, DiscussAdmin)