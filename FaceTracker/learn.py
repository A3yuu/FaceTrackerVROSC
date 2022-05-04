# coding: UTF-8

import numpy
import tensorflow as tf
from tensorflow.python.keras.layers import *
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.optimizers import *
from tensorflow.keras.layers import *

#データ
dataPathIn = 'inM3.npy'
dataPathOut = 'outM3.npy'
modelPath = ['t.h5py', './t.weights']

#学習モデル構築
inData = numpy.load(dataPathIn)
outData = numpy.load(dataPathOut)

#モデル定義
input = Input(shape=(96,96,3))
blocks = 6
filters = 16
growth = 1
strides=(2,2)
kernelSize = (3,3)
x = input
for i in range(blocks):
	x = Conv2D(filters*(growth**i), kernelSize, strides=strides, padding='same', use_bias=False)(x)
	x = BatchNormalization()(x)
	x = Activation('relu')(x)
	x = Conv2D(filters*(growth**i), kernelSize, strides=(1,1), padding='same', use_bias=False)(x)
	x = BatchNormalization()(x)
	x = Activation('relu')(x)
x = AveragePooling2D(2)(x)
x = Conv2D(4*2, 1, kernel_initializer='he_normal')(x)
x = Activation('linear')(x)
x = Reshape((4,2))(x)

#RUN
model = tf.keras.Model(inputs=input, outputs=x)
model.summary()
#前回重みロード(なければコメントアウト)
#model.load_weights(modelPath[1])
#Run
model.compile(loss='mse', optimizer='Adam')
model.save(modelPath[0])
epochss = [300]
#epochss = [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
#epochss = [1,3,6,10,10,10,20,20,20,100,100,100,100,100,100,100,100,100]
#epochss = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
for i in epochss:
	history = model.fit(inData, outData, epochs=i, verbose=1)
	model.save_weights(modelPath[1])
