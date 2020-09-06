from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob

# re-size all the images to this
IMAGE_SIZE = [224, 224]


def build():
    # add preprocessing layer to the front of VGG
    vgg = load_model('real_time_face_detector.h5')

    # No existing weights
    for layer in vgg.layers:
        layer.trainable = False

    # For number of classes
    folders = glob('Capture_face/*')

    # Layers
    x = Flatten()(vgg.output)
    # x = Dense(1000, activation='relu')(x)
    prediction = Dense(len(folders), activation='softmax')(x)

    # Object creation
    model = Model(inputs=vgg.input, outputs=prediction)

    # Model Summary
    model.summary()

    # Compile Model
    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )

    train_datagen = ImageDataGenerator(rescale=1. / 255,
                                       shear_range=0.2,
                                       zoom_range=0.2,
                                       horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1. / 255)

    training_set = train_datagen.flow_from_directory('Capture_face',
                                                     target_size=(224, 224),
                                                     batch_size=32,
                                                     class_mode='categorical')

    test_set = test_datagen.flow_from_directory('Capture_face',
                                                target_size=(224, 224),
                                                batch_size=32,
                                                class_mode='categorical')

    # fit the model
    r = model.fit_generator(
        training_set,
        validation_data=test_set,
        epochs=5,
        steps_per_epoch=len(training_set),
        validation_steps=len(test_set)
    )

    model.save('real_time_face_detector.h5')