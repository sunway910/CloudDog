from apscheduler.schedulers.background import BackgroundScheduler  # 使用它可以使你的定时任务在后台运行
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import time

'''
date：在您希望在某个特定时间仅运行一次作业时使用
interval：当您要以固定的时间间隔运行作业时使用
cron：以crontab的方式运行定时任务
minutes：设置以分钟为单位的定时器
seconds：设置以秒为单位的定时器
'''

try:
    scheduler = BackgroundScheduler()  # 创建定时任务的调度器对象——实例化调度器
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")


    # 'cron'方式循环，周一到周五，每天9:30:10执行,id为工作ID作为标记
    @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10', id='task_time')
    def my_job(param1, param2):  # 定义定时任务
        # 定时每5秒执行一次
        # t_now = time.localtime()
        print(time.strftime('%Y-%m-%d %H:%M:%S'))


    # 监控任务
    register_events(scheduler)

    # 向调度器中添加定时任务
    scheduler.add_job(my_job, 'date', args=[100, 'python'])
    # 启动定时任务调度器工作——调度器开始
    scheduler.start()
except Exception as e:
    print('定时任务异常：%s' % str(e))
