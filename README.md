#SBERRY-AI 1.0

Aplicación movil para la identificación de problemas fitosanitarios de fresa basado en el modelo MobileNetV2 con un ACC del 99.6% .

El modelo fue entrenado para detectar: 
- Mancha angular (*Xanthomonas fragariae*)
- Antracnosis (*Colletotrichum* spp.)
- Viruela (*Ramularia tulasnei*)
- Oídio en hoja ( *Sphaerotheca macularis*)
- Oídio en fruto (*Sphaerotheca macularis*)
- Moho gris en fruto (*Botrytis cinerea*)
- Quemadura de la hoja (*Diplocarpon earlianum*) 
- Frutos sanos 
- Hojas sanas


La aplicación está basada en el framework de Kivy y Buildozer:

Las imágenes para el entrenamiento del modelo se obtuvieron de los trabajos realizados por:
- Afzaal U., Bhattarai B., Pandeya Y. R. and Lee J. (2021). An instance segmentation model for strawberry diseases based on mask R-CNN. *Sensors*, *21*(19): 6565. https://doi.org/10.3390/s21196565
- Hariri M. and Avşar E. (2022). Tipburn disorder detection in strawberry leaves using convolutional neural networks and particle swarm optimization. *Multimedia Tools and Applications*, *81*(8), pp:11795-11822. https://doi.org/10.1007/s11042-022-12759-6
- Hughes D. and Salathé M. (2015). An open access repository of images on plant health to enable the development of mobile disease diagnostics. 
- Shreya M. (2023). Fruits Dataset (Images). Kaggle. https://doi.org/10.34740/KAGGLE/DSV/5514079 (Septiembre 2023).
- Sultana N., Jahan M. and Uddin M. S. (2022). An extensive dataset for successful recognition of fresh and rotten fruits. *Data in Brief*. 44:108552. https://doi.org/10.17632/bdd69gyhv8.1
https://doi.org/10.48550/arXiv.1511.08060


Contacto: "Giovanny M.R." al correo: <epsiloncob@gmail.com>

En ubuntu, el proceso automático para crear la aplicación es la siguiente:
En la terminal ejecuta los siguientes comandos:
sudo apt update
sudo apt install git

#clona el repositorio con:
git clone https://github.com/Giovanny-Montes/Sberry-AI.git

#Entra a la carpeta del proyecto
cd Sberry-AI

#Dentro damos permisos de ejecución al archivo setup.sh
chmod +x setup.sh

#Ejecutamos el instalador automatico, creará un entorno virtual de python llamado app.
./setup.sh
#Este archivo ejecuta todos los comandos necesarios para instalar dependencias y crea la aplicación.(Pueden existir errores que dependen de los permisos del usuario) 
#Tiempo estimado de 45min



