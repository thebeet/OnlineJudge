from django.views.generic import ListView

from models import Diary

class DiaryView(ListView):
    template_name = 'diary/diary.html'
    model = Diary
