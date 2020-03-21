# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


from .lib.com.lovac42.anki.version import POINT_VERSION
from .utils import getAbsolutePath, setWebExports


# Required by top toolbar for setting style sheets.
ANKI21_OLD = POINT_VERSION < 20

ADDON_NAME = "DancingBaloney"

MOD_DIR = setWebExports(r".*\.(gif|png|jpe?g|bmp|css)$")

ADDON_PATH = getAbsolutePath(__file__)

