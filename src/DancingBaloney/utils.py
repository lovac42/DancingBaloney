# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import os
from aqt import mw

from .lib.com.lovac42.anki.version import ANKI21


def getAbsolutePath(f):
    m,_ = os.path.split(f)
    return m

def setWebExports(media_types=""):
    MOD_ABS = getAbsolutePath(__file__)
    if ANKI21:
        MOD_DIR = os.path.basename(MOD_ABS)
        mw.addonManager._webExports[MOD_DIR] = media_types
        return MOD_DIR
    return MOD_ABS

