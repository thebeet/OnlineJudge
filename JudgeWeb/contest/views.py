'''
Created on 2012-8-11

@author: TheBeet
'''
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.views.generic import DetailView, ListView, TemplateView

from models import Contest, ContestProblem
from JudgeWeb.problem.models import Problem
from JudgeWeb.solution.models import Solution

class ContestListView(ListView):
    template_name = 'contest/list.html'
    model = Contest
    paginate_by = 20
    def get_queryset(self):
        if (self.kwargs.get("status") == "now"):
            return Contest.objects.now()
        elif (self.kwargs.get("status") == "past"):
            return Contest.objects.past()
        elif (self.kwargs.get("status") == "scheduled"):
            return Contest.objects.scheduled()
        else:
            return Contest.objects.all()

class ContestDetailView(DetailView):
    template_name = 'contest/detail.html'
    model = Contest

    def get_object(self, queryset=None):
        temp = super(ContestDetailView, self).get_object(queryset)
        temp.get_problems(self.request.user)
        return temp


class ContestStatisticView(DetailView):
    template_name = 'contest/statistic.html'
    model = Contest


class ContestProblemView(DetailView):
    template_name = 'contest/problem.html'
    model = Contest
    def get_context_data(self, **kwargs):
        context = kwargs
        contestid = self.kwargs['pk']
        contest_problem = self.kwargs['problem']
        displayorder = ord(contest_problem) - ord('A') + 1
        contest_problems = ContestProblem.objects.filter(contest_id = contestid, display_order = displayorder)
        if len(contest_problems) == 1:
            problemid = contest_problems[0].problem_id
            context['problem'] = (Problem.objects.filter(id = problemid))[0]
            submitSolutions = Solution.objects.filter(problem_id = problemid, contest_id = contestid)
            context['submit_counter'] = len(submitSolutions)
            submit_user = Solution.objects.raw('''SELECT distinct user_id AS subuser, id FROM solution WHERE problem_id = %s AND contest_id = %s''', [problemid, contestid])
            context['submit_user_counter'] = len(list(submit_user))
            acSolutions = Solution.objects.filter(problem_id = problemid, contest_id = contestid, result = 1)
            context['ac_solution_counter'] = len(acSolutions)
            ac_user = Solution.objects.raw('''SELECT distinct user_id AS subuser, id FROM solution WHERE problem_id = %s AND contest_id = %s AND result = 1''', [problemid, contestid])
            context['ac_submit_user_counter'] = len(list(ac_user))
            
        return context
    
class ContestRankView(ListView):
    template_name = 'contest/rank.html'
    model = Contest
    
    def get_context_data(self, **kwargs):
        context = super(ContestRankView, self).get_context_data(**kwargs)
        context["contest_prob"] = list(ContestProblem.objects.filter(contest_id = self.kwargs["contest_id"]));
        return context
    
    def get_queryset(self):
        contestid = self.kwargs["contest_id"]
        self.kwargs["problems_num"] = len(ContestProblem.objects.filter(contest_id=contestid))
        return Contest.objects.rank((Contest.objects.filter(id=contestid))[0])







