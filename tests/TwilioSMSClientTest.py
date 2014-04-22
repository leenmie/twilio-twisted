# -*- coding: utf-8 -*-
'''
Created on Apr 21, 2014

@author: leen
'''
from twisted.trial import unittest
from twiliotwisted.TwilioSMSClient import TwilioSMSClient
from twiliotwisted.TwilioException import ErrorResultException
from .TestConfig import ACCOUNT_SID, AUTH_TOKEN, FROM_NUMBER, TO_NUMBER

class MyTwilioSMSClient(TwilioSMSClient):
    def get_result(self, result):
        """implement this to handle sending result"""
        print result
        
    def get_error(self, error):
        """implement this to handle sending error"""
        if error.check(ErrorResultException):
            print error.value.message
        else:
            raise Exception("Unknown error")
    

class TwilioSMSClientTest(unittest.TestCase):

    def testSendMessage(self):
        
        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN      
        auth = {"account_sid": account_sid, "auth_token": auth_token}
        client = MyTwilioSMSClient(auth)
        
        from_number = FROM_NUMBER
        to_number = TO_NUMBER
        sms = {
                   'body': u'đù má',
                   'from': from_number,
                   'to': to_number,
                   }
        d = client.send_message(sms)        
        return d
    
    def testSendMessageProxy(self):
        """You must start a HTTP Proxy on your machine to pass this test"""              
        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN
        proxy = ("localhost", 9999)
        auth = {"account_sid": account_sid, "auth_token": auth_token}
        client = MyTwilioSMSClient(auth, proxy=proxy)
        
        from_number = FROM_NUMBER
        to_number = TO_NUMBER
        sms = {
                   'body': u'đù má',
                   'from': from_number,
                   'to': to_number,
                   }
        d = client.send_message(sms)        
        return d