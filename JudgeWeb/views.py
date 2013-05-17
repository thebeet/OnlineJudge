'''
Created on 2012-7-26

@author: TheBeet
'''

from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"