#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from PyQt4 import QtGui
from PyQt4 import QtCore

import Database


class DioScanDialog( QtGui.QDialog ):

	def __init__( self, parent ):

		QtGui.QDialog.__init__( self, parent = None )

		self.setWindowTitle( 'Folder Scan' )
		self.setMinimumWidth( 200 )
		self.setWindowModality( QtCore.Qt.ApplicationModal )

		self.similarity_checkbox = QtGui.QCheckBox( 'Compute and store similarity hashes', self )
		self.similarity_checkbox.setChecked( True )

		scan_button = QtGui.QPushButton( 'Scan', self )
		scan_button.clicked.connect( self.execute_scan )
		self.result_label = QtGui.QLabel( '' )

		self.scan_progress = QtGui.QProgressBar( self )

		close_button = QtGui.QPushButton( 'Close', self )
		close_button.clicked.connect( self.accept )

		dialog_layout = QtGui.QGridLayout()
		dialog_layout.addWidget( self.similarity_checkbox, 0, 1, 1, 2 )
		dialog_layout.addWidget( scan_button,              1, 1, 1, 1 )
		dialog_layout.addWidget( self.result_label,        1, 2, 1, 1 )
		dialog_layout.addWidget( self.scan_progress,       2, 1, 1, 2 )
		dialog_layout.addWidget( close_button,             3, 2, 1, 1 )
		self.setLayout( dialog_layout )


	def show( self ):

		self.result_label.setText( '' )
		self.scan_progress.reset()
		self.exec_()


	def set_progress_range( self, a, b ):

		self.scan_progress.setMinimum( a )
		self.scan_progress.setMaximum( b )


	def set_progress_value( self, v ):

		self.scan_progress.setValue( v )


	def execute_scan( self ):

		image_counter = Database.scan_folders(
			self.similarity_checkbox.isChecked(),
			self.set_progress_range,
			self.set_progress_value
		)
		self.result_label.setText( 'Found ' + str( image_counter ) + ' images' )


