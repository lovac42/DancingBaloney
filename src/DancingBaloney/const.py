# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


from .lib.com.lovac42.anki.version import POINT_VERSION
from .utils import getAbsolutePath, setWebExports


# Required by top toolbar for setting style sheets.
ANKI21_OLD = POINT_VERSION < 20

ADDON_NAME = "DancingBaloney"

RE_BG_IMG_EXT = "*.gif *.png *.apng *.jpg *.jpeg *.svg *.ico *.bmp"

RE_MEDIA_TYPE = r".*\.(gif|a?png|jpe?g|svg|ico|bmp|css)$"

MOD_DIR = setWebExports(RE_MEDIA_TYPE)

ADDON_PATH = getAbsolutePath(__file__)

DEFAULT_TRANSFORM = (0,100,0,0,1,1)

CB_CHECKED = -1
CB_UNCHECKED = 1
