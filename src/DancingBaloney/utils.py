# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import os
from aqt import mw

from .lib.com.lovac42.anki.version import ANKI21


BODY_CSS = '''
body {
  background: url("%s") no-repeat center center fixed !important;
  background-size: cover !important;
}
'''


def getBGImage(webview, folder, img):
    path = f"{folder}/user_files/{img}"
    url = webview.webBundlePath(path)
    if ANKI21:
        url = url.replace(r"/_anki/","/_addons/")
    return BODY_CSS % url


def setWebExports(media_types=""):
    MOD_ABS,_ = os.path.split(__file__)
    if ANKI21:
        MOD_DIR = os.path.basename(MOD_ABS)
        mw.addonManager._webExports[MOD_DIR] = media_types
        return MOD_DIR
    return MOD_ABS

