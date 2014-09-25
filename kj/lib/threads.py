import os
import time, datetime
import traceback
from threading import Thread

from ..models.user import User
from ..models.email_queue import EmailQueue

from ..db import DBSession

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR



class BaseWorker(Thread):
    
    #slow it down, so that SqlAlchemy 'sa_engine' has time to bind itself
    FIXED_STARTUP_DELAY=10 * SECOND
    

    def __init__(self, startup_delay=None, loop_sleep=None, enabled=None):
        """
        Delays are in seconds
        """
        Thread.__init__(self)
        
        #For stopping thread
        self.should_run = True
        
        self.loop_count = 0

        self.startup_delay = startup_delay + BaseWorker.FIXED_STARTUP_DELAY
        self.loop_sleep = loop_sleep
        self.enabled = enabled

        
    def run(self):
        time.sleep(self.startup_delay)
        
        self.initialize_thread()

        while self.should_run:
            try:
                self.process()
            except Exception, e:
                str_exc = traceback.format_exc()
            
            self.loop_count += 1
            time.sleep(self.loop_sleep)

        self.shutdown_thread()

    def initialize_thread(self):
        """Call when thread wants to do some initialization
        """
        pass
        
    def process(self):
        raise MethodHasToBeRedefined()
        
    def shutdown_thread(self):
        """Call when thread wants to do some final code
        """
        
    def stop(self):
        self.should_run = False

class SendEmails(BaseWorker):

    def __init__(self):
        BaseWorker.__init__(
            self,
            startup_delay = 1 * SECOND,
            loop_sleep = 10 * SECOND)

    def process(self):
        emails_to_send = EmailQueue.get_emails_to_send()
        for email in emails_to_send:
            email.send()
    
keep_alive_worker = None

def start_all_threads():
    global keep_alive_worker
    
    stop()
    
    keep_alive_worker = SendEmails()
    keep_alive_worker.start()
    
def stop():
    for t in [keep_alive_worker]:
        if t:
            t.stop()

