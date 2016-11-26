#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image


def get_quintile_indices( a ):

	quintiles = np.percentile( a, [ 20, 40, 60, 80 ] )
	result = 4 - ( np.asarray( quintiles )[ :, None ] >= a ).sum( 0 )
	return result


def to_custom_binary_representation( a ):

	b = np.zeros( a.shape[ 0 ] * 4 )
	for i,ai in enumerate( a ):
		if ai > 0:
			b[ ( i*4 + 4 - ai ) : ( i*4 + 4 ) ] = 1

	return b


def channel_to_hash( ch ):

	hist = np.bincount( ch / 32, minlength = 8 )
	qi = get_quintile_indices( hist )
	cb = to_custom_binary_representation( qi )
	hash_string = ''.join( [ str( int( digit ) ) for digit in cb ] )
	return hash_string


# A very simple perceptual hash using histograms.
# Worked for me on rotated, scaled, cropped and desaturated copies.
# Gives a 128 Bit binary string. Distance is measured by hamming distance.
def compute_similarity_hash( path ):

	image = Image.open( path )
	data = np.array( image, dtype='uint8' )
	#reverse: image = Image.fromarray( data )

	# a single channel only
	if len( data.shape ) < 3:
		gray  = data.flatten()
		red   = gray
		green = gray
		blue  = gray

	# less than 3 channels
	elif data.shape[ 2 ] < 3:
		gray  = data[ ..., 0 ].flatten()
		red   = gray
		green = gray
		blue  = gray

	# full 3 RGB channels and maybe more
	else:
		rgb = data[ ..., :3 ]

		red   = rgb[ ..., 0 ].flatten()
		green = rgb[ ..., 1 ].flatten()
		blue  = rgb[ ..., 2 ].flatten()

		#gray = np.mean( rgb, -1 ).flatten()
		gray = np.round( 0.299*red + 0.587*green + 0.114*blue ).astype( 'uint8' )

	hash_red   = channel_to_hash( red )
	hash_green = channel_to_hash( green )
	hash_blue  = channel_to_hash( blue )
	hash_gray  = channel_to_hash( gray )

	hash_string_complete = hash_red + hash_green + hash_blue + hash_gray
	return hash_string_complete


def compute_similarity_hash_difference( s1, s2 ):

	assert len( s1 ) == len( s2 )
	return sum( c1 != c2 for c1, c2 in zip( s1, s2 ) )


