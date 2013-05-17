'''
Created on 2012-9-13

@author: Macro
'''
import datetime
import platform
import os
import ctypes
import random

from django.views.generic.base import TemplateView

result_full_tag = {0: 'Waiting',
                1: 'Accepted',
                2: 'Presentation Error',
                3: 'Wrong Answer',
                4: 'Runtime error',
                5: 'Time Limit Exceed',
                6: 'Memory Limit Exceed',
                7: 'Output Limit Exceed',
                8: 'Compile Error',
                9: 'System Error',
                10: 'Validate Error',
                11: 'Restricted Call',
                12: 'Running',}

class DashBoardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_ac_num(self):
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute("""SELECT count(*) as ac_num, concat(year(submit_time),'-',month(submit_time)) as submit_date
            from solution where result=1 group by year(submit_time), month(submit_time)""")
        return cursor.fetchall()
    
    def get_submit_data(self, type, dateBeg, dateEnd):
        from django.db import connection, transaction
        cursor = connection.cursor()
        if type == "DAY":
            cursor.execute("""
                SELECT 
                    count(*) as ac_num, result,
                    concat(year(submit_time), '-', month(submit_time), '-', day(submit_time)) as submit_date
                from
                    solution
                WHERE submit_time >= """ + dateBeg + " AND submit_time <= " + dateEnd +
                """ group by year(submit_time), month(submit_time), day(submit_time) , result
                """)
        elif type == "WEEK":
            cursor.execute("""
                SELECT 
                    count(*) as ac_num, result,
                    concat(year(submit_time), 'Year ', week(submit_time), 'th Week') as submit_date
                from
                    solution
                WHERE submit_time >= """ + dateBeg + " AND submit_time <= " + dateEnd +
                """ group by year(submit_time) , week(submit_time) , result
                """)
        elif type == "MONTH":
            cursor.execute("""
                SELECT 
                    count(*) as ac_num, result,
                    concat(year(submit_time), '-', month(submit_time)) as submit_date
                from
                    solution
                WHERE submit_time >= """ + dateBeg + " AND submit_time <= " + dateEnd +
                """ group by year(submit_time) , month(submit_time) , result
                """)
        else:
            cursor.execute("""
                SELECT 
                    count(*) as ac_num, result,
                    concat(year(submit_time), '-', month(submit_time)) as submit_date
                from
                    solution
                group by year(submit_time) , month(submit_time) , result
                """)
        desc = cursor.description
        reslist =  [dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()]
        lastDate = ""
        tableRow = []
        table = []
        for row in reslist:
            date = row["submit_date"]
            if lastDate != date:
                if lastDate != "":
                    tableRow[0] = lastDate
                    table.append(tableRow)
                tableRow = []
                for col in range(0, 14):
                    tableRow.append(0)
                lastDate = date;
            tableRow[row["result"] + 1] = row["ac_num"]
        if lastDate != "":
            tableRow[0] = lastDate
            table.append(tableRow)
        
        return table
    
    def get_piechart_data(self):
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute("""
            SELECT count(*) AS type_count, result from solution group by result;
            """)
        desc = cursor.description
        reslist =  [dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()]
        count_list = [];
        for row in reslist:
            row["result"] = result_full_tag[row["result"]]
            count_list.append(row);
        return count_list
        

    def get_context_data(self, **kwargs):
        context = super(DashBoardView, self).get_context_data(**kwargs)
        context['piechart_data'] = self.get_piechart_data()
        viewType = "ALL"
        if ("beg" in kwargs) == True:
            dateBeg = kwargs["beg"]
            dateEnd = kwargs["end"]
            dayDelta = abs(self.date_delta(dateBeg, dateEnd))
            if dayDelta < 60:
                viewType = "DAY"
            elif dayDelta < 365:
                viewType = "WEEK"
            else:
                viewType = "MONTH"
            context['ac_statistics'] = self.get_submit_data(viewType, dateBeg, dateEnd)
            context['dateBegText'] = dateBeg[0:4] + "-" + dateBeg[4:6] + "-" + dateBeg[6:8]
            context['dateEndText'] = dateEnd[0:4] + "-" + dateEnd[4:6] + "-" + dateEnd[6:8]
        else:
            context['ac_statistics'] = self.get_submit_data(viewType, 0, 0)
            context['dateBegText'] = ""
            context['dateEndText'] = ""
        # system info
        context['memstat'] = self.get_memory_stat()
        context['diskstat'] = self.get_disk_stat()
        context['loadstat'] = self.get_load_stat()
        return context

    def date_delta(self, dateBeg, dateEnd):
        dBeg = self.num2date(int(dateBeg))
        dEnd = self.num2date(int(dateEnd))
        return (dEnd - dBeg).days

    def num2date(self, dateNum):
        y = (dateNum - dateNum % 10000) / 10000
        md = dateNum - y * 10000
        m = (md - md % 100) / 100
        d = md - m * 100
        return datetime.datetime(y, m, d)

    
    def get_disk_stat(self):
        import os
        hd={}
        if platform.system() == 'Linux':
            disk = os.statvfs("/")
            hd['available'] = disk.f_bsize * disk.f_bavail
            hd['capacity'] = disk.f_bsize * disk.f_blocks
            hd['used'] = disk.f_bsize * disk.f_bfree
            hd['UsedPercent'] = int(hd['used'] * 100 / hd['capacity'])
        else:
            hd['used'] = random.randint(0, 100)
            hd['capacity'] = 100
            hd['UsedPercent'] = 80
        return hd

    def get_memory_stat(self):
        mem = {}
        if platform.system() == "Linux":
            f = open("/proc/meminfo")
            lines = f.readlines()
            f.close()
            for line in lines:
                if len(line) < 2: continue
                name = line.split(':')[0]
                var = line.split(':')[1].split()[0]
                mem[name] = long(var) * 1024.0
            mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
            mem['UsedPercent'] = int(mem['MemUsed'] * 100 / mem['MemTotal'])
        else:
            mem['MemUsed'] = 980
            mem['MemTotal'] = 1000
            mem['UsedPercent'] = random.randint(0, 100)
        return mem
    
    def get_load_stat(self):
        loadavg = {}
        if platform.system() == "Linux":
            f = open("/proc/loadavg")
            con = f.read().split()
            f.close()
            loadavg['lavg_1']=con[0]
            loadavg['lavg_5']=con[1]
            loadavg['lavg_15']=con[2]
            loadavg['nr']=con[3]
            loadavg['last_pid']=con[4]
        else:
            loadavg['lavg_1']=random.randint(0,20)
            loadavg['lavg_5']=random.randint(0,100)
            loadavg['lavg_15']=random.randint(0,200)
            loadavg['nr']=1/13
            
        return loadavg

