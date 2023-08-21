<h1> Red neuronal convolucional (CNN) para detección de OCR</h1>

Este proyecto surge con el objetivo de brindar una solucion a un problema recurrente que 
presenta en la empresa donde trabajo. 

Fabricamos equipos encargados de codificar y serializar envases de medicamentos para 
laboratorios farmacéuticos. Que además de codificarlos, verifican los campos impresos mediante
el uso de cámaras y software de vision. 

Actualmente, se utiliza Tesseract para realizar la decodificación. Este motor de reconocimiento 
óptico de caracteres brindado por google ofrece resultados muy buenos en tiempos suficientemente 
rápidos como para incluirlos dentro del proceso. 

Pero la tasa de errores que tenemos con Tesseract, no satisface las necesidades de la empresa y 
nuestros clientes. Por ello, entrené un modelo personalizado de Tesseract (pueden ver el proceso
y los resultados en mi repositorio [**ocr-project**](https://github.com/juampa95/ocr-project) ) que 
no logro lo necesario, debido a algunas limitaciones en el proceso de entrenamiento.

Por ello, surge este proyecto de crear una red neuronal propia que se encargue del reconocimiento 
óptico de caracteres, el cual pueda personalizarse sin limitación alguna. 

<h2> Primeros intentos </h2>

Luego de investigar un poco mas acerca de las redes neuronales convolucionales, pude armar un primer
modelo sencillo utilizando Tensorflow y Keras. 

Antes de comenzar el entrenamiento, fue necesario armar un conjunto de datos para entrenar con esta red sencilla.
Haciendo uso de las funcionalidades ofrecidas por Keras, se uso `tf.keras.utils.image_dataset_from_directory` para
crear los datasets de entrenamiento y validation. Se pueden ver representados por la imagen siguiente

<div align="center">
  <img src="/img/ocr_cnn_results.png" width="450" height="300"/>
</div>


El modelo toma como entrada imagenes en escala de grises, que se pre-procesaran en las primeras 2 capas
1. La primer capa, hace una normalizacion de los valores de los pixeles, para que varien entre 0 y 1.
2. La segunda capa es una capa de aumento de datos, debido a que el dataset creado es reducido, opte por utiliar 
este metodo que crea variaciones dee las imagenes originales. Para ello, hace un giro horizontal o vertical de mantera 
aleatoria y luego una rotation de hasta un 25%
3. A continuacion tenemos la primer capa convolucional con 36 kernels de 3x3 con una funcion de activacion RELU.
4. Luego un MaxPooling de 2x2
4. A continuacion tenemos la segunda capa convolucional con 72 kernels de 3x3 con una funcion de activacion RELU.
5. Luego un MaxPooling de 2x2
6. Luego del agrupado y las convoluciones, tenemos un Dropout del 20%

En este punto, termina la convolucion de las imagenes, para pasar a la clasificacion mediante una red neuronal comun. 

7. Para ello "vectorizamos" los valores de los resultados de la ultima capa utilizando Flatten().

8. Luego tenemos una primera capa Densa con 100 neuronas y una funcion de activuacion RELU, para pasar a la ulimta capa 
9. Densa que clasifica en 36 cateogrias diferentes los valores de salida. Para ella, se usa una funcion de activacion softmax

Con estos pasos, la red tiene 2.3 millones de parametros para entrenar. 

***Arquitectura de red***
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 rescaling_8 (Rescaling)     (None, 80, 80, 1)         0         
                                                                 
 sequential_16 (Sequential)  (None, 80, 80, 1)         0         
                                                                 
 conv2d_16 (Conv2D)          (None, 78, 78, 36)        360       
                                                                 
 max_pooling2d_16 (MaxPooli  (None, 39, 39, 36)        0         
 ng2D)                                                           
                                                                 
 conv2d_17 (Conv2D)          (None, 37, 37, 72)        23400     
                                                                 
 max_pooling2d_17 (MaxPooli  (None, 18, 18, 72)        0         
 ng2D)                                                           
                                                                 
 dropout_8 (Dropout)         (None, 18, 18, 72)        0         
                                                                 
 flatten_8 (Flatten)         (None, 23328)             0         
                                                                 
 dense_16 (Dense)            (None, 100)               2332900   
                                                                 
 dense_17 (Dense)            (None, 36)                3636      
                                                                 
=================================================================
Total params: 2360296 (9.00 MB)
Trainable params: 2360296 (9.00 MB)
Non-trainable params: 0 (0.00 Byte)
_________________________________________________________________

