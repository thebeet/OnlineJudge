'''
Created on 2012-7-26

@author: TheBeet
'''
from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from JudgeWeb.problem.models import Problem

class UserManager(models.Manager):
    def rank(self):
        return UserProfile.objects.filter(is_active=True).order_by("-solved", "last_solve_time")

    def compare(self, user1, user2):
        pass

class UserProfile(User):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=256)
    reg_ip = models.GenericIPAddressField()
    login_ip = models.GenericIPAddressField()
    school = models.CharField(max_length=256, null = True, blank = True)
    institute = models.CharField(max_length=256, null = True, blank = True)
    department = models.CharField(max_length=256, null = True, blank = True)
    birthday = models.DateField(null = True, blank = True)
    gender = models.IntegerField(choices=((0, 'Male'), (1, 'FeMale'), (2, 'Other')))
    phone = models.CharField(max_length=256, null = True, blank = True)
    address = models.CharField(max_length=1024, null = True, blank = True)

    realname = models.CharField(max_length=256, null = True, blank = True)
    stu_no = models.CharField(max_length=256, null = True, blank = True)

    solved = models.IntegerField(default = 0)
    last_solve_time = models.DateTimeField(null = True)

    problems = models.ManyToManyField(Problem, through='UserProblem')

    objects = UserManager()

    def get_statistic(self):
        from JudgeWeb.solution.models import Solution
        from django.db.models import Count
        from JudgeWeb.common.result import result_full_tag, result_short_tag, result_tag_count

        self.problem_solved = Problem.objects.raw("select problem_id id, result from user_problem where user_id = %s and result=1 order by problem_id", [self.user_id,])
        self.problem_failed = Problem.objects.raw("select problem_id id, result from user_problem where user_id = %s and result<>1 order by problem_id", [self.user_id,])
        self.problem_all = Problem.objects.raw("select problem_id id, result from user_problem where user_id = %s order by problem_id", [self.user_id,])

        self.rank = UserProfile.objects.filter(solved__gt=self.solved)
        if (self.last_solve_time):
            self.rank.filter(last_solve_time__lt=self.last_solve_time)

        result_counts = Solution.objects.values("user").filter(user_id=self.user_id).values('result').annotate(result_count = Count('result')).order_by('result')
        self.statistic = {'all': 0}
        for i in range(result_tag_count):
            self.statistic[result_short_tag[i]] = 0
        for row in result_counts:
            self.statistic[result_short_tag[row['result']]] = row['result_count']
            self.statistic['all'] += row['result_count']

        return self.statistic

    def get_rank(self):
        rank = UserProfile.objects.filter(solved__gt=self.solved)
        if (self.last_solve_time):
            rank.filter(last_solve_time__lt=self.last_solve_time)
        return rank.count() + 1

    class Meta:
        db_table = u'user'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class UserProblem(models.Model):
    user = models.ForeignKey(UserProfile)
    problem = models.ForeignKey(Problem)

    result = models.IntegerField(null = True)
    collect = models.BooleanField(default=False)

    class Meta:
        db_table = u'user_problem'