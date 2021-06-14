import tensorflow as tf
import numpy as np
import datetime

# Check if its a CPU or GPU
device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
  print('GPU device not found')
else:
  print('Found GPU at: {}'.format(device_name))
cifar = tf.keras.datasets.cifar10

(x_train, y_train),(x_test, y_test) = cifar.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
    
  tf.keras.layers.Conv2D(32, (3, 3), padding='same', input_shape=x_train.shape[1:]),
  tf.keras.layers.Activation('relu'),
  tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
  tf.keras.layers.Dropout(0.25),

  tf.keras.layers.Conv2D(64, (3, 3), padding='same'),
  tf.keras.layers.Activation('relu'),
  tf.keras.layers.Conv2D(64, (3, 3)),
  tf.keras.layers.Activation('relu'),
  tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
  tf.keras.layers.Dropout(0.25),
    
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(512, activation=tf.nn.relu),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()


# start training
st_time = datetime.datetime.now()

model.fit(x_train, y_train, epochs=10)

# record time after training
end_time = datetime.datetime.now()

print('Training time = %s'%(end_time-st_time))

