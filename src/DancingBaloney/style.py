# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import os
from aqt import mw

from .const import *
from .lib.com.lovac42.anki.version import CCBC, ANKI21


JS_CLEAR_BG = "$(document.body).css('background','');"


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
  position: fixed;
  z-index: -99;
  will-change: transform;
  transform: rotate(%ddeg) scale(%f) translate(%d%%,%d%%) scaleX(%d) scaleY(%d);
}
'''


CSS_BUTTON = '''
button {
  background: url("%s") !important;
  opacity: %f;
  z-index: -99;
}
'''


#CSS3 only
CSS_GEAR = '''
img.gears {
  content:url("%s");
}
'''


def setImageWithJS(webview, folder, img, theme="user_files"):
    url = _getImgUrl(webview, folder, img, theme)
    if not url:
        return
    js = f'''$(document.body).css('background','url("{url}") no-repeat center center fixed').css('background-size','cover');'''
    webview.eval(js)


def getBGImage(webview, folder, img, opacity, transform, theme="user_files"):
    url = _getImgUrl(webview, folder, img, theme)
    if not url:
        return ""
    rotate,zoom,tx,ty,sx,sy = transform
    return CSS_BODY % (url, opacity/100, rotate, zoom/100, tx, ty, sx, sy)


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


def setBGColor(webview, color, top=True):
    if not color and top:
        clearBackground(webview)
        clearBackground(mw.toolbar.web)
        return ""
    if top and (CCBC or ANKI21_OLD):
        js = f"$(document.body).css('background-color','{color}');"
        webview.eval(js)
        mw.toolbar.web.eval(js)
        return ""
    return f"body {{background-color: {color} !important;}}"


def clearBackground(webview):
    webview.eval(JS_CLEAR_BG)


def getCustomPath(fname, theme="user_files"):
    css = f"{MOD_DIR}/{theme}/{fname}"
    try:
        import ccbc
        return ccbc.utils.readFile(css)
    except ImportError:
        url = _getImgUrl(mw.web, MOD_DIR, fname, theme)
        if url:
            return f'<link rel="stylesheet" type="text/css" href="{url}">'



def _getImgUrl(webview, folder, fname, theme):
    if fname and os.path.exists(f"{ADDON_PATH}/{theme}/{fname}"):
        path = f"{folder}/{theme}/{fname}"
        url = webview.webBundlePath(path)
        if ANKI21:
            url = url.replace(r"/_anki/","/_addons/")
        return url


def getCSS(webview, color, img, opacity, trans, theme="user_files"):
    css = setBGColor(webview, color, top=False)
    if img:
        css += getBGImage(
            webview, MOD_DIR, img, 
            opacity, trans, theme
        )
    return css

def setMenubarColor(tc, bc):
    css = f"color:{tc};" if tc else ""
    css += f"background-color:{bc};" if bc else ""
    mw.form.menubar.setStyleSheet(css)
