# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import aqt
from aqt import mw
from anki.hooks import wrap, addHook

from .const import *
from .utils import *
from .style import *
from .config import Config

from .lib.com.lovac42.anki.version import CCBC

conf = Config(ADDON_NAME)


def bundledCSS(webview, fname, _old):
    css = ""

    if mw.state == "review":
        # TODO: Fix for new version, it does not clear color on toolbar.
        clearBGColor()

    elif fname == "toolbar.css" and mw.state == "deckBrowser":
        color = conf.get("top_toolbar_bg_color", "#F6FFE9")
        css = setBGColor(color, top=True)

    elif fname in ("deckbrowser.css","overview.css"):
        bg = conf.get("bg_img","sheep.gif")
        css = getBGImage(webview, MOD_DIR, bg)

    elif fname == "toolbar-bottom.css":
        tool_img = conf.get("bottom_toolbar_bg_img", "#1E2438")
        if tool_img:
            css = getBGImage(webview, MOD_DIR, tool_img)
        else:
            color = conf.get("bottom_toolbar_bg_color")
            css = setBGColor(color, top=False)

    # Custom style sheets
    custom_css = conf.get(f"custom_{fname[:-4]}_style")
    if custom_css:
        cc = f"{MOD_DIR}/user_files/{custom_css}"
        try:
            import ccbc
            ret = ccbc.utils.readFile(cc)
        except ImportError:
            ret = _old(webview, cc).replace(r"/_anki/","/_addons/")
    else:
        ret = _old(webview, fname)

    if css:
        if CCBC:
            return f"{ret}\n{css}"
        return f"{ret}\n<style>{css}</style>"
    return ret


# ===== EXEC ===========

MOD_DIR = setWebExports(r".*\.(gif|png|jpe?g|bmp|css)$")

aqt.webview.AnkiWebView.bundledCSS = wrap(
    aqt.webview.AnkiWebView.bundledCSS,
    bundledCSS,
    "around"
)

#reloads with config.json data
addHook("profileLoaded", lambda:mw.reset(True))
addHook(f"{ADDON_NAME}.configUpdated", lambda:mw.reset(True))
