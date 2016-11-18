import pkg_resources
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt4 import QtGui
from PyQt4 import QtCore


class StarButton( QtGui.QAbstractButton ):

	def __init__( self, parent ):

		QtGui.QAbstractButton.__init__( self, parent )

		self.state = False

		image_on  = Image.open( pkg_resources.resource_stream( 'images', 'star_on.png' ) )
		image_off = Image.open( pkg_resources.resource_stream( 'images', 'star_off.png' ) )
		self.pixmap_on  = QtGui.QPixmap.fromImage( ImageQt( image_on ) )
		self.pixmap_off = QtGui.QPixmap.fromImage( ImageQt( image_off ) )

		self.pixmap = self.pixmap_off

		self.setFixedSize( 24, 24 )


	def paintEvent( self, event ):

		painter = QtGui.QPainter( self )
		painter.drawPixmap( event.rect(), self.pixmap )


	def set_state( self, state ):

		self.state = state

		if state:
			self.pixmap = self.pixmap_on
		else:
			self.pixmap = self.pixmap_off

		self.update()


