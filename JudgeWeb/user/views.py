'''
Created on 2012-7-26

@author: TheBeet
'''
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from models import UserProfile
from forms import RegisterForm
from django.views.generic import DetailView, ListView, FormView, TemplateView

def ajax_login(request):
    print request.POST
    message = request.user
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.POST.get("remember") == "on":
                    pass
                else:
                    request.session.set_expiry(0)
                message = 'OK'
            else:
                message = 'User Not Active'
        else:
            message = 'ERROR'
    return render_to_response('message.json', {"message" : message}, mimetype="application/json") #application/json

def ajax_logout(request):
    if request.method == 'POST':
        logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def ajax_name_tips(request):
    #todo
    pass

class UserDetailView(DetailView):
    template_name = 'user/detail.html'
    model = UserProfile
    slug_field = 'username'

class UserStatisticView(DetailView):
    template_name = 'user/statistic.html'
    model = UserProfile
    slug_field = 'username'
    def get_object(self):
        getobject = super(UserStatisticView,self).get_object()
        getobject.get_statistic()
        return getobject

class UserRankView(ListView):
    template_name = 'user/rank.html'
    paginate_by = 100
    model = UserProfile
    queryset = UserProfile.objects.rank()

class RegisterView(TemplateView, FormView):
    template_name = 'user/register.html'
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        if self.request.GET.__contains__("user"):
            userProfSet = UserProfile.objects.filter(username=self.request.GET["user"])
            if userProfSet.count() == 1:
                context["isModify"] = True
                userProf = userProfSet[0]
                context["userProfile"] = userProf
            else:
                context["isModify"] = False
        else:
            context["isModify"] = False
        return context

    def get_queryset(self):
        pass

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated() == True:
            #userProf = self.request.user
            userProf = UserProfile.objects.filter(username=self.request.user.username)[0]
        else:
            userProf = UserProfile()
            userProf.username = request.POST['username']
            userProf.reg_ip = request.META['REMOTE_ADDR']
            userProf.login_ip = request.META['REMOTE_ADDR']
            
        if (request.POST['password'] != "") & (request.POST['password'] == request.POST['password2']):
            userProf.set_password(request.POST['password'])
        userProf.nickname = request.POST['nickname']
        userProf.email = request.POST['email']
        userProf.school = request.POST['school']
        userProf.stu_no = request.POST['stu_no']
        userProf.realname = request.POST['realname']
        userProf.birthday = request.POST['birthday']
        userProf.address = request.POST['address']
        userProf.phone = request.POST['phone']
        userProf.department = request.POST['department']
        userProf.institute = request.POST['institute']
        if request.POST['sex'] == 'male':
            userProf.gender = 1
        else:
            userProf.gender = 0
        userProf.save()
        return HttpResponseRedirect('/')
    
