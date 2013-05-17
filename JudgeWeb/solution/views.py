'''
Created on 2012-7-26

@author: TheBeet
'''

from forms import SubmitSolutionForm
from models import Solution
from models import UserProfile
from JudgeWeb.user.models import UserProfile
from JudgeWeb.problem.models import Problem
from JudgeWeb.language.models import Language
from JudgeWeb.judger.models import Judger

from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import FormView

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.db.models import Q

class SubmitSolutionView(TemplateView):
    template_name = 'solution/submit.html'

    def post(self, request, *args, **kwargs):
        solution = Solution()
        solution.user = UserProfile.objects.get(id=request.user.id);
        solution.problem = Problem.objects.get(id=request.POST.get("problem"))
        solution.language = Language.objects.get(id=request.POST.get("language"))
        solution.contest = request.POST.get("contest")
        solution.source_code = request.POST.get("source_code")
        solution.result = 0;
        solution.judger = None
        solution.save()
        return HttpResponseRedirect("/soultion/")

class SolutionListView(ListView):
    template_name = 'solution/list.html'
    model = Solution
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.queryset = Solution.objects.get_query_set()
        if (request.GET.get('user')):
            try:
                user = UserProfile.objects.get(username=request.GET.get('user'))
                self.queryset = self.queryset.filter(user=user)
            except:
                from django.http import HttpResponseNotFound
                return HttpResponseNotFound()
        if (request.GET.get('problem')):
            try:
                problem = Problem.objects.get(id=request.GET.get('problem'))
                self.queryset = self.queryset.filter(problem=problem)
            except:
                from django.http import HttpResponseNotFound
                return HttpResponseNotFound()
        if (request.GET.get('result')):
            result = request.GET.get('result')
            self.queryset = self.queryset.filter(result=result)
        if (request.GET.get('language')):
            language = Language.objects.get(id=int(request.GET.get('language')))
            self.queryset = self.queryset.filter(language=language)
        return super(SolutionListView, self).get(request, *args, **kwargs)

class SolutionDetailView(DetailView):
    template_name = 'solution/detail.html'
    model = Solution

class SolutionCompareView(TemplateView):
    template_name = 'solution/compare.html'
    model = Solution

    def get_context_data(self, **kwargs):
        context = super(SolutionCompareView, self).get_context_data(**kwargs)
        if ("user1" in kwargs) == False or ("user2" in kwargs) == False :
            return context
        user1 = kwargs["user1"]
        user2 = kwargs["user2"]
        context['user1'] = user1
        context['user2'] = user2
        user1id = self.get_id_from_username(user1)
        user2id = self.get_id_from_username(user2)
        if user1id > 0 and user2id > 0:
            user1AcSol = Solution.objects.filter(result = 1, user_id=user1id).distinct()
            user2AcSol = Solution.objects.filter(result = 1, user_id=user2id).distinct()
            user1Ac = self.get_problem_id_set(user1AcSol)
            user2Ac = self.get_problem_id_set(user2AcSol)
            context['acUserSame'] = sorted(user1Ac & user2Ac)
            acUser1Only = user1Ac - user2Ac
            acUser2Only = user2Ac - user1Ac

            user1RjSol = Solution.objects.filter(~Q(result = 1), user_id=user1id).distinct()
            user2RjSol = Solution.objects.filter(~Q(result = 1), user_id=user2id).distinct()
            user1Rj = self.get_problem_id_set(user1RjSol) - user1Ac
            user2Rj = self.get_problem_id_set(user2RjSol) - user2Ac
            context['rjUserSame'] = sorted(user1Rj & user2Rj)
            rjUser1Only = user1Rj - user2Rj
            rjUser2Only = user2Rj - user1Rj
            user1AcUser2Rj = acUser1Only & rjUser2Only
            user2AcUser1Rj = acUser2Only & rjUser1Only
            context['rjUser1Only'] = sorted(rjUser1Only)
            context['rjUser2Only'] = sorted(rjUser2Only)

            acUser1Flag = []
            acUser2Flag = []
            for item in sorted(acUser1Only):
                if item in user1AcUser2Rj:
                    acUser1Flag.append([item, True])
                else:
                    acUser1Flag.append([item, False])

            for item in sorted(acUser2Only):
                if item in user2AcUser1Rj:
                    acUser2Flag.append([item, True])
                else:
                    acUser2Flag.append([item, False])
            context['acUser1Flag'] = acUser1Flag
            context['acUser2Flag'] = acUser2Flag
            context['isexist'] = True

        return context

    def get_id_from_username(self, username):
        user = UserProfile.objects.filter(username=username)
        if user.count() == 1:
            return user[0].id
        else:
            return -1

    def get_problem_id_set(self, queryresult):
        res = set({})
        for item in queryresult:
            res.add(item.problem_id)
        return res

class SystemInfoView(TemplateView):
    template_name = "dashboard/sysinfo.html"
    model = Solution

    def get_mem_info(self):
        mem = {}
        f = open("/proc/meminfo")
        lines = f.readlines()
        f.close()
        for line in lines:
            if len(line) < 2: continue
            name = line.split(':')[0]
            var = line.split(':')[1].split()[0]
            mem[name] = long(var) * 1024.0
        mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
        return mem

    def get_disk_info(self):
        import os
        hd={}
#        disk = os.statvfs("/")
#        hd['available'] = disk.f_bsize * disk.f_bavail
#        hd['capacity'] = disk.f_bsize * disk.f_blocks
#        hd['used'] = disk.f_bsize * disk.f_bfree
        return hd

