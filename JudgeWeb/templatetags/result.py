'''
Created on 2012-7-29

@author: TheBeet
'''

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

def result(value):
    from JudgeWeb.common.result import result_short_tag, result_full_tag
    return mark_safe("<span class='" + result_short_tag[value] + "'>" + result_full_tag[value] + "</span>")


register.filter('result', result)