'''
Created on 2012-7-28

@author: TheBeet
'''
from django.contrib.auth.forms import AuthenticationForm

def current_app(request):
    split_result = request.path.split('/')
    split_result[-1] = 'home'
    return {'CURRENT_APP': split_result[1]}

def judge_config(request):
    return {'JUDGE_NAME': 'XMU Online Judge'}

def result_all(request):
    from JudgeWeb.common.result import result_all, result_all_short
    return {'result_all': result_all, 'result_all_short': result_all_short}

def mail(request):
    from JudgeWeb.mail.models import Mail
    if (request.user.is_authenticated()):
        new_mail = Mail.objects.new(request.user)
        return {'new_mail': new_mail.count()}
    return {}

def contest(request):
    from JudgeWeb.contest.models import Contest
    running_contest = Contest.objects.now()
    scheduled_contest = Contest.objects.scheduled()
    return {'running_contest': running_contest.count(), 'scheduled_contest': scheduled_contest.count()}
