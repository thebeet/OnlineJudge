'''
Created on 2012-7-25

@author: TheBeet
'''
from django.core.paginator import Paginator
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse

from django.views.generic import DetailView, ListView, TemplateView, View, FormView

from JudgeWeb.user.models import UserProblem
from models import Problem
from django.views.decorators.csrf import csrf_exempt

def ajax_fav(request):
    if request.user.is_authenticated():
        problem = Problem.objects.filter(defunct=False).get(id=int(request.POST.get("problem")))
        user_problem, new = UserProblem.objects.get_or_create(user=request.user.get_profile(), problem=problem)
        print user_problem.collect, new
        if user_problem.collect:
            user_problem.collect = False
        else:
            user_problem.collect = True
        user_problem.save()
        return HttpResponse(user_problem.collect)
    return HttpResponse("-1")

class ProblemDetailView(DetailView):
    template_name = 'problem/detail.html'
    model = Problem

class ProblemListView(ListView):
    template_name = 'problem/list.html'
    model = Problem
    paginate_by = 50
    def get(self, request, *args, **kwargs):
        import re
        if (request.GET.get("search") and re.search("^\d+$", request.GET.get("search"))):
            if len(Problem.objects.list().filter(id=request.GET.get("search"))) == 1:
                return redirect("problem:detail", pk=request.GET.get("search"))
        return super(ProblemListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if self.kwargs.get("order"):
            return Problem.objects.list_order(self.request.user)
        elif self.request.GET.get("search"):
            return Problem.objects.search_list(self.request.user, self.request.GET["search"])
        else:
            return Problem.objects.list(self.request.user)


class ProblemStatisticView(DetailView):
    template_name = 'problem/statistic.html'
    model = Problem
    def get_context_data(self, **kwargs):
        context = kwargs
        context_object_name = self.get_context_object_name(self.object)
        if context_object_name:
            context[context_object_name] = self.object
        from JudgeWeb.solution.models import Solution
        context["object_list"] = list(Solution.objects.best(self.kwargs.get("pk")))
        return context

class ProblemVolumeView(ListView, FormView):
    template_name = 'problem/list.html'
    model = Problem

    def get(self, request, *args, **kwargs):
        if (self.kwargs.get("volume")):
            self.volume = int(self.kwargs["volume"])
        elif (self.request.COOKIES.get("volume")):
            self.volume = int(self.request.COOKIES.get("volume"))
        else:
            self.volume = 1
        response = super(ProblemVolumeView, self).get(request, *args, **kwargs)
        response.set_cookie("volume", self.volume, max_age = 365 * 24 * 3600)
        return response

    def get_context_data(self, **kwargs):
        context = super(ProblemVolumeView, self).get_context_data(**kwargs)
        volume_total = Problem.objects.volume_size()
        context["volume"] = self.volume
        context["volume_range"] = range(1, volume_total + 1)
        context["volume_total"] = volume_total
        return context

    def get_queryset(self):
        return Problem.objects.volume(self.volume, self.request.user)


class ProblemSearchView(ListView):
    template_name = 'problem/list.html'
    model = Problem

    def get_queryset(self):
        return Problem.objects.search_list(self.request.user, self.kwargs["keyword"])

class ProblemFavListView(ListView, FormView):
    template_name = 'problem/list.html'
    model = Problem
    paginate_by = 50


    def get_queryset(self):
        print "enter"
        if self.request.user.is_authenticated():
            print "auth"
            return Problem.objects.fav_problem(self.request.user)








