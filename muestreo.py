import random
import sys
from PIL import Image, ImageFilter

def rotate(img,angle):
	# converted to have an alpha layer
	im2 = img.convert('RGBA')
	# rotated image
	rot = im2.rotate(angle, expand=1)
	# a white image same size as rotated image
	fff = Image.new('RGBA', rot.size, (255,)*4)
	# create a composite image using the alpha layer of rot as a mask
	out = Image.composite(rot, fff, rot)
	# save your work (converting back to mode='1' or whatever..)
	return out.convert(img.mode)

def zoom(img,percentaje):
	per = 1 + percentaje
	return img.resize(( int(img.size[0] * per), int(img.size[1] * per)), Image.ANTIALIAS)
	
def grayscale(img):
	return img.convert('LA')

'''
BLUR - Difuminar	
CONTOUR
DETAIL
EDGE_ENHANCE
EDGE_ENHANCE_MORE
EMBOSS
FIND_EDGES
SHARPEN
SMOOTH
SMOOTH_MORE
'''
def apply_filter(img, filter):
	return img.filter(filter)
	
# valores coherentes 0.5 - 0.9	
def darken(img, factor):
	return img.point(lambda p: p * factor)
		
# genera set de imagenes
def muestrea(baseImage, destFolder, noImages):
	img = grayscale(Image.open(baseImage))
	samples = []
	
	# genera array de caracteristicas de imagenes
	for i in range(0, noImages):
		# rotate -20, 20 | zoom -20, 20 | blur 1 - BLUR, 0 - NO BLUR | Darken 0.6 - 0.9
		
		# genera array de muestras
		sample = [ random.randint(-20,20), random.randint(-20,20)/100, random.randint(0,1), random.randint(6,9)/10 ]
		while sample in samples:
			sample = [ random.randint(-20,20), random.randint(-20,20), random.randint(0,1), random.randint(6,9)/10 ]
		samples.append(sample)
		
	# genera imagenes
	c = 0
	for sample in samples:
		img2 = rotate(img, sample[0])
		img3 = zoom(img2, sample[1])
		if sample[2]:
			img4 = apply_filter(img3,ImageFilter.BLUR)
		else:
			img4 = img3
		img5 = darken(img4, sample[3])
		
		c=c+1
		filename = '{}/Img_{}.jpg'.format(destFolder,c) 
		print('Muestra Generada [{}] {} ...'.format(sample,filename))
		# png no soporta transparencias
		# https://stackoverflow.com/questions/48248405/cannot-write-mode-rgba-as-jpeg
		img5.convert('RGB').save(filename) 

	
if __name__ == '__main__':
	# argv[1] = Muestra, argv[2] = dest, argv[3] = Numero de muestras
	if len(sys.argv) == 4:
		muestrea(sys.argv[1], sys.argv[2], int(sys.argv[3]))
	else:
		print("Usage: python muestreo.py <muestra.png> <destino> <No Muestras>")