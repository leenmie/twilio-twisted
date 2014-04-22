'''
Created on Apr 21, 2014

@author: leen
'''
from TwilioSMSMessage import TwilioSMSMessage

class TwilioSMSClient():
    def __init__(self, auth, verify=True, proxy=None):
        self.SMSMessage = TwilioSMSMessage(auth, verify, proxy)
    
    def get_result(self, result):
        """implement this to handle sending result"""
        pass
        
    def get_error(self, error):
        """implement this to handle sending error"""
        pass
    
    def send_message(self, message):
        _deferred = self.SMSMessage.send_message(message)
        _deferred.addCallback(self.get_result)
        _deferred.addErrback(self.get_error)
        return _deferred
        