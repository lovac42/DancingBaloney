# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import aqt
from aqt import mw
from anki.hooks import wrap, addHook

from .utils import *
from .const import *
from .config import Config

from .lib.com.lovac42.anki.version import CCBC

conf = Config(ADDON_NAME)


def bundledCSS(webview, fname, _old):
    css = ""
    ret = _old(webview, fname)

    if mw.state == "review":
        # TODO: Fix for new version, it does not clear color on toolbar.
        js="$(document.body).css('background-color','');"
        mw.toolbar.web.eval(js)

    elif fname == "toolbar.css" and mw.state == "deckBrowser":
        color = conf.get("top_toolbar_bg_color", "#F6FFE9")
        if CCBC or ANKI21_OLD:
            js = f"$(document.body).css('background-color','{color}');"
            mw.toolbar.web.eval(js)
        else:
            css = f"body {{background: {color} !important;}}"

    elif fname in ("deckbrowser.css","overview.css"):
        bg = conf.get("bg_img","sheep.gif")
        img = f"{MOD_DIR}/user_files/{bg}"
        css = getBGImage(webview, img)

    elif fname == "toolbar-bottom.css":
        tool_img = conf.get("bottom_toolbar_bg_img", "#1E2438")
        if tool_img:
            img = f"{MOD_DIR}/user_files/{tool_img}"
            css = getBGImage(webview, img)
        else:
            color = conf.get("bottom_toolbar_bg_color")
            css = f"body {{background: {color} !important;}}"

    if CCBC:
        return f"{ret}\n{css}"
    return f"{ret}\n<style>{css}</style>"


# ===== EXEC ===========

MOD_DIR = setWebExports(r".*\.(gif|png|jpe?g|bmp)$")

aqt.webview.AnkiWebView.bundledCSS = wrap(
    aqt.webview.AnkiWebView.bundledCSS,
    bundledCSS,
    "around"
)

#reloads with config.json data
addHook("profileLoaded", lambda:mw.reset(True))
addHook(f"{ADDON_NAME}.configUpdated", lambda:mw.reset(True))
