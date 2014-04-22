'''
Created on Apr 22, 2014

@author: leen
'''
from twisted.internet.ssl import ClientContextFactory, SSL


class SSLVerifiedClientContextFactory(ClientContextFactory):
    
    def __init__(self, verify=True, verify_location='/etc/ssl/certs/'):
        """
        verify: SSL certificate verification
        verify_location: path to the folder keep cert files
        """
        self._verify = verify
        self._verify_location = verify_location
    
    def getContext(self, hostname, port):
        ctx = ClientContextFactory.getContext(self)
        ctx.set_options(SSL.OP_NO_SSLv2)
        if self._verify:
            ctx.load_verify_locations(None, self._verify_location)
            ctx.set_verify(SSL.VERIFY_PEER|SSL.VERIFY_FAIL_IF_NO_PEER_CERT, self._verifyCert)        
        return ctx
    
    def _verifyCert(self, connection, x509, errno, depth, verifyOK):
        return verifyOK
