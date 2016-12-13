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
from qgis.core import *
from PyQt4.QtCore import QFileInfo
from . import utility_functions as uf
import os.path
from qgis.gui import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Login_window.ui'))


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
        self.canvas = self.QgsMapCanvas

    def showEvent(self, event):
        scenario_open = False
        scenario_file = os.path.join('C:\Users\Python\Desktop\Plugin\StormClean','SampleData','Rotterdam.qgs')
        # check if file exists
        if os.path.isfile(scenario_file):
            self.iface.addProject(scenario_file)
            scenario_open = True
        else:
            last_dir = uf.getLastDir("StormClean")
            new_file = QtGui.QFileDialog.getOpenFileName(self, "", last_dir, "(*.qgs)")
            if new_file:
                self.iface.addProject(unicode(new_file))
                scenario_open = True

        for layer in uf.getCanvasLayers(self.iface, geom='all', provider='all'):
        #layer = uf.getLegendLayerByName(self.iface, '2016_Rotterdam_trees_Edit')
        #print layer
            if not layer.isValid():
                raise IOError, "Failed to open the layer"

        # add layer to the registry
            QgsMapLayerRegistry.instance().addMapLayer(layer)

        # set extent to the extent of our layer
            self.canvas.setExtent(layer.extent())

        # set the map canvas layer set
            self.canvas.setLayerSet([QgsMapCanvasLayer(layer)])