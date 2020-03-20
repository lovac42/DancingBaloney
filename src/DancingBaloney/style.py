# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


from aqt import mw

from .const import *
from .lib.com.lovac42.anki.version import CCBC


def clearBGColor():
    js="$(document.body).css('background-color','');"
    mw.toolbar.web.eval(js)


def setBGColor(color, top=True):
    if top and (CCBC or ANKI21_OLD):
        js = f"$(document.body).css('background-color','{color}');"
        mw.toolbar.web.eval(js)
        return ""
    return f"body {{background: {color} !important;}}"

