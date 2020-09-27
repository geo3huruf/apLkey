# -*- coding: utf-8 -*-
from .auth import Auth
from .server import Server

class LINE(Auth):
    def __init__(self, idOrAuthToken=None, passwd=None, **kwargs):
        self.appType = kwargs.pop('appType', None)
        self.secondary = kwargs.pop('secondary', False)
        Auth.__init__(self, self.appType, self.secondary)
        if not (idOrAuthToken or idOrAuthToken and passwd):
            self.loginWithQrCode()
        elif idOrAuthToken and not passwd:
            self.loginWithAuthToken(idOrAuthToken)
        self.__initAll()

    def __initAll(self):
        pass