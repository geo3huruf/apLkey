# -*- coding: utf-8 -*-

class Callback(object):

    def __init__(self, callback):
        self.callback = callback

    def PinVerified(self, pin):
        self.callback(f"Input {len(pin)} digits pincode on your smartphone in 2 minutes\nPincode: {pin}")

    def QrUrl(self, url, showQr=False):
        if showQr:
            notice = "Or scan this QR "
        else:
            notice = ""
        self.callback(f"Open callback URL on your smartphone in minutes\ncallbackURL: {url}")
        if showQr:
            try:
                import pyqrcode
                url = pyqrcode.create(url)
                self.callback(url.terminal('green', 'white', 1))
            except:
                pass

    def default(self, str):
        self.callback(str)