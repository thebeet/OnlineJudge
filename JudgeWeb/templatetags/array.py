'''
Created on 2012-9-15

@author: TheBeet
'''
from django import template

register = template.Library()

def array(value, arg):
    return value[arg]


register.filter('array', array)