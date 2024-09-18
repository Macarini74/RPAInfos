from service import MyService
from infoMaq import DataCollector
import win32serviceutil

if __name__ == '__main__':

    data_collect = DataCollector()
    data_collect.initCollect()
    #win32serviceutil.HandleCommandLine(MyService)