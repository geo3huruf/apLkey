# -*- coding: utf-8 -*-
from typing import List, Optional

import platform

LINE_USER_AGENTS = {
    "chrome": "Line/2.3.8",
}
LINE_APPLICATIONS = {
    "chrome": "CHROMEOS\t2.3.8\tChromeOS\t83.0",
}

LineApplicationType = list(LINE_APPLICATIONS.keys())


class Config(object):
    LINE_HOST_DOMAIN            = 'https://legy-jp-addr.line.naver.jp'
    LINE_OBS_DOMAIN             = 'https://obs-sg.line-apps.com'
    LINE_LOGIN_REQUEST_V1       = "/acct/lgn/sq/v1"
    LINE_LOGIN_CHECK_V1         = "/acct/lp/lgn/sq/v1"

    accessToken: str = None

    def __init__(self, appType: str = None, secondary: bool = False):
        if appType not in LineApplicationType:
            raise Exception("Undefined application type.")

        self.appName        = LINE_APPLICATIONS[appType]
        self.userAgent      = LINE_USER_AGENTS[appType]
        self.systemName     = str(platform.python_implementation()) + "-" + str(platform.python_version())

        if secondary:
            self.appName   += ";SECONDARY"