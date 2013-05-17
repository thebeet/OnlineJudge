'''
Created on 2012-8-11

@author: TheBeet
'''
from JudgeWeb.solution.models import Solution
from JudgeWeb.problem.models import Problem
from django.core import serializers

class Judge(object):

    def __init__(self):
        pass

    def judge(self, id):
        solution = Solution.objects.select_related().filter(sid=id);
        print serializers.serialize("json", solution)

a = Judge();
a.judge(111113)