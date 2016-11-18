from PyQt4 import QtGui

from StarButton import StarButton


class StarsWidget( QtGui.QWidget ):

	def __init__( self, parent ):

		QtGui.QWidget.__init__( self, parent )

		self.value = 0

		self.star_1 = StarButton( self )
		self.star_1.clicked.connect( self.set_value_1 )
		self.star_2 = StarButton( self )
		self.star_2.clicked.connect( self.set_value_2 )
		self.star_3 = StarButton( self )
		self.star_3.clicked.connect( self.set_value_3 )
		self.star_4 = StarButton( self )
		self.star_4.clicked.connect( self.set_value_4 )
		self.star_5 = StarButton( self )
		self.star_5.clicked.connect( self.set_value_5 )

		self.stars = [
			self.star_1,
			self.star_2,
			self.star_3,
			self.star_4,
			self.star_5
		]

		stars_layout = QtGui.QHBoxLayout()
		stars_layout.addWidget( self.star_1, 1 )
		stars_layout.addWidget( self.star_2, 1 )
		stars_layout.addWidget( self.star_3, 1 )
		stars_layout.addWidget( self.star_4, 1 )
		stars_layout.addWidget( self.star_5, 1 )
		stars_layout.addStretch( 1 )

		self.setLayout( stars_layout )

		self.setFixedSize( 150, 34 )


	def set_value_1( self ):

		self.set_value( 1 )


	def set_value_2( self ):

		self.set_value( 2 )


	def set_value_3( self ):

		self.set_value( 3 )


	def set_value_4( self ):

		self.set_value( 4 )


	def set_value_5( self ):

		self.set_value( 5 )


	def set_value( self, v ):

		self.value = v

		for i in range( 0, 5 ):
			if i < v:
				self.stars[ i ].set_state( True )
			else:
				self.stars[ i ].set_state( False )


