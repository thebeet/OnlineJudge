'''
Created on 2012-7-27

@author: TheBeet
'''
from django.db import models

class Language(models.Model):
    name = models.CharField(max_length = 64)
    defunct = models.BooleanField(default = False)

    class Meta:
        db_table = u'language'