'''
Created on 2012-9-7

@author: Macro
'''


from django.views.generic import DetailView, ListView, FormView

from models import Mail
from forms import SubmitMailForm
from django.http import HttpResponseRedirect
from JudgeWeb.user.models import UserProfile
from datetime import datetime
from django.contrib.auth.models import User

class MailInboxView(ListView, FormView):
    model = Mail
    template_name = 'mail/inbox.html'
    paginate_by = 20

    def get_queryset(self):
        return Mail.objects.inbox(self.request.user.id)

    def post(self, request, *args, **kwargs):
        receiverId = User.objects.get_by_natural_key(request.POST['receiver']).userprofile

        mail = Mail()
        mail.from_user = self.request.user.userprofile
        mail.to_user = receiverId
        mail.title = request.POST['title']
        mail.content = request.POST['content']
        mail.create_time = datetime.now()
        mail.view = 1
        mail.save()
        return HttpResponseRedirect('.')


class MailOutboxView(ListView, FormView):
    model = Mail
    template_name = 'mail/outbox.html'
    paginate_by = 20

    def get_queryset(self):
        return Mail.objects.outbox(self.request.user.id)

    def post(self, request, *args, **kwargs):
            receiverId = User.objects.get_by_natural_key(request.POST['receiver']).userprofile

            mail = Mail()
            mail.from_user = self.request.user.userprofile
            mail.to_user = receiverId
            mail.title = request.POST['title']
            mail.content = request.POST['content']
            mail.create_time = datetime.now()
            mail.view = 0
            mail.save()
            return HttpResponseRedirect('.')

class MailDetialView(DetailView, FormView):
    model = Mail
    template_name = 'mail/detail.html'

    def get(self, request, *args, **kwargs):
        mail = Mail.objects.get(id=kwargs['pk'])
        if self.request.user.userprofile == mail.to_user:
            mail.view = 1
        mail.save()
        return super(MailDetialView, self).get(request, *args, **kwargs)

class MailChatView(ListView):
    model = Mail
    template_name = 'mail/chat.html'
    paginate_by = 20
    def get_queryset(self):
        to_user = UserProfile.objects.get(username=self.kwargs.get("user"))
        return Mail.objects.chat(self.request.user.id, to_user.id)
