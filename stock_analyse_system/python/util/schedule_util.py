import time
import datetime
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
#
# def job():
#     print("job",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
#
#
# # 该示例代码生成了一个BlockingScheduler调度器，使用了默认的任务存储MemoryJobStore，以及默认的执行器ThreadPoolExecutor，并且最大线程数为10。
#
# # BlockingScheduler：在进程中运行单个任务，调度器是唯一运行的东西
# scheduler = BackgroundScheduler()
# # 采用阻塞的方式
# # 采用固定时间间隔（interval）的方式，每隔5秒钟执行一次
# # scheduler.add_job(job, 'interval', seconds=5)
# scheduler.add_job(job, 'cron', hour=13,minute=58)
#
#
# scheduler.start()
#
# while True:
#       print("------------")
#       time.sleep(5)
# #     print('main-start:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
# #     time.sleep(2)
# #     print('main-end:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
import snow_ball_service
import date_time_util
# print(type((datetime.datetime.today() + datetime.timedelta(-1)).strftime("%Y-%m-%d %H:%M:%S")))
# print(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
snow_ball_service.get_stock_position_combination(date_time_util.get_date_time(-2),date_time_util.get_date_time(0))