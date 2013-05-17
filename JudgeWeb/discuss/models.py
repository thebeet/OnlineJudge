'''
Created on 2012-9-1

@author: Macro
'''
from django.db import models
from JudgeWeb.user.models import UserProfile
from JudgeWeb.problem.models import Problem

class DiscussManager(models.Manager):
    def list(self, problem=None):
        queryset = Discuss.objects.filter(defunct=False).filter(reply_id=0)
        if (problem):
            queryset = queryset.filter(problem=problem)
        return queryset.order_by("-last_reply_time")

    def topic(self, discuss_id):
        return (Discuss.objects.filter(id=discuss_id) | Discuss.objects.filter(reply_id=discuss_id)).filter(defunct=False).order_by("id")

class Discuss(models.Model):
    problem = models.ForeignKey(Problem, null = True)
    reply_id = models.IntegerField() #not null for index
    user = models.ForeignKey(UserProfile)

    title = models.TextField(max_length = 255)
    content = models.TextField(blank = True)
    create_time = models.DateTimeField(auto_now_add = True)
    edit_time = models.DateTimeField(auto_now = True)

    reply_num = models.IntegerField()
    view_num = models.IntegerField()
    last_reply_user = models.ForeignKey(UserProfile, null=True, related_name="last_reply")
    last_reply_time = models.DateTimeField(auto_now=True)

    defunct = models.BooleanField(default = False)

    objects = DiscussManager()

    class Meta:
        db_table = u'discuss'
        ordering = ['-id']