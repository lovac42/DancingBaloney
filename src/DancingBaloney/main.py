# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import sys
import aqt
from aqt import mw
from anki.hooks import wrap, addHook

from .lib.com.lovac42.anki.version import CCBC, ANKI21

from .const import *
from .utils import *
from .style import *

from .config import Config
conf = Config(ADDON_NAME)

from .gui import Manager
mang = Manager(conf)


beforeResetState = "deckBrowser"


def bundledCSS(webview, fname, _old):
    ret = None
    theme = conf.get("theme")

    if not isinstance(webview, aqt.editor.EditorWebView):
        if mw.state == "resetRequired" and fname == "webview.css":
        # Filter out webview.css call by browser editor, editor, and clayout
            for i in range (1,12):
            #Filter out webview called from resetState in mw only
                try:
                    if "resetRequiredState" in sys._getframe(i).f_code.co_name:
                        fname = "resetRequired.css"
                except ValueError:
                    break
        elif fname == "reviewer.css":
        #Filter out reviewer.css called by clayout and preview
            for i in range (1,16):
                try:
                    if sys._getframe(i).f_code.co_name in (
                        "_onCardLayout", "_setupPreviewWebview",
                        "renderPreview", "_renderPreview"
                    ):
                        return _old(webview, fname)
                except ValueError:
                    break


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
        "toolbar-bottom.css","reviewer-bottom.css",
        "resetRequired.css"
    ):
        color = conf.get("theme_bg_color", "")
        bg = f"{mw.state}_{fname[:-4]}.jpg"

        # Note: Can't change opacity on different versions/platforms.
        # So theme_opacity is limited to the main view only.
        if "bottom" in fname:
            op = 100
            color = ""
        elif mw.state == "review":
            op = conf.get("theme_rev_opacity", 80)
        elif mw.state == "resetRequired":
            if beforeResetState == 'review':
                op = conf.get("theme_rev_opacity", 80)
            else:
                op = conf.get("theme_opacity", 90)
                bg = "alt_" + bg
            op = max(1, op-10)
        else:
            op = conf.get("theme_opacity", 90)

        css = getCSS(webview, color, bg, op, DEFAULT_TRANSFORM, theme=theme)

        btn_bg = f"btn_{bg}"
        css += getButtonImage(webview, MOD_DIR, btn_bg, 80, theme)

        if "deckbr" in fname:
            gear_bg = f"gear.png"
            css += getGearImage(webview, MOD_DIR, gear_bg, theme)

    return css, fname



def manualLoader(webview, fname):
    css = ""

    if mw.state == "review" and conf.get("show_bg_in_reviewer", 1)==1:
        # One or the other, targets different versions
        clearBackground(webview)
        clearBackground(mw.toolbar.web)

    elif fname == "toolbar.css" and mw.state == "deckBrowser":
        if not conf.get("top_toolbar_bg_img"):
            clearBackground(mw.toolbar.web)
        color = conf.get("top_toolbar_bg_color", "#F6FFE9")
        if color:
            css = setBGColor(webview, color, top=True)
        #Note: Images for toolbar is set in onAfterStateChange
        #      after page has been loaded.

    elif fname in (
        "deckbrowser.css","overview.css",
        "resetRequired.css","reviewer.css"
    ):
        #TODO: sep settings for overview
        color = conf.get("bg_color", "#3B6EA5") #win2k default blue
        bg = conf.get("bg_img","sheep.gif")

        if mw.state == "review":
            op = conf.get("bg_reviewer_opacity", 80)
        elif mw.state == "resetRequired":
            if beforeResetState == 'review':
                op = conf.get("bg_reviewer_opacity", 80)
            else:
                op = conf.get("bg_img_opacity", 90)
                bg = "alt_" + bg
            op = max(1, op-10)
        else:
            op = conf.get("bg_img_opacity", 90)

        r = conf.get("mw_img_rotate", 0)
        z = conf.get("mw_img_zoom", 100)
        tx = conf.get("mw_img_translateX", 0)
        ty = - conf.get("mw_img_translateY", 0)
        sx = conf.get("mw_img_scaleX", 1)
        sy = conf.get("mw_img_scaleY", 1)
        css = getCSS(webview, color, bg, op, (r,z,tx,ty,sx,sy))

        gear_bg = conf.get("gear_img")
        css += getGearImage(webview, MOD_DIR, gear_bg)

    elif fname == "toolbar-bottom.css":
        color = conf.get("bottom_toolbar_bg_color", "#3B6EA5")
        bg = conf.get("bottom_toolbar_bg_img")
        op = conf.get("bottom_toolbar_bg_img_opacity", 100)
        css = getCSS(webview, color, bg, op, DEFAULT_TRANSFORM)

    custom_css = conf.get(f"custom_{fname[:-4]}_style")
    return css, custom_css


def onAfterStateChange(newS, oldS, *args):
    "This is needed to get around an issue with setting images on the toolbar."

    global beforeResetState
    beforeResetState = newS

    bg = None
    theme = conf.get("theme")
    if theme:
        bg = f"{newS}_toolbar.jpg"
        theme = f"theme/{theme}"
    elif newS == "review" and conf.get("show_bg_in_reviewer", 1)==1:
        clearBackground(mw.toolbar.web)
    else:
        bg = conf.get("top_toolbar_bg_img")
        theme = "user_files"

    #TODO: make theme specific
    #Sets menubar colors
    color = conf.get("menubar_txt_color")
    bgColor = conf.get("menubar_bg_color")
    setMenubarColor(color, bgColor)

    if bg:
        setImageWithJS(mw.toolbar.web, MOD_DIR, bg, theme)



# ===== Toolbar ========

def hideBottomToolbar(self, buf, *args, **kwargs):
    old = kwargs.pop('_old')
    if not conf.get("hide_bottom_toolbar", CB_UNCHECKED)==CB_CHECKED:
        return old(self, buf, *args, **kwargs)

    self.web.setFixedHeight(0)
    self.web.bundledCSS("toolbar.css") #trigger top toolbar update

    block = (self._centerBody % buf) + """
<style>
#header {
  position: fixed;
  bottom: 0;
  padding: 9px;
}

button{
    border: solid 1px rgba(0, 0, 0, 0.2);
    border-radius: 4px;
    outline: none;
    cursor: pointer;
    padding: 1px;
    margin-right: 2px;
    min-width: 80px;
    opacity: .8;
}
</style>
"""
    block = block.replace("'","\\'").replace("\n","")
    js = f"""$(document.body).append('{block}');"""
    self.mw.web.eval(js)



aqt.toolbar.BottomBar.draw = wrap(
    aqt.toolbar.BottomBar.draw,
    hideBottomToolbar,
    "around"
)


# ===== EXEC ===========

def onProfileLoaded():
    aqt.webview.AnkiWebView.bundledCSS = wrap(
        aqt.webview.AnkiWebView.bundledCSS,
        bundledCSS,
        "around"
    )
    if conf.get("hide_bottom_toolbar", CB_UNCHECKED)==CB_CHECKED:
        mw.progress.timer(100,
            lambda:mw.bottomWeb.setFixedHeight(0),
            False
        )
    mw.reset(True)
    addHook(f"{ADDON_NAME}.configUpdated", lambda:mw.reset(True))

#reloads with config.json data
addHook("profileLoaded", onProfileLoaded)
addHook('afterStateChange', onAfterStateChange)
