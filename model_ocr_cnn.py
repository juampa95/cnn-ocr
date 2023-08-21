from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import random

batch_size = 32
img_height = 80
img_width = 80

train_ds = tf.keras.utils.image_dataset_from_directory(
  'datasets/',
  validation_split=0.2,
  label_mode = 'categorical',
  subset="training",
  seed=123,
  color_mode='grayscale',
  image_size=(img_height, img_width),
  batch_size=batch_size,
)


val_ds = tf.keras.utils.image_dataset_from_directory(
  'datasets/',
  validation_split=0.2,
  label_mode='categorical',
  subset="validation",
  seed=123,
  color_mode='grayscale',
  image_size=(img_height, img_width),
  batch_size=batch_size)


class_names = train_ds.class_names
print(class_names)

for image_batch, labels_batch in train_ds:
  print(image_batch.shape)
  print(labels_batch.shape)
  break

# Obtencion de un lote de imágenes y etiquetas del conjunto de entrenamiento para visualizar

class_names = train_ds.class_names  # Obtener los nombres de las clases desde train_ds
for images, labels in train_ds.take(1):  # Tomamos un solo lote
    batch_size = images.shape[0]
    random_indices = random.sample(range(batch_size), 10)  # Elegimos 10 índices aleatorios

    # Graficar las 10 imágenes
    plt.figure(figsize=(15, 10))
    for i, index in enumerate(random_indices):
        ax = plt.subplot(2, 5, i + 1)  # Crear una cuadrícula de 2x5 para las imágenes
        plt.imshow(images[index].numpy().squeeze(), cmap='gray')  # Mostrar la imagen en escala de grises
        label_index = labels[index].numpy().argmax()  # Obtener el índice de la etiqueta
        label_name = class_names[label_index]  # Obtener el nombre de la etiqueta
        plt.title(f'Label: {label_name}')  # Mostrar el nombre de la etiqueta como título
        plt.axis('off')  # Ocultar ejes
    plt.show()

#Creacion de la capa para aumento de datos

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip('horizontal_and_vertical'),
    tf.keras.layers.RandomRotation(0.25),
    # tf.keras.layers.RandomBrightness(factor=(-0.05, 0.05)),
    # tf.keras.layers.RandomContrast(factor=(0.95, 1.05))
])
#Creacion de la arquitectura de red


modelo = tf.keras.models.Sequential([
    tf.keras.layers.Rescaling(1./255, input_shape=(80, 80, 1)),
    data_augmentation,
    tf.keras.layers.Conv2D(36, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Conv2D(72, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(100, activation='relu'),
    tf.keras.layers.Dense(36, activation='softmax')
])

modelo.compile(optimizer='adam',
               loss='categorical_crossentropy',
               metrics=['accuracy'])

modelo.summary()

epoch = 30

history = modelo.fit(
    train_ds, epochs=epoch, batch_size=32,
    validation_data=val_ds
)


# Visualizacion de resultados

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epoch)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

modelo.save('ocr_cnn.keras')
