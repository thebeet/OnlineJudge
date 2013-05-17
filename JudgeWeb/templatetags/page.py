'''
Created on 2012-9-24

@author: TheBeet
'''
from django import template

register = template.Library()

def page(value, arg):
    getcopy = value.copy()
    getcopy["page"] = arg
    return getcopy.urlencode()


register.filter('page', page)