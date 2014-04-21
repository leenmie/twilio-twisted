# -*- coding: utf-8 -*-
'''
Created on Apr 21, 2014

@author: leen
'''
from twisted.trial import unittest
from twiliotwisted.TwilioSMSClient import TwilioSMSClient
from twiliotwisted.TwilioException import ErrorResultException
from .TestConfig import ACCOUNT_SID, AUTH_TOKEN, FROM_NUMBER, TO_NUMBER

class TwilioSMSClientTest(unittest.TestCase):

    def testSendMessage(self):
        def print_response(res):
            print res
        
        def error_response(res):
            if res.check(ErrorResultException):
                print res.value.message

        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN      
        auth = {"account_sid": account_sid, "auth_token": auth_token}
        client = TwilioSMSClient(auth)
        
        from_number = FROM_NUMBER
        to_number = TO_NUMBER
        sms = {
                   'body': u'đù má',
                   'from': from_number,
                   'to': to_number,
                   }
        d = client.send_message(sms)        
        return d