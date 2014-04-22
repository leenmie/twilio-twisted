# -*- coding: utf-8 -*-
'''
Created on Apr 20, 2014

@author: leen
'''
from twisted.trial import unittest
from twiliotwisted.TwilioSMSMessage import TwilioSMSMessage
from twiliotwisted.TwilioException import ErrorResultException
from .TestConfig import ACCOUNT_SID, AUTH_TOKEN, FROM_NUMBER, TO_NUMBER

def print_response(res):
    print res
        
def error_response(res):
    if res.check(ErrorResultException):
        print res.value.message
    else:
        raise Exception("Unknown error")


class TwilioSMSMessageTest(unittest.TestCase):

    def testSendMessage(self):    
        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN
        auth = {"account_sid": account_sid, 
                "auth_token": auth_token}
        message = TwilioSMSMessage(auth)
        from_number = FROM_NUMBER
        to_number = TO_NUMBER
        d = None
        for _ in range(2):
            sms = {
                   'body': u'đù má',
                   'from': from_number,
                   'to': to_number,
                   }        
            d = message.send_message(sms)
            d.addCallback(print_response)
            d.addErrback(error_response)
        return d
    
    def testSendMessageProxy(self):    
        """You must start a HTTP Proxy on your machine to pass this test"""              
        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN
        proxy = ("localhost", 9999)
        auth = {"account_sid": account_sid, 
                "auth_token": auth_token}
        message = TwilioSMSMessage(auth, proxy=proxy)
        from_number = FROM_NUMBER
        to_number = TO_NUMBER
        d = None
        for _ in range(2):
            sms = {
                   'body': u'đù má',
                   'from': from_number,
                   'to': to_number,
                   }        
            d = message.send_message(sms)
            d.addCallback(print_response)
            d.addErrback(error_response)
        return d
        