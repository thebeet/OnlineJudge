'''
Created on 2012-9-1

@author: Macro
'''
from django.views.generic import DetailView, ListView, FormView

from models import Discuss
from JudgeWeb.problem.models import Problem
from forms import SubmitDiscussForm
from django.template import Context, Template
from django import template
from django.http import HttpResponseRedirect

class DiscussListView(ListView):
    paginate_by = 20
    template_name = 'discuss/list.html'
    model = Discuss
    def get_queryset(self):
        return Discuss.objects.list(self.kwargs.get('problem'))

    def post(self, request, *args, **kwargs):
        discuss = Discuss()
        discuss.problem = kwargs['problem']
        discuss.reply_id = 0
        discuss.user = request.user.id
        discuss.title = request.POST['title']
        discuss.content = request.POST['content']
        discuss.defunct = False
        discuss.save();
        return HttpResponseRedirect('.')

class DiscussDetailView(ListView, FormView):
    template_name = 'discuss/detail.html'
    model = Discuss
    form_class = SubmitDiscussForm
    discuss_id = 0

    def get_queryset(self):
        return Discuss.objects.topic(self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        template.Context({"discuss_id" : kwargs['pk']})
        return super(DiscussDetailView, self).get(request, *args, **kwargs)
        '''return self.render_to_response(self.get_context_data(form=form, pid=self.kwargs["pk"]))'''

    def get_initial(self):
        if (self.discuss_id != 0):
            return {"discuss_id": self.discuss_id}
        else:
            return self.initial.copy()

    def post(self, request, *args, **kwargs):
        self.discuss_id = kwargs['pk']
        firstDiscuss = Discuss.objects.get(discuss_id=kwargs['pk'])
        discuss = Discuss()
        discuss.pid = firstDiscuss.pid
        discuss.reply_id = firstDiscuss.discuss_id
        discuss.uid = request.user.id
        discuss.username = request.user.username
        discuss.title = request.POST['title']
        discuss.content = request.POST['content']
        discuss.reply_num = 0
        discuss.view_num = 0
        discuss.defunct = 0
        discuss.top = 0
        discuss.save();
        return HttpResponseRedirect('.')



