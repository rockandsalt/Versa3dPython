# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 11:47:41 2018

@author: inst
"""

import sys
import os
from PyQt5 import QtWidgets
from versa3d.main_window import MainWindow
from versa3d.controller import Versa3dController

def set_up_app(main_win : MainWindow, control : Versa3dController) -> None:
    CONTROLLER.settings.add_setting_signal.connect(
        main_win.populate_printer_drop_down
    )

    CONTROLLER.load_settings()

    printer_setting = control.settings.get_printer(0)
    build_bed_size = printer_setting.build_bed_size.value
    main_win.setup_scene(build_bed_size)

    main_win.change_printer_signal.connect(control.change_printer)
    main_win.change_printhead_signal.connect(control.change_printhead)
    main_win.change_preset_signal.connect(control.change_preset)

    control.update_scene.connect(main_win.resize_scene)
    
    main_win.show_parameter_win.connect(control.edit_preset)
    control.spawn_preset_win_signal.connect(main_win.spawn_setting_window)

    main_win.show_printer_win.connect(control.edit_printer)
    control.spawn_printer_win_signal.connect(main_win.spawn_printer_window)

    main_win.show_printhead_win.connect(control.edit_printhead)
    control.spawn_printhead_win_signal.connect(main_win.spawn_printhead_window)

    main_win.import_obj_signal.connect(control.import_object)
    control.render_signal.connect(main_win.render)
    control.unrender_signal.connect(main_win.unrender)

    main_win.undo_sig.connect(control.undo_stack.undo)
    main_win.redo_sig.connect(control.undo_stack.redo)

    main_win.export_gcode_signal.connect(control.export_gcode)
    main_win.rubber_style.emitter.commit_move.connect(control.transform)

if __name__ == "__main__":
    APP = QtWidgets.QApplication(sys.argv)

    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        BASE_PATH = sys._MEIPASS
        UI_PATH = os.path.join(BASE_PATH, 'GUI', 'Versa3dMainWindow.ui')
    except Exception:
        BASE_PATH = os.path.abspath(".")
        UI_PATH = os.path.join(
            BASE_PATH, 'designer_files', 'Versa3dMainWindow.ui')

    APP.setOrganizationName("msam")
    APP.setOrganizationDomain("https://msam-uwaterloo.ca/")
    APP.setApplicationName("Versa3d")

    WINDOW = MainWindow(UI_PATH)
    CONTROLLER = Versa3dController(parent = WINDOW)
    set_up_app(WINDOW, CONTROLLER)
    WINDOW.show()

    sys.exit(APP.exec_())
