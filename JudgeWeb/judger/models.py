from django.db import models

class Judger(models.Model):
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    judger_name = models.CharField(max_length = 128)
    info = models.TextField(blank = True)

    defunct = models.BooleanField(default = False)

    class Meta:
        db_table = u'judger'