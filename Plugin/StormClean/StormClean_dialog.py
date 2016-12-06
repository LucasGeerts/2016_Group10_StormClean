# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StormCleanDialog
                                 A QGIS plugin
 The plugin allows the user to analyse Voluntary Geographic Information (VGI) provided by citizens of a storm struck city. StormClean prioritises information based on predefined or user-defined knowledge, allowing the usergroup to vary. It provides the full capabilities of a modern SDSS and both cartographic as well as tabular output.
                             -------------------
        begin                : 2016-12-02
        git sha              : $Format:%H$
        copyright            : (C) 2016 by C. Kleijwegt, L. Geerts, D. Kersbergen
        email                : cathelijne.kleijwegt@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Window1.ui'))


class StormCleanDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(StormCleanDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
