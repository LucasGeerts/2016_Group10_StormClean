# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StormCleanDialog
                                 A QGIS plugin
 StormClean provides the opportunity to first responders and clean up teams to directly process and prioritise Voluntary Geographic Information (VGI).
                             -------------------
        begin                : 2016-12-06
        git sha              : $Format:%H$
        copyright            : (C) 2016 by D. Kersbergen, L. Geerts, C. Kleijwegt
        email                : d.kersbergen@student.tudelft.nl
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
from qgis.core import QgsProject
from PyQt4.QtCore import QFileInfo
from . import utility_functions as uf

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'StormClean_dialog_base.ui'))


class StormCleanDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(StormCleanDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
    # define globals
        self.iface = iface
    # data
        # self.openScenario("C:\Users\Python\Desktop\Plugin\StormClean\data\rotterdam.qgs")
        # Get the project instance
        project = QgsProject.instance()
        # Print the current project file name (might be empty in case no projects have been loaded)
        print project.fileName
        # Load another project
        project.read(QFileInfo("C:\Users\Python\Desktop\Plugin\StormClean\data\rotterdam.qgs"))
        print project.fileName
    # test functions
        #self.LogOut.clicked.connect(self.openScenario)

    """def openScenario(self,filename=""):
            #scenario_file = os.path.join('C:\Users\Python\Desktop\Plugin\StormClean\data',filename)
            # check if file exists
            if os.path.isfile(filename):
                self.iface.addProject(filename)
                scenario_open = True
            else:
                last_dir = uf.getLastDir("StormClean")
                new_file = QtGui.QFileDialog.getOpenFileName(self, "", last_dir, "(*.qgs)")
                if new_file:
                    self.iface.addProject(unicode(new_file))
                    scenario_open = True
            if scenario_open:
               # self.updateLayers()
                pass

    def updateLayers(self):
        layers = uf.getLegendLayers(self.iface, 'all', 'all')
        self.selectLayerCombo.clear()
        if layers:
            layer_names = uf.getLayersListNames(layers)
            self.selectLayerCombo.addItems(layer_names)
            self.setSelectedLayer()
        else:
            self.selectAttributeCombo.clear()
            self.clearChart()"""