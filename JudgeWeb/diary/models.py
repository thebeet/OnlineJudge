from django.db import models


class Diary(models.Model):
    create_time = models.DateField(auto_now_add = True)
    content = models.TextField();

    class Meta:
        db_table = u'diary'