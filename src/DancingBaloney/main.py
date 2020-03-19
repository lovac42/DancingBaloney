# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import aqt
from aqt import mw
from anki.hooks import wrap, addHook

from .utils import *
from .config import Config

try:
    from anki.utils import pointVersion
    OLD_VERSION = pointVersion() < 20
except:
    OLD_VERSION = True



conf = Config("DancingBaloney")


def bundledCSS(webview, fname, _old):
    ret = _old(webview, fname)

    if mw.state == "review":
        # TODO: Fix for new version, it does not clear color on toolbar.
        js="$(document.body).css('background-color','');"
        mw.toolbar.web.eval(js)

    elif fname == "toolbar.css" and mw.state == "deckBrowser":
        c = conf.get("top_toolbar_bg_color", "#F6FFE9")
        if not OLD_VERSION:
            ret += "<style>body {background: %s;}</style>"%c
        else:
            js="$(document.body).css('background-color','%s');"%c
            mw.toolbar.web.eval(js)

    elif fname in ("deckbrowser.css","overview.css"):
        bg = conf.get("bg_img","sheep.gif")
        img = "%s/user_files/%s"%(MOD_DIR, bg)
        ret += getBGImage(webview, img)

    elif fname == "toolbar-bottom.css":
        tool_img = conf.get("bottom_toolbar_bg_img", "#1E2438")
        if tool_img:
            img = "%s/user_files/%s"%(MOD_DIR, tool_img)
            ret += getBGImage(webview, img)
        else:
            c = conf.get("bottom_toolbar_bg_color")
            ret += "<style>body {background: %s;}</style>"%c

    return ret


# ===== EXEC ===========

MOD_DIR = setWebExports()

aqt.webview.AnkiWebView.bundledCSS = wrap(
    aqt.webview.AnkiWebView.bundledCSS,
    bundledCSS,
    "around"
)

#reloads with config.json data
addHook("profileLoaded", lambda:mw.reset(True))
