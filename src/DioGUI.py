#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

import Database
from StarsWidget import StarsWidget


class DioGUI( QtGui.QSplitter ):

	def __init__( self, app, parent = None ):

		QtGui.QWidget.__init__( self, parent )
		self.setWindowTitle( 'Daign Image Organizer' )

		self.app = app
		self.current_hash = None

		Database.create_database()

		# View

		self.view = QtGui.QLabel( '' )

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
		#show_all_button = QtGui.QPushButton( 'All Images', self )
		#show_all_button.setDisabled( True )

		search_box = QtGui.QGroupBox( 'Image Search', self )
		search_grid = QtGui.QGridLayout()
		search_grid.addWidget( search_tags_button,     0, 0, 1, 1 )
		search_grid.addWidget( search_names_button,    0, 1, 1, 1 )
		search_grid.addWidget( self.search_tags_list,  1, 0, 1, 1 )
		search_grid.addWidget( self.search_names_list, 1, 1, 1, 1 )
		search_grid.addWidget( search_stars_widget,    2, 0, 1, 2 )
		search_grid.addWidget( show_random_button,     3, 0, 1, 1 )
		#search_grid.addWidget( show_all_button,        3, 1, 1, 1 )
		search_box.setLayout( search_grid )

		details_paths_label = QtGui.QLabel( 'Paths' )
		self.details_paths_input = QtGui.QTextEdit( '', self )
		self.details_paths_input.setDisabled( True )
		self.details_paths_input.setMaximumHeight( 45 )

		details_stars_label = QtGui.QLabel( 'Stars' )
		self.details_stars_input = StarsWidget( self )

		details_tags_label = QtGui.QLabel( 'Tags' )
		self.details_tags_input = QtGui.QLineEdit( '', self )

		details_names_label = QtGui.QLabel( 'Names' )
		self.details_names_input = QtGui.QLineEdit( '', self )

		save_button = QtGui.QPushButton( 'Save', self )
		save_button.clicked.connect( self.save_details )
		delete_button = QtGui.QPushButton( 'Delete Entry', self )
		delete_button.clicked.connect( self.delete_entry )

		image_details_box = QtGui.QGroupBox( 'Image Details', self )
		image_details_grid = QtGui.QGridLayout()
		image_details_grid.addWidget( details_paths_label,      0, 0, 1, 1 )
		image_details_grid.addWidget( self.details_paths_input, 0, 1, 1, 2 )
		image_details_grid.addWidget( details_stars_label,      1, 0, 1, 1 )
		image_details_grid.addWidget( self.details_stars_input, 1, 1, 1, 2 )
		image_details_grid.addWidget( details_tags_label,       2, 0, 1, 1 )
		image_details_grid.addWidget( self.details_tags_input,  2, 1, 1, 2 )
		image_details_grid.addWidget( details_names_label,      3, 0, 1, 1 )
		image_details_grid.addWidget( self.details_names_input, 3, 1, 1, 2 )
		image_details_grid.addWidget( save_button,              4, 1, 1, 1 )
		image_details_grid.addWidget( delete_button,            4, 2, 1, 1 )
		image_details_box.setLayout( image_details_grid )

		controls_layout = QtGui.QVBoxLayout()
		controls_layout.addWidget( scan_button, 1 )
		controls_layout.addWidget( search_box, 2 )
		controls_layout.addWidget( image_details_box, 1 )

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


	def show_random_image( self ):

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

		hash_md5 = Database.get_random_image( tag, name, stars_from, stars_to )
		self.current_hash = hash_md5

		if hash_md5 is not None:
			paths = Database.get_paths( hash_md5 )

			if len( paths ) > 0:
				pixmap = QtGui.QPixmap( paths[ 0 ] )
				scaled_pixmap = pixmap.scaled( self.view.size(), QtCore.Qt.KeepAspectRatio )
				self.view.setPixmap( scaled_pixmap )
			else:
				self.view.setText( 'No Image Found' )

			self.details_paths_input.setText( '\n'.join( paths ) )
			self.details_stars_input.set_value( Database.get_stars( hash_md5 ) )
			self.details_tags_input.setText( Database.get_tags( hash_md5 ) )
			self.details_names_input.setText( Database.get_names( hash_md5 ) )

		else:
			self.view.setText( 'Found Nothing' )
			self.details_paths_input.setText( '' )
			self.details_stars_input.set_value( 0 )
			self.details_tags_input.setText( '' )
			self.details_names_input.setText( '' )


	def save_details( self ):

		if self.current_hash is not None:
			Database.save_details(
				self.current_hash,
				self.details_stars_input.value,
				str( self.details_tags_input.text() ),
				str( self.details_names_input.text() )
			)


	def delete_entry( self ):

		if self.current_hash is not None:
			Database.delete_entry( self.current_hash )


