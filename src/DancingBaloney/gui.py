# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/DancingBaloney
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import os
from aqt.qt import *
from aqt import mw
from aqt.utils import getFile

from .lib.com.lovac42.anki.gui import toolbar
from .forms.settings import Ui_Settings
from .forms import getcolor
from .const import ADDON_PATH

from .lib.com.lovac42.anki.version import CCBC


class Manager:
    shown = False

    def __init__(self, conf):
        self.conf = conf
        self.setupMenu()

    def setupMenu(self):
        m = toolbar.getMenu(mw, "&View")
        a = QAction("Wallpaper", mw)
        a.triggered.connect(self.show)
        m.addAction(a)

    def show(self):
        if not self.shown:
            self.shown = True
            s = SettingsDialog(self.conf, self.reset)
            s.show()

    def reset(self):
        self.shown = False



class SettingsDialog(QDialog):
    lastColor = QColor("white") #initialize color wheel on blank fields
    timer = None

    def __init__(self, conf, callback):
        QDialog.__init__(self, mw, Qt.Window)
        mw.setupDialogGC(self)
        self.conf = conf
        self.cleanup = callback
        self.setupDialog()
        self.loadConfigData()
        self.setupConnections()


    def setupDialog(self):
        self.setWindowTitle("Wallpaper Settings")
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setFocusPolicy(Qt.StrongFocus)
        self.tabWidget.setObjectName("tabWidget")
        self.form = Ui_Settings()
        self.form.setupUi(self.tabWidget)

        if CCBC:
            self.form.mw_rotate_label.setEnabled(False)
            self.form.mw_rotate_slider.setEnabled(False)
            self.form.mw_rotate_value.setEnabled(False)
            self.form.mw_zoom_label.setEnabled(False)
            self.form.mw_zoom_slider.setEnabled(False)
            self.form.mw_zoom_value.setEnabled(False)
            self.form.mw_translateX_slider.setEnabled(False)
            self.form.mw_translateX_value.setEnabled(False)
            self.form.mw_translateY_slider.setEnabled(False)
            self.form.mw_translateY_value.setEnabled(False)
            self.form.mw_flipH_checkbox.setEnabled(False)
            self.form.mw_flipV_checkbox.setEnabled(False)

    def reject(self):
        self.accept()

    def accept(self):
        self.conf.save()
        QDialog.accept(self)
        self.cleanup()

    def setupConnections(self):
        f = self.form

        # ComboBoxes -----------
        f.theme_combobox.currentIndexChanged.connect(
            self._updateComboBox
        )

        # Checkboxes
        f.mw_flipH_checkbox.stateChanged.connect(
            lambda:self._updateCheckbox(f.mw_flipH_checkbox, "mw_img_scaleX")
        )
        f.mw_flipV_checkbox.stateChanged.connect(
            lambda:self._updateCheckbox(f.mw_flipV_checkbox, "mw_img_scaleY")
        )

        # Sliders -----------------------
        controller = {
          # Themes ----------------
            f.theme_opacity_slider : (f.theme_opacity_value, "theme_opacity"),
            f.theme_rev_opacity_slider : (f.theme_rev_opacity_value, "theme_rev_opacity"),
          # Toolbar ----------------
            f.mw_opacity_slider : (f.mw_opacity_value, "bg_img_opacity"),
            f.btm_opacity_slider : (f.btm_opacity_value, "bottom_toolbar_bg_img_opacity"),
            f.mw_rotate_slider : (f.mw_rotate_value, "mw_img_rotate", "% 5d°"),
            f.mw_zoom_slider : (f.mw_zoom_value, "mw_img_zoom"),
            f.mw_translateX_slider : (f.mw_translateX_value, "mw_img_translateX", "%d"),
            f.mw_translateY_slider : (f.mw_translateY_value, "mw_img_translateY", "%d"),
        }
        for slider,args in controller.items():
            s = slider.value()
            slider.valueChanged.connect(
                lambda s=s,args=args:self._updateSliderLabel(s, *args)
            )


        # LineEdits -----------------------
        controller = {
          # Themes ----------------
            f.theme_color_input : ("theme_bg_color",),
          # Menu Toolbar -----------
            f.menubar_text_input : ("menubar_txt_color",),
            f.menubar_color_input : ("menubar_bg_color",),
          # Toolbar ----------------
            f.toolbar_color_input : ("top_toolbar_bg_color",),
            f.toolbar_image_input : ("top_toolbar_bg_img",),
            f.mw_color_input : ("bg_color",),
            f.mw_image_input : ("bg_img",),
            f.mw_gear_input : ("gear_img",),
          # Bottom Toolbar ----------
            f.btm_color_input : ("bottom_toolbar_bg_color",),
            f.btm_image_input : ("bottom_toolbar_bg_img",),
        }
        for ed,args in controller.items():
            t = ed.text()
            ed.textChanged.connect(
                lambda t=t,args=args:self._updateLineEdit(t,*args)
            )


        # Image Buttons -----------------------
        controller = {
            f.toolbar_image_button : (f.toolbar_image_input,),
            f.mw_image_button : (f.mw_image_input,),
            f.mw_gear_button : (f.mw_gear_input,),
            f.btm_image_button : (f.btm_image_input,),
        }
        for btn,args in controller.items():
            # 'a' is used to get around an issue
            # with pything binding
            btn.clicked.connect(
                lambda a="a",args=args:self._getFile(a,*args)
            )


        # Color Buttons -----------------------
        controller = {
            f.theme_color_button : (f.theme_color_input,),
            f.toolbar_color_button : (f.toolbar_color_input,),
            f.mw_color_button : (f.mw_color_input,),
            f.btm_color_button : (f.btm_color_input,),
            f.menubar_text_button : (f.menubar_text_input,),
            f.menubar_color_button : (f.menubar_color_input,),
        }
        for btn,args in controller.items():
            btn.clicked.connect(
                lambda a="a",args=args:self._chooseColor(a,*args)
            )


    def loadConfigData(self):
        f = self.form

        # Themes ------------------
        themeList = self._getThemes()
        f.theme_combobox.addItem("")
        f.theme_combobox.addItems(themeList)
        try:
            n = themeList.index(self.conf.get("theme")) + 1
            self.tabWidget.setCurrentIndex(len(self.tabWidget)-1)
        except ValueError:
            n = 0
            self.tabWidget.setCurrentIndex(0)
        f.theme_combobox.setCurrentIndex(n)

        n = self.conf.get("theme_opacity", 100)
        f.theme_opacity_slider.setValue(n)
        f.theme_opacity_value.setText("% 5d%%"%n)

        n = self.conf.get("theme_rev_opacity", 100)
        f.theme_rev_opacity_slider.setValue(n)
        f.theme_rev_opacity_value.setText("% 5d%%"%n)

        s = self.conf.get("theme_bg_color", "")
        f.theme_color_input.setText(s)

        # Toolbar ----------------
        s = self.conf.get("top_toolbar_bg_color", "")
        f.toolbar_color_input.setText(s)
        s = self.conf.get("top_toolbar_bg_img", "")
        f.toolbar_image_input.setText(s)

        # MW ----------------
        s = self.conf.get("bg_color", "")
        f.mw_color_input.setText(s)
        s = self.conf.get("bg_img", "")
        f.mw_image_input.setText(s)
        n = self.conf.get("bg_img_opacity", 100)
        f.mw_opacity_slider.setValue(n)
        f.mw_opacity_value.setText("% 5d%%"%n)
        s = self.conf.get("gear_img", "")
        f.mw_gear_input.setText(s)

        # Bottom Toolbar ----------
        s = self.conf.get("bottom_toolbar_bg_color", "")
        f.btm_color_input.setText(s)
        s = self.conf.get("bottom_toolbar_bg_img", "")
        f.btm_image_input.setText(s)
        n = self.conf.get("bottom_toolbar_bg_img_opacity", 100)
        f.btm_opacity_slider.setValue(n)
        f.btm_opacity_value.setText("% 5d%%"%n)
        n = self.conf.get("mw_img_rotate", 0)
        f.mw_rotate_slider.setValue(n)
        f.mw_rotate_value.setText("% 5d°"%n)
        n = self.conf.get("mw_img_zoom", 100)
        f.mw_zoom_slider.setValue(n)
        f.mw_zoom_value.setText("% 5d%%"%n)
        n = self.conf.get("mw_img_translateX", 0)
        f.mw_translateX_slider.setValue(n)
        f.mw_translateX_value.setText(str(n))
        n = self.conf.get("mw_img_translateY", 0)
        f.mw_translateY_slider.setValue(n)
        f.mw_translateY_value.setText(str(n))
        n = self.conf.get("mw_img_scaleX", False)
        f.mw_flipH_checkbox.setChecked(n)
        n = self.conf.get("mw_img_scaleY", False)
        f.mw_flipV_checkbox.setChecked(n)

        # Menubar -----------
        s = self.conf.get("menubar_txt_color", "")
        f.menubar_text_input.setText(s)
        s = self.conf.get("menubar_bg_color", "")
        f.menubar_color_input.setText(s)

    def _updateLineEdit(self, text, key):
        self.conf.set(key, text)
        self._refresh()

    def _updateComboBox(self):
        self.conf.set("theme",
            self.form.theme_combobox.currentText())
        self._refresh(150)

    def _updateSliderLabel(self, num, label, key, format="% 5d%%"):
        label.setText(format%num)
        self.conf.set(key, num)
        self._refresh()

    def _getThemes(self):
        d = f"{ADDON_PATH}/theme"
        return [x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))]

    def _getFile(self, pad, lineEditor):
        def setWallpaper(path):
            f = path.split("user_files/")[-1]
            lineEditor.setText(f)

        f = getFile(mw, "Wallpaper",
            cb=setWallpaper,
            dir=f"{ADDON_PATH}/user_files"
        )

    def _chooseColor(self, pad, lineEditor):
        def liveColor(qcolor):
            if qcolor.isValid():
                self.lastColor=qcolor
                lineEditor.setText(qcolor.name())

        diag=QDialog(self)
        form=getcolor.Ui_Dialog()
        form.setupUi(diag)
        cor = lineEditor.text()
        if QColor.isValidColor(cor):
            form.color.setCurrentColor(QColor(cor))
        else:
            form.color.setCurrentColor(self.lastColor)
        form.color.currentColorChanged.connect(liveColor)
        diag.show()

    def _updateCheckbox(self, func, key):
        n = -1 if func.isChecked() else 1
        self.conf.set(key, n)
        self._refresh()

    def _refresh(self, ms=100):
        if self.timer:
            self.timer.stop()
        self.timer = mw.progress.timer(
            ms, lambda:mw.reset(True), False)
