from django.db import models

from JudgeWeb.user.models import UserProfile
from JudgeWeb.problem.models import Problem
from JudgeWeb.solution.models import Solution

class CummunicateManager(models.Manager):
    def newSolution(self, user, solution):
        communicate = Communicate()
        communicate.user = user
        communicate.solution = solution
        communicate.operator = "judge"
        communicate.save()

    def rejudgeSolution(self, user, solution):
        communicate = Communicate()
        communicate.user = user
        communicate.solution = solution
        communicate.operator = "rejudge"
        communicate.save()

class Communicate(models.Model):
    user = models.ForeignKey(UserProfile)
    problem = models.ForeignKey(Problem, null=True)
    solution = models.ForeignKey(Solution, null=True)
    operator = models.CharField()
    status = models.IntegerField()

    update_time = models.DateTimeField(auto_now = True)
    create_time = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = u'communicate'