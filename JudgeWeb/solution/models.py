'''
Created on 2012-7-27

@author: TheBeet
'''
from django.db import models

from JudgeWeb.problem.models import Problem
from JudgeWeb.user.models import UserProfile
from JudgeWeb.language.models import Language
from JudgeWeb.judger.models import Judger
from JudgeWeb.contest.models import Contest

class SolutionManager(models.Manager):
    def best(self, problem, num=10):
        return Solution.objects.raw("select user_id, id, problem_id, language_id, result, source_code from solution where problem_id=%s and result=1 group by user_id order by run_time, memory, id limit %s", [problem, num, ])

    def contest(self, contest):
        return Solution.objects.filter(countst=contest)

class Solution(models.Model):
    user = models.ForeignKey(UserProfile)
    problem = models.ForeignKey(Problem)
    language = models.ForeignKey(Language)
    contest = models.ForeignKey(Contest, null = True)
    submit_time = models.DateTimeField(auto_now_add = True)

    result = models.IntegerField()
    run_time = models.IntegerField(null = True, blank = True)
    memory = models.IntegerField(null = True, blank = True)
    source_code = models.TextField()
    result_detail = models.TextField(null = True, blank = True)

    judger = models.ForeignKey(Judger, null = True)

    objects = SolutionManager()

    class Meta:
        db_table = u'solution'
        ordering = ['-id']
