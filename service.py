import schedule
from time import sleep
from infoMaq import DataCollector

class MyService():

    def __init__(self):
        self.data_collector = DataCollector()
    
    def initJob(self):

        def job():
            self.data_collector.initCollect()

        schedule.every(1).minutes.do(job)

        while True:
            schedule.run_pending()
            sleep(2)
