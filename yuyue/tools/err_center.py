#!/usr/bin/env python
import time


def err_record(err):
    open('./Logs/err_%s.log'%(time.strftime('%Y-%m-%d',time.localtime(time.time()))),'a',encoding='utf8').write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\t'+err)

                            
