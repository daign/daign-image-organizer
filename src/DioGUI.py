#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from PyQt4 import QtGui
from PyQt4 import QtCore

import Database
from DioView import DioView
from DioDetails import DioDetails


class DioGUI( QtGui.QSplitter ):

	def __init__( self, parent = None ):

		QtGui.QSplitter.__init__( self, parent )
		self.setWindowTitle( 'Daign Image Organizer' )

		self.selected_range = []
		self.selected_image = None

		Database.create_database()

		# View

		self.view = DioView( self )

		# Controls

		scan_button = QtGui.QPushButton( 'Scan Folders', self )
		scan_button.clicked.connect( self.scan_folders )

		search_tags_button = QtGui.QPushButton( 'Load Tags', self )
		search_tags_button.clicked.connect( self.load_tags )
		self.search_tags_list = QtGui.QListWidget( self )

		search_names_button = QtGui.QPushButton( 'Load Names', self )
		search_names_button.clicked.connect( self.load_names )
		self.search_names_list = QtGui.QListWidget( self )

		search_stars_label = QtGui.QLabel( 'Stars' )
		self.search_stars_from_input = QtGui.QSpinBox( self )
		self.search_stars_from_input.setRange( 0, 7 )
		self.search_stars_from_input.setValue( 0 )
		search_stars_to_label = QtGui.QLabel( 'to' )
		self.search_stars_to_input = QtGui.QSpinBox( self )
		self.search_stars_to_input.setRange( 0, 7 )
		self.search_stars_to_input.setValue( 7 )
		search_stars_layout = QtGui.QHBoxLayout()
		search_stars_layout.addWidget( search_stars_label )
		search_stars_layout.addWidget( self.search_stars_from_input )
		search_stars_layout.addWidget( search_stars_to_label )
		search_stars_layout.addWidget( self.search_stars_to_input )
		search_stars_layout.addStretch( 1 )
		search_stars_widget = QtGui.QWidget( self )
		search_stars_widget.setLayout( search_stars_layout )

		show_random_button = QtGui.QPushButton( 'Random Image', self )
		show_random_button.clicked.connect( self.show_random_image )
		show_all_button = QtGui.QPushButton( 'All Images', self )
		show_all_button.clicked.connect( self.show_all_images )

		search_box = QtGui.QGroupBox( 'Image Search', self )
		search_grid = QtGui.QGridLayout()
		search_grid.addWidget( search_tags_button,     0, 0, 1, 1 )
		search_grid.addWidget( search_names_button,    0, 1, 1, 1 )
		search_grid.addWidget( self.search_tags_list,  1, 0, 1, 1 )
		search_grid.addWidget( self.search_names_list, 1, 1, 1, 1 )
		search_grid.addWidget( search_stars_widget,    2, 0, 1, 2 )
		search_grid.addWidget( show_random_button,     3, 0, 1, 1 )
		search_grid.addWidget( show_all_button,        3, 1, 1, 1 )
		search_box.setLayout( search_grid )

		self.details = DioDetails( self )

		controls_layout = QtGui.QVBoxLayout()
		controls_layout.addWidget( scan_button, 1 )
		controls_layout.addWidget( search_box, 2 )
		controls_layout.addWidget( self.details, 1 )

		controls_widget = QtGui.QWidget( self )
		controls_widget.setLayout( controls_layout )

		self.addWidget( self.view )
		self.addWidget( controls_widget )
		self.setSizes( [ 600, 200 ] )


	def scan_folders( self ):

		image_counter = Database.scan_folders()

		dialog = QtGui.QDialog()
		dialog.setWindowTitle( 'Folder Scan Finished' )
		dialog.setMinimumWidth( 200 )
		dialog.setWindowModality( QtCore.Qt.ApplicationModal )

		dialog_label = QtGui.QLabel( 'Found ' + str( image_counter ) + ' images' )
		ok_button = QtGui.QPushButton( 'Ok', dialog )
		ok_button.clicked.connect( dialog.accept )

		dialog_layout = QtGui.QVBoxLayout()
		dialog_layout.addWidget( dialog_label, 1 )
		dialog_layout.addWidget( ok_button, 1 )
		dialog.setLayout( dialog_layout )

		dialog.exec_()


	def load_tags( self ):

		tags = Database.get_all_tags()
		self.search_tags_list.clear()

		if tags is not None:
			self.search_tags_list.addItem( '' )
			for t in tags:
				self.search_tags_list.addItem( t )


	def load_names( self ):

		names = Database.get_all_names()
		self.search_names_list.clear()

		if names is not None:
			self.search_names_list.addItem( '' )
			for n in names:
				self.search_names_list.addItem( n )


	def get_filtered_selection( self ):

		tag = self.search_tags_list.currentItem()
		if tag is not None:
			tag = str( tag.text() )
			if len( tag ) == 0:
				tag = None

		name = self.search_names_list.currentItem()
		if name is not None:
			name = str( name.text() )
			if len( name ) == 0:
				name = None

		stars_from = self.search_stars_from_input.value()
		stars_to = self.search_stars_to_input.value()

		self.set_selected_range( Database.get_filtered_selection( tag, name, stars_from, stars_to ) )


	def set_selected_range( self, new_range ):

		self.selected_range = new_range
		self.view.list_needs_update = True


	def show_all_images( self ):

		self.get_filtered_selection()
		self.selected_image = None

		self.show_list()


	def show_random_image( self ):

		self.get_filtered_selection()

		if len( self.selected_range ) > 0:

			hash_md5 = random.choice( self.selected_range )
			self.show_image( hash_md5 )

		else:

			self.selected_image = None

			self.details.show_text( 'Found Nothing' )
			self.view.show_text( 'Found Nothing' )


	def show_list( self ):

		if len( self.selected_range ) > 0:

			self.details.show_list_details( self.selected_range )
			self.view.show_list( self.selected_range )

		else:

			self.details.show_text( 'Found Nothing' )
			self.view.show_text( 'Found Nothing' )


	def show_image( self, hash_md5 ):

		self.selected_image = hash_md5

		self.details.show_image_details( hash_md5 )
		self.view.show_image( hash_md5 )


