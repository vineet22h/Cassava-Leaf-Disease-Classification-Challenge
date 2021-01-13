import numpy as np
from efficientnet.keras import EfficientNetB7, EfficientNetB4, EfficientNetB5
from tensorflow.keras import models, layers
from tensorflow.keras.optimizers import Adam

def create_model_b7():
    conv_base = EfficientNetB7(include_top = False,
                               input_shape = (600, 600, 3))
    model = conv_base.output
    model = layers.GlobalAveragePooling2D()(model)
    model = layers.Dense(5, activation = "softmax")(model)
    model = models.Model(conv_base.input, model)

    model.compile(optimizer = Adam(lr = 0.001),
                  loss = "sparse_categorical_crossentropy",
                  metrics = ["acc"])
    return model

def create_model_b5():
    conv_base = EfficientNetB5(include_top = False,
                               input_shape = (456, 456, 3))
    model = conv_base.output
    model = layers.GlobalAveragePooling2D()(model)
    model = layers.Dense(5, activation = "softmax")(model)
    model = models.Model(conv_base.input, model)

    model.compile(optimizer = Adam(lr = 0.001),
                  loss = "sparse_categorical_crossentropy",
                  metrics = ["acc"])
    return model

def create_model_b4():
    conv_base = EfficientNetB4(include_top = False,
                               input_shape = (380, 380, 3))
    model = conv_base.output
    model = layers.GlobalAveragePooling2D()(model)
    model = layers.Dense(5, activation = "softmax")(model)
    model = models.Model(conv_base.input, model)

    model.compile(optimizer = Adam(lr = 0.001),
                  loss = "sparse_categorical_crossentropy",
                  metrics = ["acc"])
    return model