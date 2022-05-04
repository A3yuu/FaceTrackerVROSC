# coding: UTF-8

import numpy
import random
import cv2

rOfs = 0.3
rScl = 1.7

#データ
inDataPath = 'inM3.npy'
outDataPath = 'outM3.npy'

#300w
imagePath = '01_Indoor/'
imageFiles = [imagePath + 'indoor_' + str(x+1).zfill(3) + '.png' for x in range(300)]
annotationPath = '01_Indoor/'
annotationFiles = [annotationPath + 'indoor_' + str(x+1).zfill(3) + '.pts' for x in range(300)]

inData = []
outData = []

roopCounter = -1

def show(image, annotation):
	imageS=image.copy()
	for a in annotation:
		pos = [int(i*96) for i in a]
		cv2.drawMarker(imageS, pos, (0, 255, 0))
	cv2.imshow("video frame", imageS)
	cv2.waitKey(300)

#ループ
for annotationFile in annotationFiles:
	roopCounter=roopCounter+1
	print(annotationFile)
	with open(annotationFile, 'r') as file:
		#300W
		imageFile = imageFiles[roopCounter]
		file.readline()
		file.readline()
		file.readline()
	
		#入力データ
		image = cv2.imread(imageFile, cv2.IMREAD_COLOR)
		#教師データ
		annotation = []
		for line in file:
			if line[0] == '}':
				break
			x, y = line.replace('\n', '').replace('\r', '').split(' ')
			annotation.append([float(x),float(y)])
		
		annotation = numpy.array(annotation)
		#口周りだけ
		minx = min(annotation[48:68,0])
		miny = min(annotation[48:68,1])
		maxx = max(annotation[48:68,0])
		maxy = max(annotation[48:68,1])
		h = maxy-miny
		w = maxx-minx
		if h<w:
			l=w
		else:
			l=h
		for i in range(16):
			minx2 = int(minx - (random.random()-rOfs)*l/rScl)
			miny2 = int(miny - (random.random()-rOfs)*l/rScl)
			maxx2 = int(maxx + (random.random()-rOfs)*l/rScl)
			maxy2 = int(maxy + (random.random()-rOfs)*l/rScl)
			h2 = maxy2-miny2
			w2 = maxx2-minx2
			if h2<w2:
				l2=w2
				o=int((w2-h2)/2)
				miny2 -= o
				maxy2 += o
			else:
				l2=h2
				o=int((h2-w2)/2)
				minx2 -= o
				maxx2 += o
			image2 = cv2.resize(image[miny2 : maxy2, minx2 : maxx2],dsize=(96, 96))
			inData.append(image2)
			annotation2 = [annotation[60],annotation[64],annotation[62],annotation[66]]
			annotation2 = (annotation2-numpy.array([minx2,miny2])) / l2
			outData.append(annotation2)
			#show(image2,annotation2)
			#mirror
			image2 = cv2.flip(image2, 1)
			inData.append(image2)
			annotation2 = annotation2 * numpy.array([-1,1]) + numpy.array([1,0])
			annotation2[0],annotation2[1] = annotation2[1],annotation2[0].copy()
			outData.append(annotation2)
			#show(image2,annotation2)

		

numpy.save(inDataPath, numpy.array(inData, dtype=numpy.uint8))
numpy.save(outDataPath, numpy.array(outData, dtype=numpy.float16))
