#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import string
import sqlite3
import hashlib

import ImageSimilarity


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
		cur.execute( "CREATE TABLE IF NOT EXISTS Images(Hash BLOB PRIMARY KEY, Stars INT, Similarity TEXT)" )
		cur.execute( "CREATE TABLE IF NOT EXISTS Tags(Hash BLOB, Tag TEXT)" )
		cur.execute( "CREATE TABLE IF NOT EXISTS Names(Hash BLOB, Name TEXT)" )


def scan_folders( with_similarity, set_range_callback, set_value_callback ):

	rootdir = '.'
	pattern = re.compile( '\.(jpg|jpeg|png|gif|bmp|tif|tiff)$' )

	counter_files = 0
	for path, dirs, files in os.walk( rootdir ):
		counter_files += len( files )
	set_range_callback( 0, counter_files )


	counter_files = 0
	counter_images = 0
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

					if with_similarity:
						similarity_hash = ImageSimilarity.compute_similarity_hash( path )
						cur.execute(
							"""INSERT OR REPLACE INTO Images (Hash, Stars, Similarity)
							VALUES(?,COALESCE((SELECT Stars FROM Images WHERE Hash=?), 0),?)""",
							( hash_md5, hash_md5, similarity_hash )
						)

					counter_images += 1

				counter_files += 1
				set_value_callback( counter_files )

	return counter_images


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


def get_filtered_selection( tag, name, stars_from, stars_to ):

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()

		# no limitation in query
		if tag is None and name is None and stars_from == 0 and stars_to == 7:

			cur.execute( "SELECT DISTINCT Hash FROM Paths ORDER BY Path" )
			hashes = cur.fetchall()

			if len( hashes ) > 0:
				return [ h[ 0 ] for h in hashes ]
			else:
				return []

		# invalid range for stars, ignored
		elif stars_from > stars_to:

			cur.execute(
				"""SELECT DISTINCT Hash FROM Paths
				LEFT OUTER JOIN Tags USING (Hash) LEFT OUTER JOIN Names USING (Hash)
				WHERE (Tag=? OR ? is NULL) AND (Name=? OR ? is NULL) ORDER BY Path""",
				( tag, tag, name, name )
			)
			hashes = cur.fetchall()

			if len( hashes ) > 0:
				return [ h[ 0 ] for h in hashes ]
			else:
				return []

		else:

			cur.execute(
				"""SELECT DISTINCT Hash FROM Paths
				LEFT OUTER JOIN Images USING (Hash) LEFT OUTER JOIN Tags USING (Hash)
				LEFT OUTER JOIN Names USING (Hash)
				WHERE (Tag=? OR ? is NULL) AND (Name=? OR ? is NULL)
				AND ((Stars <= ? AND Stars >= ? ) OR (? is 0 AND Stars is NULL)) ORDER BY Path""",
				( tag, tag, name, name, stars_to, stars_from, stars_from )
			)
			hashes = cur.fetchall()

			if len( hashes ) > 0:
				return [ h[ 0 ] for h in hashes ]
			else:
				return []


def get_similar( hash_md5, quantity ):

	sim_1 = get_similarity_hash( hash_md5 )

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()
		cur.execute( """SELECT DISTINCT Hash,Similarity FROM Paths LEFT OUTER JOIN Images USING (Hash)""" )
		results = cur.fetchall()

		if len( results ) > 0:
			candidates = [
				( r[ 0 ], ImageSimilarity.compute_similarity_hash_difference( sim_1, r[ 1 ] ) )
				for r in results
			]
			sorted_candidates = sorted( candidates, key=lambda c: c[1] )
			limited_candidates = sorted_candidates[:quantity]
			return [ c[ 0 ] for c in limited_candidates ]

		else:
			return []


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


def get_similarity_hash( hash_md5 ):

	con = sqlite3.connect( 'daign-image-organizer.db' )
	con.text_factory = str
	with con:

		cur = con.cursor()
		cur.execute( "SELECT Similarity FROM Images WHERE Hash=?", ( hash_md5, ) )
		similarity = cur.fetchone()
		if similarity is None:
			return None
		else:
			return similarity[ 0 ]


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
			cur.execute(
				"""INSERT OR REPLACE INTO Images(Hash, Stars, Similarity)
				VALUES(?,?,(SELECT Similarity FROM Images WHERE Hash=?))""",
				( hash_md5, stars, hash_md5 )
			)

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


