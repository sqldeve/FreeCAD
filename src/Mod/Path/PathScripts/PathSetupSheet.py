# -*- coding: utf-8 -*-

# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2017 sliptonic <shopinthewoods@gmail.com>               *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

import FreeCAD
import Path
import PathScripts.PathLog as PathLog
import PySide

__title__ = "Setup Sheet for a Job."
__author__ = "sliptonic (Brad Collette)"
__url__ = "http://www.freecadweb.org"
__doc__ = "A container for all default values and job specific configuration values."

if False:
    PathLog.setLevel(PathLog.Level.DEBUG, PathLog.thisModule())
    PathLog.trackModule()
else:
    PathLog.setLevel(PathLog.Level.INFO, PathLog.thisModule())

def translate(context, text, disambig=None):
    return PySide.QtCore.QCoreApplication.translate(context, text, disambig)

class Default:
    HorizRapid = 'DefaultHorizRapid'
    VertRapid = 'DefaultVertRapid'
    SafeHeight = 'DefaultSafeHeight'
    ClearanceHeight = 'DefaultClearanceHeight'

class SetupSheet:
    '''Spreadsheet used by a Job to hold global reference values.
It's mostly a convencience wrapper around Spreadsheet.
    '''

    def __init__(self, obj):
        self.obj = obj

    def setup(self):
        '''setup() ... initializes receiver with default values.'''
        self.obj.SetupSheet = self.obj.Document.addObject('Spreadsheet::Sheet', 'SetupSheet')
        self.obj.SetupSheet.set('A2', translate('PathSetupSheet', 'Tool Rapid Speeds'))
        self.createSetting(3, Default.HorizRapid, '0 mm/s', translate('PathSetupSheet', 'Horizontal'), translate('PathSetupSheet', 'Default speed for horizzontal rapid moves.'))
        self.createSetting(4, Default.VertRapid,  '0 mm/s', translate('PathSetupSheet', 'Vertical'),   translate('PathSetupSheet', 'Default speed for vertical rapid moves.'))
        self.obj.SetupSheet.set('A6', translate('PathSetupSheet', 'Operation Heights'))
        self.createSetting(7, Default.SafeHeight,      '3 mm',  translate('PathSetupSheet', 'Safe Height'),      translate('PathSetupSheet', 'Default value added to StartDepth used for the safe height.'))
        self.createSetting(8, Default.ClearanceHeight, '5 mm',  translate('PathSetupSheet', 'Clearance Height'), translate('PathSetupSheet', 'Default value added to StartDepth used for the clearance height.'))

    def updateSetting(self, alias, value):
        '''updateSetting(alias, value) ... stores a new value for the given value.'''
        cell = self.obj.SetupSheet.getCellFromAlias(alias)
        PathLog.debug("updateSetting(%s, %s): %s" % (alias, value, cell))
        self.obj.SetupSheet.set(cell, value)

    def createSetting(self, row, alias, value, label, desc):
        '''createSetting(row, alias, value, label, desc) ... sets the values of the new setting in the given row.'''
        labelCell = "B%d" % row
        valueCell = "C%d" % row
        descCell  = "D%d" % row
        PathLog.debug("createSetting(%d, %s, %s): %s" % (row, alias, value, valueCell))
        self.obj.SetupSheet.set(labelCell, label)
        self.obj.SetupSheet.set(valueCell, value)
        self.obj.SetupSheet.setAlias(valueCell, alias)
        self.obj.SetupSheet.set(descCell, desc)

    def setFromTemplate(self, attrs):
        '''setFromTemplate(attrs) ... sets the default values from the given dictionary.'''
        if attrs.get(Default.VertRapid):
            self.updateSetting(Default.VertRapid, attrs[Default.VertRapid])
        if attrs.get(Default.HorizRapid):
            self.updateSetting(Default.HorizRapid, attrs[Default.HorizRapid])
        if attrs.get(Default.SafeHeight):
            self.updateSetting(Default.SafeHeight, attrs[Default.SafeHeight])
        if attrs.get(Default.ClearanceHeight):
            self.updateSetting(Default.ClearanceHeight, attrs[Default.ClearanceHeight])

    def templateAttributes(self, includeRapids, includeHeights):
        '''templateAttributes(includeRapids, includeHeights) ... answers a dictionary with the default values.'''
        attrs = {}
        if includeRapids:
            attrs[Default.VertRapid]            = self.obj.SetupSheet.DefaultVertRapid.UserString
            attrs[Default.HorizRapid]           = self.obj.SetupSheet.DefaultHorizRapid.UserString
        if includeHeights:
            attrs[Default.SafeHeight]           = self.obj.SetupSheet.DefaultSafeHeight.UserString
            attrs[Default.ClearanceHeight]      = self.obj.SetupSheet.DefaultClearanceHeight.UserString
        return attrs

    def expressionReference(self):
        '''expressionReference() ... returns the string to be used in expressions'''
        return self.obj.SetupSheet.Label