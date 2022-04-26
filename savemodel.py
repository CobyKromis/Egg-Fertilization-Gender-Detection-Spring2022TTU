#File Name: savemodel.py
#Primary Contributor: Coby Kromis
#Other Contributors:
#Purpose: This file is used for the purpose of loading a pre-trained model into
#         a newly defined model and evaluating it with a testing set of images

import os
import glob
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import MaskResize as mr

#Expected height and width of input images
img_height = 256
img_width = 256
batch_size = 10

#Number of times the model will be evaluated
TEST_NUMBER = 100

#Go through file directories that contain test photos and create an array of .jpg files
fTe0 = glob.glob('C:\\Users\\cobyk\\Lab4\\EP\\Test\\0\\*.jpg')
fTe1 = glob.glob('C:\\Users\\cobyk\\Lab4\\EP\\Test\\1\\*.jpg')

#Take .jpg file arrays and mask/resize them
iTe0 = [mr.oMask(imgTe0) for imgTe0 in fTe0]
iTe1 = [mr.oMask(imgTe1) for imgTe1 in fTe1]

#Main file directory for test images
fTe = 'C:\\Users\\cobyk\\Lab4\\EP\\Test'

#Define data set from file directory defined above
test = tf.keras.preprocessing.image_dataset_from_directory(
    fTe, labels='inferred', label_mode="int",
    class_names=['0', '1'], batch_size=batch_size, image_size=(img_height, img_width),
    shuffle=True, seed=321
)

#Define sequential model with identical architecture to model defined in fd.py
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(img_height, img_width, 3),),
    keras.layers.Dense(128, activation='sigmoid'),
    layers.Dense(2)
])

#Compile defined model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss=[keras.losses.SparseCategoricalCrossentropy(from_logits=True),],
    metrics=["accuracy"]
)

#Define file location for saved weights of a trained model and load those weights into the new model defined above
mSavePath = "C:\\Users\\cobyk\\Lab4\\Models\\Model1\\cp-5000.ckpt"
model.load_weights(mSavePath)

#Run model evalutation with test images TEST_NUMBER number of times
for i in range(TEST_NUMBER):
    model.evaluate(test, batch_size=batch_size, verbose=2)