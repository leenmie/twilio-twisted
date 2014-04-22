# -*- coding: utf-8 -*-
'''
Created on Apr 18, 2014

@author: leen
'''
import urllib
import json
from twisted.internet import reactor
from twisted.web.client import Agent, ProxyAgent
from twisted.web.http_headers import Headers
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.client import FileBodyProducer
from StringIO import StringIO
from twiliotwisted.TwilioException import ErrorResponseException, ErrorResultException
from twiliotwisted.SSLVerifiedClientContextFactory import SSLVerifiedClientContextFactory
from twisted.internet.endpoints import TCP4ClientEndpoint
from email import base64mime


#from OpenSSL.crypto import load_certificate

TWILIO_REST_API_URI = 'https://api.twilio.com/'
REST_API_VERSION = '2010-04-01'

import logging
logging.basicConfig(level=logging.DEBUG)

class ResponseBody(Protocol):
    def __init__(self, response, max_length):
        self.deferred = Deferred()
        self.response = response
        self.max_length = max_length
        self.body = ""

    def dataReceived(self, data):
        self.body += data
        if len(self.body) > self.max_length:
            self.transport.loseConnection()

    def connectionLost(self, reason):
        self.deferred.callback(self)

        
class TwilioResponseBody(ResponseBody):
            
    def connectionLost(self, reason):
        if self.response.code >= 400:
            self.deferred.errback(self)
        else:
            self.deferred.callback(self)

class TwilioSMSMessage():
    """
    Use Twilio REST API to send SMS
    """

    def __init__(self, auth, verify=True, verify_location='/etc/ssl/certs/', proxy=None):
        """
        auth: {"account_sid": account_sid, "auth_token": auth_token}
        verify: SSL certificate verification
        verify_location: path to your certificates folder (.pem format)
        proxy: ([str]host, [int]port)
        """
        contextFactory = SSLVerifiedClientContextFactory(verify = verify, verify_location = verify_location)
        agent = None
        if proxy:
            host, port = proxy
            endpoint = TCP4ClientEndpoint(reactor, host, port)
            agent = ProxyAgent(endpoint)
        else:
            agent = Agent(reactor, contextFactory)
        self.agent = agent
        self.account_sid = auth['account_sid']
        self.auth_token = auth['auth_token']
        self._generate_url()
        self._generate_auth_header()
    
    def _generate_url(self):
        self.MESSAGE_URI = ''.join([
                                    TWILIO_REST_API_URI,
                                    REST_API_VERSION,
                                    '/Accounts/{}/Messages'.format(self.account_sid) + '.json'
                                    ])
        
    def _generate_auth_header(self):
        s = '{}:{}'.format(self.account_sid, self.auth_token)
        encoded_s = base64mime.encode(s, maxlinelen=100)
        self._auth_header = 'Basic {}'.format(encoded_s).strip()
                        
    def send_message(self, message):
        post_message = {
                     'From': message['from'],                           
                     'To': message['to'],
                     'Body': message['body'].encode('utf-8'),                                                               
                    }                
        post_encoded = urllib.urlencode(post_message)
        post_data = FileBodyProducer(StringIO(post_encoded))
        header = Headers({
                          'User-Agent': ['twilio-python'],
                          'Authorization': [self._auth_header],
                          'Accept-Charset': ['utf-8'],
                          'Content-Type' : ['application/x-www-form-urlencoded'],
                          'Accept' : ['application/json'],
                          })
        d = self.agent.request(
                               'POST', 
                               self.MESSAGE_URI, 
                               header,
                               post_data
                               )
        d.addCallbacks(self._get_response, self._get_response_error)
        d.addCallbacks(self._get_result, self._get_result_error)
        return d
        
    def _get_response(self, response, max_length=102400):
        response_body = TwilioResponseBody(response, max_length)
        response.deliverBody(response_body)
        return response_body.deferred
    
    def _get_response_error(self, error):
        logging.debug('_get_response_error')
        logging.error(error)        
        raise ErrorResponseException()
        
    def _get_result(self, response):     
        logging.debug('get_result')   
        d = Deferred()
        res = None
        if response:
            body = response.body.decode('utf-8')
            res = json.loads(body)
        d.callback(res)
        return d
                
    def _get_result_error(self, error_response):
        logging.debug('get_result_error')
        if not error_response.check(ErrorResponseException):
            body = error_response.value.body.decode('utf-8')
            res = json.loads(body)
            raise ErrorResultException(res)
        else:
            raise ErrorResponseException()
        
if __name__ == "__main__":
    def test_sample():
        def print_response(res):
            print res
            
        def error_response(res):
            print 'Error sent', res
            if res.check(ErrorResultException):
                print res.value.message
        
        account_sid = "YOUR_ACCOUNT"
        auth_token = "AUTH_TOKEN"
        auth = {"account_sid": account_sid, "auth_token": auth_token}
        message = TwilioSMSMessage(auth)
        from_number = "FROM"
        to_number = "TO"
        sms = {
                   'body': u'đù má',
                   'from': from_number,
                   'to': to_number,
                   }
        d = message.send_message(sms)
        d.addCallback(print_response)
        d.addErrback(error_response)
    for _ in range(2):
        test_sample()
    reactor.run()