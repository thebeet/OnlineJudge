'''
Created on 2012-9-13

@author: Macro
'''

from django.db import models

class Statistics(models.Model):
    pass
#    def get_ac_num(self):
#        from django.db import connection, transaction
#        cursor = connection.cursor()
#        cursor.execute("""SELECT count(submit_time)
#            from solution where result=1
#            group by left(submit_time, 10)""", [self.baz])
#        return cursor.fetchall()