from django.db import models
from django.db.models import Q


class ProblemManager(models.Manager):
    def list(self, user=None):
        if user and user.is_authenticated():
            return list(Problem.objects.raw("""select id, title, solved, user_status, collect from problem left join
                     (select problem_id id, result user_status, collect from user_problem where user_id = %s ) as t using(id) where defunct=0""", [user.id,]))
        else:
            return Problem.objects.filter(defunct=False).values("id", "title", "solved")

    def list_order(self, user=None):
        if user and user.is_authenticated():
            return list(Problem.objects.raw("""select id, title, solved, user_status, collect from problem left join
                     (select problem_id id, result user_status, collect from user_problem where user_id = %s ) as t using(id) where defunct=0 order by solved DESC""", [user.id,]))
        else:
            return Problem.objects.filter(defunct=False).values("id", "title", "solved").order_by("-solved")

    def volume(self, page, user=None, problem_start=1000, pagesize=50):
        start =  problem_start + pagesize * (page - 1)
        end = problem_start + pagesize * page
        if user and user.is_authenticated():
            return list(Problem.objects.raw("""select id, title, solved, user_status, collect from problem left join
                     (select problem_id id, result user_status, collect from user_problem where user_id = %s ) as t using(id) where defunct=0 and (id >= %s) and (id < %s)""", [ user.id, start, end,]))
        else:
            return Problem.objects.list().filter(id__lt = problem_start + pagesize * page, id__gte = problem_start + pagesize * (page - 1))

    def fav_problem(self, user):
        if user and user.is_authenticated():
            return list(Problem.objects.raw("""select id, title, solved, user_status, collect from problem left join
                     (select problem_id id, result user_status, collect from user_problem where user_id = %s ) as t using(id) where collect = 1""", [user.id,]))
        else:
            return list()

    def volume_size(self, problem_start=1000, pagesize=50):
        from django.db.models import Max
        return int((Problem.objects.filter(defunct=False).aggregate(max_id=Max("id"))["max_id"] - problem_start + pagesize) / pagesize)

    def search_list(self, user = None, keyword = ""):
        keywordList = [];
        if keyword != "":
            keywordList = keyword.split(' ')
        if user and user.is_authenticated():
            params = [user.id, ]
            sqlBeg = "select id, title, solved, user_status, collect from problem left join (select problem_id id, result user_status, collect from user_problem where user_id =%s ) as t using(id) where "
            sqlEnd = "defunct=0"
            sqlQuery = ""
            for word in keywordList:
                sqlQuery += "(title like %s or description like %s) and "
                params.append('%' + word + '%')
                params.append('%' + word + '%')
            s = sqlBeg + sqlQuery + sqlEnd
            return list(Problem.objects.raw(s, params))
        else:
            resultList = Problem.objects.list()
            for word in keywordList:
                resultList = resultList.filter(Q(title__icontains = word) | Q(description = word))
            return list(resultList)

    def is_problem_num(self, keyword = ""):
        queryRet = list(Problem.objects.filter(id = keyword))
        if len(queryRet) == 1:
            return True
        else:
            return False

class Problem(models.Model):
    title = models.CharField(max_length=765)
    case_number = models.IntegerField()
    time_limit = models.IntegerField(default = 1000)
    case_time_limit = models.IntegerField(default = 3000)
    memory_limit = models.IntegerField()
    output_limit = models.IntegerField()
    is_spj = models.BooleanField()

    description = models.TextField()
    input = models.TextField()
    output = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    hint = models.TextField(null = True, blank = True)
    source = models.CharField(max_length = 300)
    analysis = models.TextField(null = True, blank = True)
    create_time = models.DateTimeField()

    defunct = models.BooleanField()

    solved = models.IntegerField(default = 0)

    objects = ProblemManager()

    def statistic(self):
        from JudgeWeb.solution.models import Solution
        from django.db.models import Count
        from JudgeWeb.common.result import result_full_tag, result_short_tag, result_tag_count
        result_counts = Solution.objects.values("user").filter(problem=self.id).values('result').annotate(result_count = Count('result')).order_by('result')
        self.statistic = {'all': 0}
        for i in range(result_tag_count):
            self.statistic[result_short_tag[i]] = 0
        for row in result_counts:
            self.statistic[result_short_tag[row['result']]] = row['result_count']
            self.statistic['all'] += row['result_count']
        #statistic['all'] = Solution.objects.values("user").filter(problem=self.pid).count()
        return self.statistic

    def get_statistic_with_contest(self, contest):
        from JudgeWeb.solution.models import Solution
        from JudgeWeb.contest.models import UserContestProblem
        from django.db.models import Count
        from JudgeWeb.common.result import result_full_tag, result_short_tag, result_tag_count
        result_counts = Solution.objects.values("user").filter(contest=contest,problem=self.id).values('result').annotate(result_count = Count('result')).order_by('result')
        self.statistic = {'all': 0}
        for i in range(result_tag_count):
            self.statistic[result_short_tag[i]] = 0
        for row in result_counts:
            self.statistic[result_short_tag[row['result']]] = row['result_count']
            self.statistic['all'] += row['result_count']
        self.statistic['solved'] = UserContestProblem.objects.filter(contest=contest).filter(problem=self.id).filter(result=1).count()
        print self.statistic['solved']
        return self.statistic

    def __unicode__(self):
        return self.id.__str__()

    class Meta:
        db_table = u'problem'