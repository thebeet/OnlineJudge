'''
Created on 2012-8-28

@author: TheBeet
'''

from django.views.generic import ListView

class JSONListView(ListView):
    def get(self, request, *args, **kwargs):
        if (request.is_ajax()):
