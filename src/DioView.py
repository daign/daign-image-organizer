#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore

import Database


class DioView( QtGui.QStackedWidget ):

	def __init__( self, parent ):

		QtGui.QStackedWidget.__init__( self, parent )

		self.parent = parent
		self.list_needs_update = True

		self.list = QtGui.QListWidget( self )
		self.list.setViewMode( QtGui.QListView.IconMode )
		self.list.setLayoutMode( QtGui.QListView.Batched )
		self.list.setBatchSize( 4 )
		self.list.setResizeMode( QtGui.QListView.Adjust )
		self.list.setMovement( QtGui.QListView.Static )
		self.list.setDragEnabled( False )
		self.list.setIconSize( QtCore.QSize( 120, 120 ) )
		self.list.setVerticalScrollMode( QtGui.QAbstractItemView.ScrollPerPixel )
		self.list.setSpacing( 6 )

		self.list.itemDoubleClicked.connect( self.list_item_clicked )

		self.addWidget( self.list )

		self.label = QtGui.QLabel( '' )
		self.label.setContextMenuPolicy( QtCore.Qt.ActionsContextMenu )

		back_action = QtGui.QAction( 'Back to list', self )
		back_action.triggered.connect( self.back_to_list )
		self.label.addAction( back_action )

		find_similar_action = QtGui.QAction( 'Find similar images', self )
		find_similar_action.triggered.connect( self.find_similar )
		self.label.addAction( find_similar_action )

		self.addWidget( self.label )


	def show_list( self, hashes ):

		self.list.clear()
		self.setCurrentWidget( self.list )

		for h in hashes[0:200]:

			paths = Database.get_paths( h )
			if len( paths ) > 0:

				item = QtGui.QListWidgetItem()
				item.setSizeHint( QtCore.QSize( 120, 120 ) )
				item.setToolTip( paths[ 0 ] )
				item.setBackgroundColor( QtGui.QColor( 0, 0, 0 ) )
				item.dio_hash = h

				icon = QtGui.QIcon()
				pixmap = QtGui.QPixmap( paths[ 0 ] )
				icon.addPixmap( pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off )
				item.setIcon( icon )
				self.list.addItem( item )

		self.list_needs_update = False


	def show_image( self, hash_md5 ):

		self.setCurrentWidget( self.label )

		paths = Database.get_paths( hash_md5 )
		if len( paths ) > 0:
			pixmap = QtGui.QPixmap( paths[ 0 ] )
			scaled_pixmap = pixmap.scaled( self.label.size(), QtCore.Qt.KeepAspectRatio )
			self.label.setPixmap( scaled_pixmap )
		else:
			self.label.setText( 'No Image Found' )


	def show_text( self, text ):

		self.setCurrentWidget( self.label )

		self.label.setText( text )


	def list_item_clicked( self, item ):

		self.parent.show_image( item.dio_hash )


	def back_to_list( self ):

		if not self.list_needs_update:

			self.setCurrentWidget( self.list )
			self.parent.details.setCurrentWidget( self.parent.details.list_details_box )

		else:

			self.parent.show_list()


	def find_similar( self ):

		hashes = Database.get_similar( self.parent.selected_image, 50 )
		self.parent.set_selected_range( hashes )
		self.parent.show_list()


