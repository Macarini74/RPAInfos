import schedule
import win32serviceutil
import win32event
import win32service
import servicemanager
from infoMaq import DataCollector

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "GetInfo"
    _svc_display_name_ = "Get System Info Background"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.data_collector = DataCollector()
    
    def SvcDoRun(self):

        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))

        def job():
            self.data_collector.initColect()

        schedule.every().day.do(job)

        while True:
            schedule.run_pending()
            if win32event.WaitForSingleObject(self.stop_event, 10000) == win32event.WAIT_OBJECT_0:
                break
        
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STOPPED, (self._svc_name_, ''))
