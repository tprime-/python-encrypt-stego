#!/usr/bin/env python

from PIL import Image
from Crypto.Cipher import AES
from Crypto import Random
import argparse

def encrypt(key, secret_message):
	iv = Random.new().read(AES.block_size) # iv is 16 bytes long
	print "Original IV:", iv
	obj = AES.new(key, AES.MODE_CFB, iv)
	ciphertext = obj.encrypt(secret_message)

	return iv, ciphertext

def decrypt(extracted_iv, key, ciphertext):
	print "Extracted IV:", extracted_iv
	obj = AES.new(key, AES.MODE_CFB, extracted_iv)
	plaintext = obj.decrypt(ciphertext)

	return plaintext

def encode_stego(key, secret_message, target_image):
	source_image = Image.open(target_image)
	dest_image = Image.new("RGB", source_image.size)

	print "Source image size:", source_image.size
	print "Encoding..."

	# copy pixel values from our source image into destination image
	for column in range(source_image.size[0]):	
		for row in range(source_image.size[1]):
			dest_image.putpixel((column,row), source_image.getpixel((column,row)))

	iv, ciphertext = encrypt(key, secret_message)
	iv_and_ciphertext = iv + ciphertext

	# hide our secret message in the first len(iv_and_ciphertext) pixels
	for pixel in range(len(iv_and_ciphertext)):
		dest_image.putpixel((pixel,0), (source_image.getpixel((0, pixel))[0], source_image.getpixel((0, pixel))[1], ord(iv_and_ciphertext[pixel])))

	#write to disk
	dest_image.save('stego.png')

	return

def decode_stego(target_image):
	extracted_iv = ""
	ciphertext = ""
	stego_image = Image.open(target_image)

	print "Decoding..."

	# extract our IV from the first 16 bytes of the image
	for pixel in list(stego_image.getdata())[0:16]:
		extracted_iv+=chr(pixel[2])

	# extract the rest
	for pixel in list(stego_image.getdata())[16:]:
		ciphertext+=chr(pixel[2])

	return extracted_iv, ciphertext

def main(args):
	if len(args.key) not in (16, 24, 32):
		print "Key length must be 16, 24, or 32 bytes long"
	elif args.operation == "encrypt":
		encode_stego(args.key, args.secret_message, args.target_image)
	else:
		extracted_iv, ciphertext = decode_stego(args.target_image)
		print decrypt(extracted_iv, args.key, ciphertext)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='Encode an encrypted message within an image',
		usage='Usage: ./stego.py -o [encrypt]|[decrypt] -m [message] -k [key] -i [image] -v',
	)
	parser.add_argument('-v', '--version',
		action='version',
		version='stego version 0.1',
	)
	parser.add_argument('-o',
		dest='operation',
		help='Operation: encrypt or decrypt',
		choices=['encrypt','decrypt'],
		required=True,
	)
	parser.add_argument('-m',
		dest='secret_message',
		help='Message to encrypt and encode',
	#	required=True,
	)
	parser.add_argument('-k',
		dest='key',
		help='Encryption key - must be a multiple of 16',
		required=True,
	)
	parser.add_argument('-i',
		dest='target_image',
		help='Image to encode or decode',
		required=True,
	)
	args = parser.parse_args()
	main(args)