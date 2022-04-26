#File Name: fd.py (stands for fertilization detection)
#Primary Contributor: Coby Kromis
#Other Contributors:
#Purpose: This file is used for the purpose of testing methods for creating, training, and testing a
#         neural network to determine the fertilization of a candled chicken egg

import glob

import os

import cv2 as cv

import string

import MaskResize as mr
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#Expected height and width of input images
img_height = 256
img_width = 256
batch_size = 10

BS_MUL = 10
SAVE_FREQ = BS_MUL

#Naming convention for file folders:
#fTr0 --> f (folder) Tr (train) 0 (unfertilized)
#fTe1 --> f (folder) Te (test) 1 (fertilized)
fTr0 = glob.glob('C:\\Users\\cobyk\\Lab4\\EP\\Train\\0\\*.jpg')
fTr1 = glob.glob('C:\\Users\\cobyk\\Lab4\\EP\\Train\\1\\*.jpg')
fTe0 = glob.glob('C:\\Users\\cobyk\\Lab4\\EP\\Test\\0\\*.jpg')
fTe1 = glob.glob('C:\\Users\\cobyk\\Lab4\\EP\\Test\\1\\*.jpg')

#Note: Naming convention will be altered slightly once white eggs are added to the data

iTr0 = [mr.oMask(imgTr0) for imgTr0 in fTr0]
iTr1 = [mr.oMask(imgTr1) for imgTr1 in fTr1]
iTe0 = [mr.oMask(imgTe0) for imgTe0 in fTe0]
iTe1 = [mr.oMask(imgTe1) for imgTe1 in fTe1]

#Define sequential model
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(img_height, img_width, 3),),
    keras.layers.Dense(128, activation='sigmoid'),
    layers.Dense(2)
])

#File locations for test and training images
fTr = 'C:\\Users\\cobyk\\Lab4\\EP\\Train'
fTe = 'C:\\Users\\cobyk\\Lab4\\EP\\Test'

#Define data set from file directories defined above
train = tf.keras.preprocessing.image_dataset_from_directory(
    fTr, labels='inferred', label_mode="int",
    class_names=['0', '1'], batch_size=batch_size, image_size=(img_height, img_width),
    shuffle=True, seed=123
)

test = tf.keras.preprocessing.image_dataset_from_directory(
    fTe, labels='inferred', label_mode="int",
    class_names=['0', '1'], batch_size=batch_size, image_size=(img_height, img_width),
    shuffle=True, seed=321
)

#Compile model defined above
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss=[keras.losses.SparseCategoricalCrossentropy(from_logits=True),],
    metrics=["accuracy"]
)

#File location and naming convention for saving training weights of model
mSavePath = "C:\\Users\\cobyk\\Lab4\\Models\\Model4\\cp-{epoch:04d}.ckpt"

#Set up callback system to save weights during training at a frequency defined by BS_MUL * batch_size
mSave = tf.keras.callbacks.ModelCheckpoint(
    filepath= mSavePath,
    save_weights_only=True,
    verbose=1,
    save_freq=SAVE_FREQ
)

model.save_weights(mSavePath.format(epoch=0))

#Train model number of times based on epoch number
model.fit(train, epochs=5000, callbacks=[mSave], verbose=2)
