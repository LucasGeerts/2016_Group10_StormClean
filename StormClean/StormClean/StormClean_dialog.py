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
import random
from PyQt4 import QtGui, uic, QtCore
from qgis.core import *
from qgis.networkanalysis import *
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
        self.canvas_1 = self.QgsMapCanvas_1
        self.canvas_2 = self.QgsMapCanvas_2
        self.canvas_3 = self.QgsMapCanvas_3
        self.canvas_4 = self.QgsMapCanvas_4


    #GUI
        self.Pages.setCurrentIndex(0)
    #Interaction
        self.Login.clicked.connect(self.topage1)
        self.Cancel.clicked.connect(self.close)
        self.pushButton_logout.clicked.connect(self.Logoutclicked)
        self.pushButton_logout2.clicked.connect(self.Logoutclicked)
        self.pushButton_logout3.clicked.connect(self.Logoutclicked)
        self.pushButton_logout4.clicked.connect(self.Logoutclicked)
        self.pushButton_logout5.clicked.connect(self.Logoutclicked)
        self.listWidget_listofneighbourhood.currentItemChanged.connect(self.topage2)
        self.listWidget_incidents.currentItemChanged.connect(self.topage3)
        self.back.clicked.connect(self.topage1)
        self.pushButton_No.clicked.connect(self.notoincident)
        self.pushButton_Yes.clicked.connect(self.yestoincident)
        self.pushButton_arrived.clicked.connect(self.topage5)

    #shortest route
        self.graph = QgsGraph()
        self.tied_points = []

    def showEvent(self, event):
        self.Pages.setCurrentIndex(0)
        self.Box_Password.clear()
        self.Box_Username.clear()
        scenario_open = False
        scenario_file = os.path.join(os.path.dirname(__file__),'SampleData','Rotterdam.qgs')
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

        startpointlayer = uf.getLegendLayerByName(self.iface, 'StartPointsRoute')
        allstartpointfeatures = startpointlayer.getFeatures()
        source_points = [feature.geometry().asPoint() for feature in allstartpointfeatures]
        startpoint = random.choice(source_points)
        global startpoint
        #print startpoint

        onestartpointlayer = uf.getLegendLayerByName(self.iface, "OneStartPoint")
        # create one if it doesn't exist
        if not onestartpointlayer:
            attribs = ['id']
            types = [QtCore.QVariant.String]
            onestartpointlayer = uf.createTempLayer('OneStartPoint', 'POINT', startpointlayer.crs().postgisSrid(),
                                                    attribs, types)
            uf.loadTempLayer(onestartpointlayer)
        uf.insertTempFeatures(onestartpointlayer, [startpoint], [['random string, after this a random number', 12]])

    def topage1(self):
        if self.listWidget_incidents:
           self.listWidget_incidents.clear()
        self.Pages.setCurrentIndex(1)
        if self.canvas.layerCount() == 0:
            #Open map to canvas
            canvas_layers = []
            layer1 = uf.getLegendLayerByName(self.iface, 'Wijk_Rott')
            layer2 = uf.getLegendLayerByName(self.iface, 'BackgroundGrey')
            layers = [layer1, layer2]
            for layer in layers:
                if not layer.isValid():
                    raise IOError, "Failed to open the layer"
                QgsMapLayerRegistry.instance().addMapLayer(layer)
                canvas_layers.append(QgsMapCanvasLayer(layer))
            self.canvas.setExtent(layer1.extent())
            self.canvas.setLayerSet(canvas_layers)

            #Fill attributes in list
            self.listWidget_listofneighbourhood.clear()
            for item in uf.getFieldValues(layer1, 'WK_NAAM')[0]:
                self.listWidget_listofneighbourhood.addItem(item)


    def Logoutclicked(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle('StormClean')
        msgBox.setText('Are you sure you want to log out?')
        msgBox.addButton(QtGui.QPushButton('No'), QtGui.QMessageBox.RejectRole)
        msgBox.addButton(QtGui.QPushButton('Yes'), QtGui.QMessageBox.AcceptRole)
        ret = msgBox.exec_()
        if ret == 0:
            pass
        elif ret == 1:
            self.Pages.setCurrentIndex(0)
            self.Box_Password.clear()
            self.Box_Username.clear()

    def topage2(self, name=''):
        layer = uf.getLegendLayerByName(self.iface, 'Wijk_Rott')
        expr = QgsExpression('"WK_NAAM"  =  ' + "'" + str(name.text()) + "'")
        attr = layer.getFeatures(QgsFeatureRequest(expr))
        ids = [att.id() for att in attr]
        layer.setSelectedFeatures(ids)
        self.canvas.zoomToSelected(layer)

        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle('StormClean')
        msgBox.setText('Would you like to select '+ str(name.text() + '?'))
        msgBox.addButton(QtGui.QPushButton('No'), QtGui.QMessageBox.RejectRole)
        msgBox.addButton(QtGui.QPushButton('Yes'), QtGui.QMessageBox.AcceptRole)
        ret = msgBox.exec_()
        if ret == 0:
            pass
        elif ret == 1:

            self.WijkName.setFontPointSize(18)
            self.WijkName.setFontWeight(600)
            self.WijkName.setText(name.text())


            self.canvas_1.zoomToSelected(layer)
            canvas_layers_1 = []
            for item in uf.getCanvasLayers(self.iface, geom='all', provider='all'):
                if not item.isValid():
                    raise IOError, "Failed to open the layer"
                QgsMapLayerRegistry.instance().addMapLayer(item)
                canvas_layers_1.append(QgsMapCanvasLayer(item))
            item0 = uf.getLegendLayerByName(self.iface, 'BackgroundGrey')
            QgsMapLayerRegistry.instance().addMapLayer(item0)
            canvas_layers_1.append(QgsMapCanvasLayer(item0))
            self.canvas_1.setLayerSet(canvas_layers_1)
            self.Pages.setCurrentIndex(2)
            self.listWidget_incidents.clear()
            incident = uf.getLegendLayerByName(self.iface, 'IncidentPoints')
            rectangle = self.canvas_1.extent()
            incident.invertSelectionInRectangle(rectangle)
            table = uf.getFieldValuesSorted(incident, 'IncidentName', sorted = 'IncidentValue', selection = True)
            global table
            for itemsort, itemid, itemtext in table:
                if itemtext == " REMOVE" or itemtext == "REMOVE" or str(itemtext) == "NULL":
                    pass
                else:
                    self.listWidget_incidents.addItem(str(itemsort) + ' --- ' + str(itemtext))
            incident.removeSelection()


        layer.removeSelection()
        self.canvas.setExtent(layer.extent())
        self.canvas.refresh()

    def topage3(self, listitem):
        if listitem == None:
            pass
        else:
            index = self.listWidget_incidents.currentRow()
            layer = uf.getLegendLayerByName(self.iface, 'IncidentPoints')
            expr = QgsExpression('"ID"  =  ' + "'" + str(table[index][1]) + "'")
            attr = layer.getFeatures(QgsFeatureRequest(expr))
            ids = [att.id() for att in attr]
            layer.setSelectedFeatures(ids)
            self.canvas_1.zoomToSelected(layer)
            scale = self.canvas_1.scale()
            msgBox = QtGui.QMessageBox()
            msgBox.setWindowTitle('StormClean')
            msgBox.setText('Would you like to select '+ str(table[index][2]) + '?')
            msgBox.addButton(QtGui.QPushButton('No'), QtGui.QMessageBox.RejectRole)
            msgBox.addButton(QtGui.QPushButton('Yes'), QtGui.QMessageBox.AcceptRole)
            ret = msgBox.exec_()
            if ret == 0:
                pass
            elif ret == 1:

                self.textBrowser_incidentname.setFontPointSize(18)
                self.textBrowser_incidentname.setFontWeight(600)
                self.textBrowser_incidentname.setText(str(table[index][2]))

                self.canvas_2.zoomToSelected(layer)
                self.canvas_2.zoomScale(scale)
                expr = QgsExpression('"ID"  =  ' + "'" + str(table[index][1]) + "'")
                attr = layer.getFeatures(QgsFeatureRequest(expr))
                for att in attr:
                    attribute =  att.attribute('ManualComment')
                    if attribute != NULL:
                        self.textBrowser_manualdiscription.setHtml(
                            "<p><strong>Manual description</strong></p>" + str(attribute))
                        self.textBrowser.setHtml(
                            "<p><strong>NOT PROVIDED</strong></p>")
                    else:
                        self.textBrowser_manualdiscription.setHtml(
                            "<p><strong>Manual description</strong><p>" + "<p>No information provided<p>")
                        self.textBrowser.setHtml(
                            "<p><strong>NOT PROVIDED</strong></p>")
                global scale
                global index

                canvas_layers_2 = []
                for item in uf.getCanvasLayers(self.iface, geom='all', provider='all'):
                    if not item.isValid():
                        raise IOError, "Failed to open the layer"
                    QgsMapLayerRegistry.instance().addMapLayer(item)
                    canvas_layers_2.append(QgsMapCanvasLayer(item))
                item0 = uf.getLegendLayerByName(self.iface, 'BackgroundGrey')
                QgsMapLayerRegistry.instance().addMapLayer(item0)
                canvas_layers_2.append(QgsMapCanvasLayer(item0))
                self.canvas_2.setLayerSet(canvas_layers_2)
                self.Pages.setCurrentIndex(3)

            layer.removeSelection()
            self.canvas_1.zoomToPreviousExtent()
            self.canvas_1.zoomScale(scale)
            self.canvas_1.refresh()

    def notoincident(self):
        #layer.removeSelection()
        self.Pages.setCurrentIndex(2)


    def yestoincident(self):
        self.calculateRoute()

        canvas_layers_3 = []
        item1 = uf.getLegendLayerByName(self.iface, 'Routes')
        item2 = uf.getLegendLayerByName(self.iface, 'IncidentPoints')
        item0 = uf.getLegendLayerByName(self.iface, 'BackgroundGrey')

        for itemx in [item1,item2,item0]:
            QgsMapLayerRegistry.instance().addMapLayer(itemx)
            canvas_layers_3.append(QgsMapCanvasLayer(itemx))
        self.canvas_3.setLayerSet(canvas_layers_3)
        self.canvas_3.setExtent(item1.extent())
        self.Pages.setCurrentIndex(4)

    def topage5(self):
        layer = uf.getLegendLayerByName(self.iface, 'IncidentPoints')
        expr = QgsExpression('"ID"  =  ' + "'" + str(table[index][1]) + "'")
        attr = layer.getFeatures(QgsFeatureRequest(expr))
        ids = [att.id() for att in attr]
        layer.setSelectedFeatures(ids)
        self.canvas_1.zoomToSelected(layer)
        scale = self.canvas_1.scale()

        self.textBrowser_incidentname_2.setFontPointSize(18)
        self.textBrowser_incidentname_2.setFontWeight(600)
        self.textBrowser_incidentname_2.setText(str(table[index][2]))

        self.canvas_4.zoomToSelected(layer)
        self.canvas_4.zoomScale(scale)
        expr = QgsExpression('"ID"  =  ' + "'" + str(table[index][1]) + "'")
        attr = layer.getFeatures(QgsFeatureRequest(expr))
        for att in attr:
            attribute = att.attribute('ManualComment')
            if attribute != NULL:
                self.textBrowser_manualdiscription_2.setHtml(
                    "<p><strong>Manual description</strong></p>" + str(attribute))
                self.textBrowser_2.setHtml(
                    "<p><strong>NOT PROVIDED</strong></p>")
            else:
                self.textBrowser_manualdiscription_2.setHtml(
                    "<p><strong>Manual description</strong><p>" + "<p>No information provided<p>")
                self.textBrowser_2.setHtml(
                    "<p><strong>NOT PROVIDED</strong></p>")

        canvas_layers_4 = []
        item1 = uf.getLegendLayerByName(self.iface, 'IncidentPoints')
        item0 = uf.getLegendLayerByName(self.iface, 'BackgroundGrey')

        for itemx in [item1,item0]:
            QgsMapLayerRegistry.instance().addMapLayer(itemx)
            canvas_layers_4.append(QgsMapCanvasLayer(itemx))
        self.canvas_4.setLayerSet(canvas_layers_4)
        self.canvas_4.setLayerSet(canvas_layers_4)

        self.Pages.setCurrentIndex(5)

    def getNetwork(self):
        roads_layer = uf.getLegendLayerByName(self.iface, 'NWB_2016_Rotterdam_roads_Edit')
        if roads_layer:
            return roads_layer
        else:
            return

    def buildNetwork(self):
        self.network_layer = self.getNetwork()
        if self.network_layer:
            # get the points to be used as origin and destination
            # in this case gets the centroid of the selected features
            selected_sources = uf.getLegendLayerByName(self.iface, 'IncidentPoints')
            allfeatures = selected_sources.getFeatures()
            source_points = [feature.geometry().asPoint() for feature in allfeatures]
            source_points.append(startpoint)
            # build the graph including these points
            if len(source_points) > 1:
                self.graph, self.tied_points = uf.makeUndirectedGraph(self.network_layer, source_points)
                # the tied points are the new source_points on the graph
                if self.graph and self.tied_points:
                    text = "network is built for %s points" % len(self.tied_points)
                    #print text
                    # self.insertReport(text)
        return

    def calculateRoute(self):
        self.buildNetwork()
        # origin and destination must be in the set of tied_points
        options = len(self.tied_points)
        if options > 1:
            # origin and destination are given as an index in the tied_points list
            origin = -1
            destination = table[index][1]
            # destination = random.randint(1,options-1)  # this was original code, I guess we don't want a random destination...
            # calculate the shortest path for the given origin and destination
            path = uf.calculateRouteDijkstra(self.graph, self.tied_points, origin, destination)
            # store the route results in temporary layer called "Routes"
            routes_layer = uf.getLegendLayerByName(self.iface, "Routes")
            # create one if it doesn't exist
            if not routes_layer:
                attribs = ['id']
                types = [QtCore.QVariant.String]
                routes_layer = uf.createTempLayer('Routes', 'LINESTRING', self.network_layer.crs().postgisSrid(),
                                                  attribs, types)
                uf.loadTempLayer(routes_layer)
            # insert route line
            #for route in routes_layer.getFeatures():
                #print route.id()
            uf.insertTempFeatures(routes_layer, [path], [[12]])
            # uf.insertTempFeatures(routes_layer, [path], [['testing',100.00]])
            # buffer = processing.runandload('qgis:fixeddistancebuffer',routes_layer,10.0,5,False,None)
            # self.refreshCanvas(routes_layer)

    def deleteRoutes(self):
        routes_layer = uf.getLegendLayerByName(self.iface, "Routes")
        if routes_layer:
            ids = uf.getAllFeatureIds(routes_layer)
            routes_layer.startEditing()
            for id in ids:
                routes_layer.deleteFeature(id)
            routes_layer.commitChanges()