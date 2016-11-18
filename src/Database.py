#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import string
import sqlite3
import hashlib


def md5( fname ):

	hash_md5 = hashlib.md5()
	with open( fname, 'rb' ) as f:
		for chunk in iter( lambda: f.read( 4096 ), b'' ):
			hash_md5.update( chunk )
	return sqlite3.Binary( hash_md5.digest() )


def create_database():

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()
		cur.execute( "CREATE TABLE IF NOT EXISTS Paths(Hash BLOB, Path TEXT)" )
		cur.execute( "CREATE TABLE IF NOT EXISTS Images(Hash BLOB PRIMARY KEY, Stars INT)" )
		cur.execute( "CREATE TABLE IF NOT EXISTS Tags(Hash BLOB, Tag TEXT)" )
		cur.execute( "CREATE TABLE IF NOT EXISTS Names(Hash BLOB, Name TEXT)" )


def scan_folders():

	rootdir = '.'
	pattern = re.compile( '\.(jpg|jpeg|png|gif|bmp|tif|tiff)$' )
	counter = 0

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()
		cur.execute( "DROP TABLE IF EXISTS Paths" )
		cur.execute( "CREATE TABLE Paths(Hash BLOB, Path TEXT)" )

		for subdir, dirs, files in os.walk( rootdir ):
			for file in files:
				if pattern.search( file ) is not None:
					path = os.path.join( subdir, file )
					hash_md5 = md5( path )
					cur.execute( "INSERT INTO Paths VALUES(?,?)", ( hash_md5, path ) )
					counter += 1

	return counter


def get_all_tags():

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()
		cur.execute( "SELECT DISTINCT Tag FROM Tags" )
		tags = cur.fetchall()
		if len( tags ) > 0:
			return sorted( [ t[ 0 ] for t in tags ] )
		else:
			return None


def get_all_names():

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()
		cur.execute( "SELECT DISTINCT Name FROM Names" )
		names = cur.fetchall()
		if len( names ) > 0:
			return sorted( [ n[ 0 ] for n in names ] )
		else:
			return None


def get_random_image( tag, name, stars_from, stars_to ):

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()

		# no limitation in query
		if tag is None and name is None and stars_from == 0 and stars_to == 7:

			cur.execute( "SELECT Hash FROM Paths ORDER BY RANDOM() LIMIT 1" )
			hash_md5 = cur.fetchone()

			if hash_md5 is not None:
				return hash_md5[ 0 ]
			else:
				return None

		# invalid range for stars, ignored
		elif stars_from > stars_to:

			cur.execute( "SELECT DISTINCT Hash FROM Paths LEFT OUTER JOIN Tags USING (Hash) LEFT OUTER JOIN Names USING (Hash) WHERE (Tag=? OR ? is NULL) AND (Name=? OR ? is NULL) ORDER BY RANDOM() LIMIT 1", ( tag, tag, name, name ) )
			hash_md5 = cur.fetchone()

			if hash_md5 is not None:
				return hash_md5[ 0 ]
			else:
				return None

		else:

			cur.execute( "SELECT DISTINCT Hash FROM Paths LEFT OUTER JOIN Images USING (Hash) LEFT OUTER JOIN Tags USING (Hash) LEFT OUTER JOIN Names USING (Hash) WHERE (Tag=? OR ? is NULL) AND (Name=? OR ? is NULL) AND ((Stars <= ? AND Stars >= ? ) OR (? is 0 AND Stars is NULL)) ORDER BY RANDOM() LIMIT 1", ( tag, tag, name, name, stars_to, stars_from, stars_from ) )
			hash_md5 = cur.fetchone()

			if hash_md5 is not None:
				return hash_md5[ 0 ]
			else:
				return None


def get_paths( hash_md5 ):

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()
		cur.execute( "SELECT Path FROM Paths WHERE Hash=?", ( hash_md5, ) )
		paths = cur.fetchall()
		if len( paths ) > 0:
			return [ p[ 0 ] for p in paths ]
		else:
			return []


def get_stars( hash_md5 ):

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()
		cur.execute( "SELECT Stars FROM Images WHERE Hash=?", ( hash_md5, ) )
		stars = cur.fetchone()
		if stars is None:
			return 0
		else:
			return stars[ 0 ]


def get_tags( hash_md5 ):

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()
		cur.execute( "SELECT Tag FROM Tags WHERE Hash=?", ( hash_md5, ) )
		tags = cur.fetchall()
		if len( tags ) > 0:
			return ', '.join( [ t[ 0 ] for t in tags ] )
		else:
			return ''


def get_names( hash_md5 ):

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()
		cur.execute( "SELECT Name FROM Names WHERE Hash=?", ( hash_md5, ) )
		names = cur.fetchall()
		if len( names ) > 0:
			return ', '.join( [ n[ 0 ] for n in names ] )
		else:
			return ''


def save_details( hash_md5, stars, tags, names ):

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()

		if stars != 0:
			cur.execute( "REPLACE INTO Images VALUES(?,?)", ( hash_md5, stars ) )

		tags_list = re.split( ';|,', tags )
		tags_list = [ string.capwords( t.lstrip().rstrip() ) for t in tags_list ]
		cur.execute( "DELETE FROM Tags WHERE Hash=?", ( hash_md5, ) )
		for t in tags_list:
			if len( t ) > 0:
				cur.execute( "INSERT INTO Tags VALUES(?,?)", ( hash_md5, t ) )

		names_list = re.split( ';|,', names )
		names_list = [ string.capwords( n.lstrip().rstrip() ) for n in names_list ]
		cur.execute( "DELETE FROM Names WHERE Hash=?", ( hash_md5, ) )
		for n in names_list:
			if len( n ) > 0:
				cur.execute( "INSERT INTO Names VALUES(?,?)", ( hash_md5, n ) )


def delete_entry( hash_md5 ):

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()
		cur.execute( "DELETE FROM Images WHERE Hash=?", ( hash_md5, ) )
		cur.execute( "DELETE FROM Tags WHERE Hash=?", ( hash_md5, ) )
		cur.execute( "DELETE FROM Names WHERE Hash=?", ( hash_md5, ) )


