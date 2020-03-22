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

from .lib.com.lovac42.anki.version import CCBC, ANKI21

from .config import Config
conf = Config(ADDON_NAME)

from .gui import Manager
mang = Manager(conf)


def bundledCSS(webview, fname, _old):
    ret = None
    theme = conf.get("theme")
    if theme:
        theme = f"theme/{theme}"
        css, custom_css = themeLoader(webview, fname, theme)
    else:
        css, custom_css = manualLoader(webview, fname)
        theme = "user_files"

    # Custom style sheets
    if custom_css:
        ret = getCustomPath(custom_css, theme)
    if ret == None:
        ret = _old(webview, fname)
    if css:
        if CCBC:
            return f"{ret}\n{css}"
        return f"{ret}\n<style>{css}</style>"
    return ret




def themeLoader(webview, fname, theme):
    css = ""
    if fname in (
        "deckbrowser.css","overview.css","reviewer.css",
        "toolbar-bottom.css","reviewer-bottom.css"
    ):
        # Note: Can't change opacity on different versions/platforms.
        # So theme_opacity is limited to the main view only.
        op = 100 if "bottom" in fname else conf.get("theme_opacity", 100)

        bg = f"{mw.state}_{fname[:-4]}.jpg"
        css = getBGImage(webview, MOD_DIR, bg, op, theme)

        btn_bg = f"btn_{bg}"
        css += getButtonImage(webview, MOD_DIR, btn_bg, 80, theme)

        if ANKI21 and "deckbr" in fname:
            gear_bg = f"gear.png"
            css += getGearImage(webview, MOD_DIR, gear_bg, theme)

    return css, fname



def manualLoader(webview, fname):
    css = ""

    if mw.state == "review":
        # TODO: Fix for new version, it does not clear color on toolbar.
        # One or the other, targets different versions
        clearBGColor(webview)
        clearBGColor(mw.toolbar.web)

    elif fname == "toolbar.css" and mw.state == "deckBrowser":
        img = conf.get("top_toolbar_bg_img")
        if not img: #colors css prevent setting images in stateChanged hook
            color = conf.get("top_toolbar_bg_color", "#F6FFE9")
            css = setBGColor(color, top=True)

    elif fname in ("deckbrowser.css","overview.css"):
        bg = conf.get("bg_img","sheep.gif")
        if bg:
            op = conf.get("bg_img_opacity", 100)
            css = getBGImage(webview, MOD_DIR, bg, op)
        else:
            color = conf.get("bg_color", "#3B6EA5")
            css = setBGColor(color, top=False)

        if ANKI21:
            gear_bg = conf.get("gear_img")
            css += getGearImage(webview, MOD_DIR, gear_bg)

    elif fname == "toolbar-bottom.css":
        tool_img = conf.get("bottom_toolbar_bg_img", "#1E2438")
        if tool_img:
            op = conf.get("bottom_toolbar_bg_img_opacity", 100)
            css = getBGImage(webview, MOD_DIR, tool_img, op)
        else:
            color = conf.get("bottom_toolbar_bg_color")
            css = setBGColor(color, top=False)

    custom_css = conf.get(f"custom_{fname[:-4]}_style")
    return css, custom_css


def onAfterStateChange(newS, oldS, *args):
    "This is needed to get around an issue with setting images on the toolbar."
    theme = conf.get("theme")
    if theme:
        bg = f"{newS}_toolbar.jpg"
        theme = f"theme/{theme}"
    else:
        bg = conf.get("top_toolbar_bg_img")
        theme = "user_files"
    if bg:
        setToolbarImage(mw.toolbar.web, MOD_DIR, bg, theme)


# ===== EXEC ===========

def onProfileLoaded():
    aqt.webview.AnkiWebView.bundledCSS = wrap(
        aqt.webview.AnkiWebView.bundledCSS,
        bundledCSS,
        "around"
    )
    mw.reset(True)
    addHook(f"{ADDON_NAME}.configUpdated", lambda:mw.reset(True))

#reloads with config.json data
addHook("profileLoaded", onProfileLoaded)
addHook('afterStateChange', onAfterStateChange)
