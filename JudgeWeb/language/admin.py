'''
Created on 2012-9-1

@author: TheBeet
'''
from django.contrib import admin
from JudgeWeb.language.models import Language

class LanguageAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'defunct', )
    list_editable = ('defunct', )

admin.site.register(Language, LanguageAdmin)