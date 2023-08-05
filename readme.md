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