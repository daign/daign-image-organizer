#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

import Database
from StarsWidget import StarsWidget


class DioDetails( QtGui.QStackedWidget ):

	def __init__( self, parent ):

		QtGui.QStackedWidget.__init__( self, parent )

		self.parent = parent

		image_paths_label = QtGui.QLabel( 'Paths' )
		self.image_paths_input = QtGui.QTextEdit( '', self )
		self.image_paths_input.setDisabled( True )
		self.image_paths_input.setMaximumHeight( 45 )

		image_stars_label = QtGui.QLabel( 'Stars' )
		self.image_stars_input = StarsWidget( self )

		image_tags_label = QtGui.QLabel( 'Tags' )
		self.image_tags_input = QtGui.QLineEdit( '', self )

		image_names_label = QtGui.QLabel( 'Names' )
		self.image_names_input = QtGui.QLineEdit( '', self )

		save_button = QtGui.QPushButton( 'Save', self )
		save_button.clicked.connect( self.save_details )
		delete_button = QtGui.QPushButton( 'Delete Entry', self )
		delete_button.clicked.connect( self.delete_entry )

		self.image_details_box = QtGui.QGroupBox( 'Image Details', self )
		image_details_grid = QtGui.QGridLayout()
		image_details_grid.addWidget( image_paths_label,      0, 0, 1, 1 )
		image_details_grid.addWidget( self.image_paths_input, 0, 1, 1, 2 )
		image_details_grid.addWidget( image_stars_label,      1, 0, 1, 1 )
		image_details_grid.addWidget( self.image_stars_input, 1, 1, 1, 2 )
		image_details_grid.addWidget( image_tags_label,       2, 0, 1, 1 )
		image_details_grid.addWidget( self.image_tags_input,  2, 1, 1, 2 )
		image_details_grid.addWidget( image_names_label,      3, 0, 1, 1 )
		image_details_grid.addWidget( self.image_names_input, 3, 1, 1, 2 )
		image_details_grid.addWidget( save_button,            4, 1, 1, 1 )
		image_details_grid.addWidget( delete_button,          4, 2, 1, 1 )
		self.image_details_box.setLayout( image_details_grid )

		self.addWidget( self.image_details_box )

		self.list_details_label = QtGui.QLabel( '' )

		self.list_details_box = QtGui.QGroupBox( 'Selection Details', self )
		list_details_layout = QtGui.QVBoxLayout()
		list_details_layout.addWidget( self.list_details_label, 1 )
		self.list_details_box.setLayout( list_details_layout )

		self.addWidget( self.list_details_box )

		self.text_label = QtGui.QLabel( '' )

		self.addWidget( self.text_label )


	def show_list_details( self, hashes ):

		self.setCurrentWidget( self.list_details_box )
		if len( hashes ) > 200:
			self.list_details_label.setText( str( len( hashes ) ) + ' images in selection,\nshowing first 200' )
		else:
			self.list_details_label.setText( str( len( hashes ) ) + ' images in selection' )


	def show_image_details( self, hash_md5 ):

		self.setCurrentWidget( self.image_details_box )

		paths = Database.get_paths( hash_md5 )
		self.image_paths_input.setText( '\n'.join( paths ) )
		self.image_stars_input.set_value( Database.get_stars( hash_md5 ) )
		self.image_tags_input.setText( Database.get_tags( hash_md5 ) )
		self.image_names_input.setText( Database.get_names( hash_md5 ) )


	def show_text( self, text ):

		self.setCurrentWidget( self.text_label )
		self.text_label.setText( text )


	def save_details( self ):

		if self.parent.selected_image is not None:
			Database.save_details(
				self.parent.selected_image,
				self.image_stars_input.value,
				str( self.image_tags_input.text() ),
				str( self.image_names_input.text() )
			)


	def delete_entry( self ):

		if self.parent.selected_image is not None:
			Database.delete_entry( self.parent.selected_image )


