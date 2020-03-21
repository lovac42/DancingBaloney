# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import os
from aqt import mw

from .const import *
from .lib.com.lovac42.anki.version import CCBC, ANKI21


JS_CLEAR_BG = "$(document.body).css('background-color','');"

CSS_BODY = '''
body::before {
  background: url("%s") no-repeat center center fixed !important;
  background-size: cover !important;
  opacity: %f;
  content: "";
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  position: absolute;
  z-index: -99;
}
'''

CSS_BUTTON = '''
button {
  background: url("%s") !important;
  opacity: %f;
  z-index: -99;
}
'''


CSS_GEAR = '''
img.gears {
  content:url("%s");
}
'''


def setToolbarImage(webview, folder, img, theme="user_files"):
    url = _getImgUrl(webview, folder, img, theme)
    if not url:
        return
    js = f'''$(document.body).css('background','url("{url}") no-repeat center center fixed').css('background-size','cover');'''
    webview.eval(js)


def getBGImage(webview, folder, img, opacity, theme="user_files"):
    url = _getImgUrl(webview, folder, img, theme)
    if not url:
        return ""
    return CSS_BODY % (url, opacity/100)


def getGearImage(webview, folder, img, theme="user_files"):
    url = _getImgUrl(webview, folder, img, theme)
    if not url:
        return ""
    return CSS_GEAR % (url)


def getButtonImage(webview, folder, img, opacity, theme="user_files"):
    url = _getImgUrl(webview, folder, img, theme)
    if not url:
        return ""
    return CSS_BUTTON % (url, opacity/100)


def setBGColor(color, top=True):
    if top and (CCBC or ANKI21_OLD):
        js = f"$(document.body).css('background-color','{color}');"
        mw.toolbar.web.eval(js)
        return ""
    return f"body {{background: {color} !important;}}"


def clearBGColor(webview):
    webview.eval(JS_CLEAR_BG)


def _getImgUrl(webview, folder, img, theme):
    if os.path.exists(f"{ADDON_PATH}/{theme}/{img}"):
        path = f"{folder}/{theme}/{img}"
        url = webview.webBundlePath(path)
        if ANKI21:
            url = url.replace(r"/_anki/","/_addons/")
        return url
