pyuic5 settings.ui -o out.py


type header.py >settings.py

findstr /V "# PyQt5" out.py>>settings.py

del out.py
move settings.py ..\src\DancingBaloney\forms
