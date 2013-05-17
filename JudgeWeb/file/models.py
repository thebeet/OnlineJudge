from django.db import models


class File(models.Model):
    create_time = models.DateField(auto_now_add = True)
    content = models.FileField();

    class Meta:
        db_table = u'file'