pyuic5 settings.ui -o out.py

echo # -*- coding: utf-8 -*-> settings.py
echo # Copyright (C) 2020 Lovac42>> settings.py
echo # Support: https://github.com/lovac42/DancingBaloney>> settings.py
echo # License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html>> settings.py
echo.>> settings.py
echo # Form implementation generated from reading ui file 'settings.ui'>> settings.py
echo #>> settings.py
echo # Created by: PyQt5 UI code generator 5.12.2>> settings.py
echo #>> settings.py
echo # WARNING! All changes made in this file will be lost!>> settings.py
echo.>> settings.py
echo from ..lib.com.lovac42.anki.version import ANKI21 >> settings.py
echo.>> settings.py
echo if ANKI21:>> settings.py
echo     from PyQt5 import QtCore, QtWidgets>> settings.py
echo else:>> settings.py
echo     from PyQt4 import QtCore, QtGui as QtWidgets>> settings.py

findstr /V "# PyQt5" out.py>>settings.py

del out.py
move settings.py ..\src\DancingBaloney\forms
