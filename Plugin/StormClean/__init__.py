# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StormClean
                                 A QGIS plugin
 The plugin allows the user to analyse Voluntary Geographic Information (VGI) provided by citizens of a storm struck city. StormClean prioritises information based on predefined or user-defined knowledge, allowing the usergroup to vary. It provides the full capabilities of a modern SDSS and both cartographic as well as tabular output.
                             -------------------
        begin                : 2016-12-02
        copyright            : (C) 2016 by C. Kleijwegt, L. Geerts, D. Kersbergen
        email                : cathelijne.kleijwegt@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load StormClean class from file StormClean.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .StormClean import StormClean
    return StormClean(iface)
