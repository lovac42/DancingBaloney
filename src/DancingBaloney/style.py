# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


from aqt import mw

from .const import *
from .lib.com.lovac42.anki.version import CCBC, ANKI21

BODY_CSS = '''
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


def getBGImage(webview, folder, img, opacity):
    path = f"{folder}/user_files/{img}"
    url = webview.webBundlePath(path)
    if ANKI21:
        url = url.replace(r"/_anki/","/_addons/")
    return BODY_CSS % (url, opacity/100)


def clearBGColor():
    js="$(document.body).css('background-color','');"
    mw.toolbar.web.eval(js)


def setBGColor(color, top=True):
    if top and (CCBC or ANKI21_OLD):
        js = f"$(document.body).css('background-color','{color}');"
        mw.toolbar.web.eval(js)
        return ""
    return f"body {{background: {color} !important;}}"

