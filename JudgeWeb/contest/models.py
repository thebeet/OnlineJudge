'''
Created on 2012-8-11

@author: TheBeet
'''
from django.db import models

from JudgeWeb.problem.models import Problem
from JudgeWeb.user.models import UserProfile
from django.db import connection

import datetime

class ContestManager(models.Manager):
    def now(self):
        return Contest.objects.filter(defunct=False).filter(start_time__lt=datetime.datetime.now()).filter(end_time__gt=datetime.datetime.now())

    def past(self):
        return Contest.objects.filter(defunct=False).filter(end_time__lt=datetime.datetime.now())

    def scheduled(self):
        return Contest.objects.filter(defunct=False).filter(start_time__gt=datetime.datetime.now())

    def rank(self, contest):
        contest_problems = list(ContestProblem.objects.filter(contest_id = contest.id));
        #contest['problems_num'] = len(contest_problems);
        problems_num = len(contest_problems);
        sql_prob_info = "";
        title_range = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        idx = 0;
        for problem in contest_problems:
            sql_prob_info += "sum(if(problem_id = " + str(problem.problem_id) + ", total_solve_time, 0)) as " + title_range[idx] + ", "
            sql_prob_info += "sum(if(problem_id = " + str(problem.problem_id) + ", err_time, 0)) as " + title_range[idx] + "_err, "
            idx = idx + 1
        sql_full = "select user_id, count(*) as ac_num," + sql_prob_info + "sum(total_solve_time) as all_time_penatly " + "from (select user_id, result, problem_id, ROUND(penatly / 1200) as err_time, solve_time, (penatly + TIME_TO_SEC(timediff(solve_time, %s))) as total_solve_time from contest_user_problem where contest_id = %s group by user_id , problem_id) as prob_rank where result = 1 group by user_id order by ac_num DESC;"
        #user_rank_queryset = UserProfile.objects.raw(sql_full, [contest.start_time, str(contest.id)])
        cursor = connection.cursor()
        cursor.execute(sql_full, [contest.start_time, str(contest.id)])
        desc = cursor.description
        reslist =  [dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()]
        user_rank_list = list()
        for user_info in reslist:
            user_dict = dict()
            user_dict["username"] = UserProfile.objects.filter(id = user_info["user_id"])[0].username
            user_dict["ac_num"] = user_info["ac_num"]
            user_dict["all_time_penatly"] = user_info["all_time_penatly"]
            problem_info_list = list()
            for i in range(problems_num):
                use_time = str(datetime.timedelta(seconds=int(user_info[title_range[i]])))
                err_time = str(user_info[title_range[i] + '_err'])
                if err_time == '0':
                    problem_info_list.append(use_time)
                else:
                    problem_info_list.append(use_time + '(' + err_time + ')')
            user_dict["problem_info_list"] = problem_info_list
            user_rank_list.append(user_dict)
        return user_rank_list



class Contest(models.Model):
    title = models.CharField(max_length = 765)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    type = models.IntegerField()
    objects = ContestManager()
    problems = models.ManyToManyField(Problem, through = 'ContestProblem')

    defunct = models.BooleanField(default = False)

    def status(self):
        now = datetime.datetime.now().__str__()
        if (now > self.end_time.__str__()):
            self.status = "end"
        elif (now < self.start_time.__str__()):
            self.status = "scheduled"
        else:
            self.status = "running"
        return self.status

    def get_problems(self, user=None):
        if user and user.is_authenticated():
            self.get_problems = list(Problem.objects.raw("""select user_status, id, title, CHAR(64 + display_order) display_order, t2.solved solved from problem
                                                         inner join (select display_order, problem_id id from contest_problem
                                                                     where contest_id = %s) as t using(id)
                                                         left join (select problem_id id, count(*) solved from contest_user_problem
                                                                     where contest_id = %s and result=1 group by problem_id) as t2 using(id)
                                                         left join (select problem_id id, result user_status from contest_user_problem where contest_id = %s and user_id = %s) as t3 using(id)
                                                        order by t.display_order""",
                                                      [self.id, self.id, self.id, user.id]))
        else:
            self.get_problems = list(Problem.objects.raw("""select id, title, CHAR(64 + display_order) display_order, if(t2.solved=null, 0, t2.solved) solved from problem
                                                         inner join (select display_order, problem_id id from contest_problem
                                                                     where contest_id = %s) as t using(id)
                                                         left join (select problem_id id, count(*) solved from contest_user_problem
                                                                     where contest_id = %s and result=1 group by problem_id) as t2 using(id)
                                                        order by t.display_order""",
                                                      [self.id, self.id]))
        return self.get_problems

    def statistic(self):
        self.statistic = self.get_problems()
        for problem in self.statistic:
            problem.get_statistic_with_contest(self.id)
        return self.statistic

    class Meta:
        db_table = u'contest'
        ordering = ['-start_time']

class UserContestProblem(models.Model):
    contest = models.ForeignKey(Contest)
    problem = models.ForeignKey(Problem)
    user = models.ForeignKey(UserProfile)
    result = models.IntegerField()
    penatly = models.IntegerField()
    solve_time = models.DateTimeField(null = True)
    class Meta:
        db_table = u'contest_user_problem'

class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest)
    problem = models.ForeignKey(Problem)

    display_order = models.IntegerField()

    class Meta:
        db_table = u'contest_problem'