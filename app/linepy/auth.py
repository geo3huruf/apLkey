# -*- coding: utf-8 -*-
from typing import Optional

import urllib, base64, os
import axolotl_curve25519 as curve

from .server import Server
from .callback import Callback
from thrift.transport.THttpClient import THttpClient
from thrift.protocol.TCompactProtocol import TCompactProtocolAcceleratedFactory

from line.ttypes import *
from line import SecondaryQrCodeLoginService, SecondaryQrCodeLoginPermitNoticeService

class Auth(object):
    isLogin = False

    accessToken: str = None
    certificate: str = None

    def __init__(self, appType: Optional[str] = None, secondary: bool = False):
        if appType == 'CHROMEOS':
            self.appName = "chrome"
            self.secondary = False
        self.server = Server(self.appName, self.secondary)
        self.callback = Callback(self.__defaultCallback)
        self.systemName = None

    def loginWithQrCode(self):
        if self.systemName is None:
            self.systemName = self.server.systemName
        self.tauth = self.createSession(self.server.LINE_LOGIN_REQUEST_V1,
                                   SecondaryQrCodeLoginService.Client)
        sessionId   = self.tauth.createSession(CreateQrSessionRequest()).authSessionId
        callbackURL = self.tauth.createQrCode(CreateQrCodeRequest(sessionId)).callbackUrl
        secret      = self.genE2EESecret()
        self.callback.QrUrl(f'{callbackURL}{secret}')
        self.server.set_accessToken('')
        self.checkVerified = self.createSession(self.server.LINE_LOGIN_CHECK_V1,
                                         SecondaryQrCodeLoginPermitNoticeService.Client)
        self.checkVerified.checkQrCodeVerified(CheckQrCodeVerifiedRequest(sessionId))
        try:
            self.tauth.verifyCertificate(VerifyCertificateRequest(sessionId, None))
            return
        except SecondaryQrCodeException:
            pinCode = self.tauth.createPinCode(CreatePinCodeRequest(sessionId)).pinCode
            self.callback.PinVerified(pinCode)
            self.checkVerified.checkPinCodeVerified(CheckPinCodeVerifiedRequest(sessionId))
        lReq = self.tauth.qrCodeLogin(QrCodeLoginRequest(sessionId, self.systemName, True))
        self.loginWithAuthToken(lReq.accessToken)

    def loginWithAuthToken(self, authToken=None):
        if authToken is None:
            raise Exception('Please provide Auth Token')
        if self.appName is None:
            self.appName=self.server.appName
        self.server.set_accessToken(authToken)
        self.accessToken = authToken

    def genE2EESecret(self):
        private_key = curve.generatePrivateKey(os.urandom(32))
        public_key = curve.generatePublicKey(private_key)

        secret = urllib.parse.quote(base64.b64encode(public_key).decode())
        version = 1
        return f"?secret={secret}&e2eeVersion={version}"
    
    def createTransport(self, endPoint):
        http = THttpClient(self.server.LINE_HOST_DOMAIN + endPoint)
        http.setCustomHeaders(self.server.Headers())
        return http
        
    def createSession(self, url, client):
        self.trans = self.createTransport(url)
        self.proto = TCompactProtocolAcceleratedFactory().getProtocol(self.trans)
        return client(self.proto)
    
    def __defaultCallback(self, str):
        print(str)