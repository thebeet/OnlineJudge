'''
Created on 2012-9-7

@author: Macro
'''

from django.db import models

from JudgeWeb.user.models import UserProfile

class MailManager(models.Manager):
    def new(self, user):
        return Mail.objects.inbox(user).filter(view=False)

    def inbox(self, user):
        return Mail.objects.filter(defunct=False).filter(to_user_id=user).order_by('-id')

    def outbox(self, user):
        return Mail.objects.filter(defunct=False).filter(from_user_id=user).order_by('-id')

    def chat(self, user_me, user_other):
        return (Mail.objects.filter(from_user_id=user_me).filter(to_user_id=user_other) |
                Mail.objects.filter(to_user_id=user_me).filter(from_user_id=user_other)).filter(defunct=False).order_by('-id')


class Mail(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name="mail_from")
    to_user = models.ForeignKey(UserProfile, related_name="mail_to")
    title = models.CharField(max_length = 256)
    content = models.TextField(blank = True)
    create_time = models.DateTimeField()
    view = models.BooleanField(default = False)

    defunct = models.BooleanField(default = False)

    objects = MailManager()

    class Meta:
        db_table = u'mail'

