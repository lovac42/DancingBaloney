# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import os
from aqt import mw


def getBGImage(webview, path):
    return '''
<style>
body {
  background: url("%s") no-repeat center center fixed;
  background-size: cover;
}
</style>''' % webview.webBundlePath(path).replace(r"/_anki/","/_addons/")


def setWebExports():
    MOD_ABS,_ = os.path.split(__file__)
    MOD_DIR = os.path.basename(MOD_ABS)
    mw.addonManager._webExports[MOD_DIR] = '.*\.(gif|png|jpe?g|bmp)$'
    return MOD_DIR

